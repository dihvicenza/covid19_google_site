import pandas as pd
#import matplotlib.pyplot as plt
import os
from os import environ

import datetime
from datetime import date as dateImport
pd.options.mode.chained_assignment = None


def mappa():


	covid19 = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv",sep=",")

	covid19['data']=(pd.to_datetime(covid19["data"]))
	covid19=covid19.fillna(0)
	#print (covid19.info())
	listaDate=list(pd.to_datetime(covid19["data"]))
	for i in range(len(listaDate)):
		listaDate[i]=listaDate[i].strftime("%d-%m-%Y")
	covid19["data"]=listaDate.copy()


	covid19.drop(["stato","codice_regione","lat","long","codice_nuts_1", "codice_nuts_2","note","note_test","note_casi"], axis=1, inplace=True)

	covid19.set_index("denominazione_regione",inplace=True)

	date=covid19["data"]

	ultimoGiorno=date[-1]
	penultimoGiorno=date[-22]
	covid19UltimoGiorno=covid19[covid19["data"]==ultimoGiorno]
	covid19PenultimoGiorno=covid19[covid19["data"]==penultimoGiorno]


	#Rapporto positivi su totale tamponi effettuati ultimo giorno
	tamponiEffettuatuUltimoGiorno=covid19UltimoGiorno["tamponi"]-covid19PenultimoGiorno["tamponi"]
	tamponiEffettuatuUltimoGiornoTotale=tamponiEffettuatuUltimoGiorno.sum()
	##print(tamponiEffettuatuUltimoGiorno)
	##print(tamponiEffettuatuUltimoGiornoTotale)
	nuoviPositiviUltimoGiornoInItalia=covid19UltimoGiorno["nuovi_positivi"].sum()
	##print(nuoviPositiviUltimoGiornoInItalia)
	rapportoPositiviSuTotaleTamponiUltimoGiorno=covid19UltimoGiorno["nuovi_positivi"]*100/tamponiEffettuatuUltimoGiorno
	##print(rapportoPositiviSuTotaleTamponiUltimoGiorno)
	##print(covid19.info())
	rapportoPositiviTamponiUltimoGiornoInItalia=nuoviPositiviUltimoGiornoInItalia*100/tamponiEffettuatuUltimoGiornoTotale
	##print("\n\n\nRapporto positivi tamponi totali ultimo giorno regione per regione")
	##print(rapportoPositiviSuTotaleTamponiUltimoGiorno)
	##print ("Nell'ultima giornata il rapporto positivi/tamponi totali e del " +str(rapportoPositiviTamponiUltimoGiornoInItalia)+"%")


	#Rapporto positivi su tamponi molecolari ultimo giorno
	tamponiMolecolariUltimoGiorno=covid19UltimoGiorno["tamponi_test_molecolare"]-covid19PenultimoGiorno["tamponi_test_molecolare"]
	nuoviPositiviMolecolare=covid19UltimoGiorno["totale_positivi_test_molecolare"]-covid19PenultimoGiorno["totale_positivi_test_molecolare"]
	tassoPositiviMolecolari=nuoviPositiviMolecolare*100/tamponiMolecolariUltimoGiorno
	##print("\n\n\nTasso di positivita al tampone molecolare ultimo giorno regione per regione")
	##print(tassoPositiviMolecolari)
	tassoNazionalePositiviMolecolari=nuoviPositiviMolecolare.sum()*100/tamponiMolecolariUltimoGiorno.sum()
	##print("Il tasso di positivita ai tamponi molecolari nell'ultima giornata e pari al "+str(tassoNazionalePositiviMolecolari)+"%")




	#Ingressi ultimo giorno in terapia intensiva
	ingressiUltimoGiornoTerapiaIntensiva=covid19UltimoGiorno["terapia_intensiva"]-covid19PenultimoGiorno["terapia_intensiva"]
	##print("\n\n\nReparti terapia intensiva ultimo giorno regione per regione")
	##print (ingressiUltimoGiornoTerapiaIntensiva)
	ingressiUltimoGiornoTerapiaIntensivaInItalia=ingressiUltimoGiornoTerapiaIntensiva.sum()
	valore="un incremento"
	if ingressiUltimoGiornoTerapiaIntensivaInItalia<0:
		valore="una riduzione"

	##print("Rispetto a ieri oggi le terapie intensive segnano " +valore+" di "+str(abs(ingressiUltimoGiornoTerapiaIntensivaInItalia))+" unita")

	#Ingressi ospedalieri ultimo giorno NON in terapia intensiva
	ingressiUltimoGiornoOspedaleCompresaTerapiaIntensiva=covid19UltimoGiorno["totale_ospedalizzati"]-covid19PenultimoGiorno["totale_ospedalizzati"]
	ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva=ingressiUltimoGiornoOspedaleCompresaTerapiaIntensiva-ingressiUltimoGiornoTerapiaIntensiva
	##print("\n\n\nReparti non terapia intensiva ultimo giorno regione per regione")
	##print(ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva)
	ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia=ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva.sum()
	valore="un incremento"
	if ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia<0:
		valore="una riduzione"
	##print("Rispetto a ieri oggi i reparti non in terapia intensive segnano " +valore+" di "+str(abs(ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia))+" unita")


	#Morti ultimo giorno
	decedutiUltimoGiorno=covid19UltimoGiorno["deceduti"]-covid19PenultimoGiorno["deceduti"]

	


	##print("\n\n\n\n\n\n\n")
	##print("Dati del giorno "+ str(list(covid19UltimoGiorno["data"])[0]))
	##print("Rapporto positivi/tamponi ultimo giorno = %.2f" % rapportoPositiviTamponiUltimoGiornoInItalia+"%")
	##print("Rapporto positivi/tamponi ultima settimana =%.2f" %rapportoPositiviUltimaSettimanaInItalia+"%")
	##print("Rapporto positivi/tamponi MOLECOLARI ultimo giorno = %.2f" %tassoNazionalePositiviMolecolari+"%")
	##print("Rapporto positivi/tamponi MOLECOLARI ultima settimana = %.2f" %tassoNazionalePositiviMolecolariUltimaSettimana+"%")
	##print("Ingressi terapia intensiva ultimo giorno = "+str(ingressiUltimoGiornoTerapiaIntensivaInItalia))
	##print("Ingressi terapia intensiva ultima settimana = "+str(nuoveTerapieIntensiveUltimaSettimanaItalia))
	##print("Ingressi NON terapia intensiva ultimo giorno = "+str(ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia))
	##print("Ingressi NON terapia intensiva ultima settimana = "+str(ingressiUltimaSettimanaOspedaleSenzaTerapiaIntensivaInItalia))
	##print("Deceduti giornalieri = "+str(decedutiUltimoGiorno.sum()))
	##print("Deceduti settimanali = "+str(decedutiUltimaSettimana.sum()))
	##print("Letalita da inizio pandemia = %.2f" %tassoDiMortalitaNazionale+"%")


	regioni=covid19UltimoGiorno.index

	covid19Mappa=pd.DataFrame({"regione":regioni,"rapportoGiornalieroSuTamponiTotali":rapportoPositiviSuTotaleTamponiUltimoGiorno,"rapportoGiornalieroSuTamponiMolecolari":tassoPositiviMolecolari,"ingressiGiornalieriInIntensiva":ingressiUltimoGiornoTerapiaIntensiva,"ingressiGiornalieriFuoriIntensiva":ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva,"decedutiGiornalieri":decedutiUltimoGiorno})

	#AGGIUNGIAMO LE COLONNE RELATIVE AL DATO NAZIONALE. Mettiamo in ogni colonna lo stesso valore 21 volte, perché tutte le colonne dei Dataframe devono essere lunghe uguali
	covid19Mappa["rapportoItalianoSuTamponiTotali"]= [rapportoPositiviTamponiUltimoGiornoInItalia for i in range(21)]
	covid19Mappa["rapportoItalianoSuTamponiMolecolari"] = [tassoNazionalePositiviMolecolari for i in range(21)]
	covid19Mappa["ingressiInIntensivaMediaRegionale"]= [ingressiUltimoGiornoTerapiaIntensivaInItalia/21 for i in range(21)]
	covid19Mappa["ingressiInOspedaleNonIntensivaMediaRegionale"]= [ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia/21 for i in range(21)]
	covid19Mappa["decedutiMediaRegionale"]= [(decedutiUltimoGiorno.sum())/21  for i in range(21)]


	d=covid19Mappa.to_csv(sep=",",index=False)

	from github import Github, InputGitTreeElement
	from datetime import date

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


