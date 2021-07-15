import pandas as pd
pd.options.mode.chained_assignment = None
from github import Github, InputGitTreeElement
from datetime import date
from os import environ

def mappa():

	covid19 = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv",sep=",")

	covid19['data']=(pd.to_datetime(covid19["data"]))
	covid19=covid19.fillna(0)
	listaDate1=list(pd.to_datetime(covid19["data"]))
	listaDate=[listaDate1[i].strftime("%d-%m-%Y") for i in range(len(listaDate1))]
	covid19["data"]=listaDate.copy()

	covid19.drop(["stato","codice_regione","lat","long","codice_nuts_1", "codice_nuts_2","note","note_test","note_casi"], axis=1, inplace=True)
	covid19.set_index("denominazione_regione",inplace=True)

	ultimoGiorno=listaDate[-1]
	penultimoGiorno=listaDate[-22]
	covid19UltimoGiorno=covid19[covid19["data"]==ultimoGiorno]
	covid19PenultimoGiorno=covid19[covid19["data"]==penultimoGiorno]

	#---------------Rapporto positivi su totale tamponi effettuati ultimo giorno-------------
	tamponiEffettuatuUltimoGiorno=covid19UltimoGiorno["tamponi"]-covid19PenultimoGiorno["tamponi"]
	tamponiEffettuatuUltimoGiornoTotale=tamponiEffettuatuUltimoGiorno.sum()
	nuoviPositiviUltimoGiornoInItalia=covid19UltimoGiorno["nuovi_positivi"].sum()
	rapportoPositiviSuTotaleTamponiUltimoGiorno=covid19UltimoGiorno["nuovi_positivi"]*100/tamponiEffettuatuUltimoGiorno
	rapportoPositiviTamponiUltimoGiornoInItalia=nuoviPositiviUltimoGiornoInItalia*100/tamponiEffettuatuUltimoGiornoTotale

	#----------------Rapporto positivi su tamponi molecolari ultimo giorno------------------
	tamponiMolecolariUltimoGiorno=covid19UltimoGiorno["tamponi_test_molecolare"]-covid19PenultimoGiorno["tamponi_test_molecolare"]
	nuoviPositiviMolecolare=covid19UltimoGiorno["totale_positivi_test_molecolare"]-covid19PenultimoGiorno["totale_positivi_test_molecolare"]
	tassoPositiviMolecolari=nuoviPositiviMolecolare*100/tamponiMolecolariUltimoGiorno
	tassoNazionalePositiviMolecolari=nuoviPositiviMolecolare.sum()*100/tamponiMolecolariUltimoGiorno.sum()

	#-----------------Ingressi ultimo giorno in terapia intensiva---------------------------
	ingressiUltimoGiornoTerapiaIntensiva=covid19UltimoGiorno["terapia_intensiva"]-covid19PenultimoGiorno["terapia_intensiva"]
	ingressiUltimoGiornoTerapiaIntensivaInItalia=ingressiUltimoGiornoTerapiaIntensiva.sum()

	#----------Ingressi ospedalieri ultimo giorno NON in terapia intensiva-----------------
	ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva=covid19UltimoGiorno["ricoverati_con_sintomi"]-covid19PenultimoGiorno["ricoverati_con_sintomi"]
	ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia=ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva.sum()

	#--------------------------Morti ultimo giorno--------------------------------
	decedutiUltimoGiorno=covid19UltimoGiorno["deceduti"]-covid19PenultimoGiorno["deceduti"]

	regioni=covid19UltimoGiorno.index

	covid19Mappa=pd.DataFrame({"regione":regioni,"rapportoGiornalieroSuTamponiTotali":rapportoPositiviSuTotaleTamponiUltimoGiorno,"rapportoGiornalieroSuTamponiMolecolari":tassoPositiviMolecolari,"ingressiGiornalieriInIntensiva":ingressiUltimoGiornoTerapiaIntensiva,"ingressiGiornalieriFuoriIntensiva":ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva,"decedutiGiornalieri":decedutiUltimoGiorno})

	#AGGIUNGIAMO LE COLONNE RELATIVE AL DATO NAZIONALE. Mettiamo in ogni colonna lo stesso valore 21 volte, perché tutte le colonne dei Dataframe devono essere lunghe uguali
	listaItaliaPositiviTotali=[]
	listaItaliaPositiviMolecolari=[]
	listaItaliaIntensiva=[]
	listaItaliaOrdinari=[]
	listaItaliaDeceduti=[]
	for i in range(21):
		listaItaliaPositiviTotali.append(rapportoPositiviTamponiUltimoGiornoInItalia)
		listaItaliaPositiviMolecolari.append(tassoNazionalePositiviMolecolari)
		listaItaliaIntensiva.append(ingressiUltimoGiornoTerapiaIntensivaInItalia)
		listaItaliaOrdinari.append(ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia)
		listaItaliaDeceduti.append(decedutiUltimoGiorno.sum()/21)

	covid19Mappa["rapportoItalianoSuTamponiTotali"]=listaItaliaPositiviTotali
	covid19Mappa["rapportoItalianoSuTamponiMolecolari"]=listaItaliaPositiviMolecolari
	covid19Mappa["ingressiInIntensivaMediaRegionale"]=listaItaliaIntensiva
	covid19Mappa["ingressiInOspedaleNonIntensivaMediaRegionale"]=listaItaliaOrdinari
	covid19Mappa["decedutiMediaRegionale"]=listaItaliaDeceduti

	#-------------------------------COMMIT SU GITHUB------------------------
	d=covid19Mappa.to_csv(sep=",",index=False)

	fileList=[d]
	listaGiornoMeseAnno=listaDate[-1].split("-")
	fileNames=["Covid19-"+listaGiornoMeseAnno[2]+"-"+listaGiornoMeseAnno[1]+"-"+listaGiornoMeseAnno[0]+".csv"]
	commitMessage=date.today().strftime("%d-%m-%Y")
	g=Github(environ["gitToken"])

	#creo connessione
	repo=g.get_user().get_repo("Covid")
	mainRef= repo.get_git_ref("heads/main")

	#carichiamo il file
	mainSha=mainRef.object.sha
	baseTree= repo.get_git_tree(mainSha)

	elementList=[]
	for j in range(len(fileList)):
		element=InputGitTreeElement(fileNames[j],'100644','blob',fileList[j])#100644 è per file normale, 'blob' binary large object per caricare su gihub file
		elementList.append(element)

	tree=repo.create_git_tree(elementList, baseTree)
	parent=repo.get_git_commit(mainSha)

	commit=repo.create_git_commit(commitMessage,tree,[parent])
	mainRef.edit(commit.sha)
	print("Aggiornamento mappa completato")