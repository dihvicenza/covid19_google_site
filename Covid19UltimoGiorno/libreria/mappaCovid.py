#In questo file la funzione per ottenere il csv da cui si realizza la mappa relativa all'ultima giornata con l'italia suddivisa in regioni
#Per i commenti dettagliati vedere il file graficiCovid.py 
import pandas as pd
import os
from os import environ
import datetime
from datetime import date as dateImport
from github import Github, InputGitTreeElement
from datetime import date

pd.options.mode.chained_assignment = None


#Funzione chiamata da application per leggere il csv della Protezione Civile, elaborarne i dati, generare un nuovo csv e pusharlo nella cartella pubblica "Covid" di github
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


	#TASSO TAMPONI TOTALI ULTIMO GIORNO
	tamponiEffettuatuUltimoGiorno=covid19UltimoGiorno["tamponi"]-covid19PenultimoGiorno["tamponi"]
	tamponiEffettuatuUltimoGiornoTotale=tamponiEffettuatuUltimoGiorno.sum()
	nuoviPositiviUltimoGiornoInItalia=covid19UltimoGiorno["nuovi_positivi"].sum()
	rapportoPositiviSuTotaleTamponiUltimoGiorno=covid19UltimoGiorno["nuovi_positivi"]*100/tamponiEffettuatuUltimoGiorno
	rapportoPositiviTamponiUltimoGiornoInItalia=nuoviPositiviUltimoGiornoInItalia*100/tamponiEffettuatuUltimoGiornoTotale

	#TASSO TAMPONI MOLECOLARI ULTIMO GIORNO
	tamponiMolecolariUltimoGiorno=covid19UltimoGiorno["tamponi_test_molecolare"]-covid19PenultimoGiorno["tamponi_test_molecolare"]
	nuoviPositiviMolecolare=covid19UltimoGiorno["totale_positivi_test_molecolare"]-covid19PenultimoGiorno["totale_positivi_test_molecolare"]
	tassoPositiviMolecolari=nuoviPositiviMolecolare*100/tamponiMolecolariUltimoGiorno
	tassoNazionalePositiviMolecolari=nuoviPositiviMolecolare.sum()*100/tamponiMolecolariUltimoGiorno.sum()

	#TERAPIA INTENSIVA ULTIMO GIORNO
	ingressiUltimoGiornoTerapiaIntensiva=covid19UltimoGiorno["terapia_intensiva"]-covid19PenultimoGiorno["terapia_intensiva"]
	ingressiUltimoGiornoTerapiaIntensivaInItalia=ingressiUltimoGiornoTerapiaIntensiva.sum()


	#RICOVERI ORDINARI ULTIMO GIORNO
	ingressiUltimoGiornoOspedaleCompresaTerapiaIntensiva=covid19UltimoGiorno["totale_ospedalizzati"]-covid19PenultimoGiorno["totale_ospedalizzati"]
	ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva=ingressiUltimoGiornoOspedaleCompresaTerapiaIntensiva-ingressiUltimoGiornoTerapiaIntensiva
	ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia=ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva.sum()


	#DECEDUTI ULTIMO GIORNO
	decedutiUltimoGiorno=covid19UltimoGiorno["deceduti"]-covid19PenultimoGiorno["deceduti"]

	#--------------------------------------------------------CREAZIONE CSV---------------------------------------------

	regioni=covid19UltimoGiorno.index #regioni è la serie costituita dagli indici del dataframe, cioè tutte le regioni

	covid19Mappa=pd.DataFrame({"regione":regioni,"rapportoGiornalieroSuTamponiTotali":rapportoPositiviSuTotaleTamponiUltimoGiorno,"rapportoGiornalieroSuTamponiMolecolari":tassoPositiviMolecolari,"ingressiGiornalieriInIntensiva":ingressiUltimoGiornoTerapiaIntensiva,"ingressiGiornalieriFuoriIntensiva":ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva,"decedutiGiornalieri":decedutiUltimoGiorno})

	#AGGIUNGIAMO LE COLONNE RELATIVE AL DATO NAZIONALE. 
	#Mettiamo in ogni colonna lo stesso valore 21 volte, perché tutte le colonne dei Dataframe devono essere lunghe uguali
	covid19Mappa["rapportoItalianoSuTamponiTotali"]= [rapportoPositiviTamponiUltimoGiornoInItalia for i in range(21)]
	covid19Mappa["rapportoItalianoSuTamponiMolecolari"] = [tassoNazionalePositiviMolecolari for i in range(21)]
	covid19Mappa["ingressiInIntensivaMediaRegionale"]= [ingressiUltimoGiornoTerapiaIntensivaInItalia/21 for i in range(21)]#Diviso 21 perchè calcola la media regionale
	covid19Mappa["ingressiInOspedaleNonIntensivaMediaRegionale"]= [ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia/21 for i in range(21)] #Diviso 21 perchè calcola la media regionale
	covid19Mappa["decedutiMediaRegionale"]= [(decedutiUltimoGiorno.sum())/21  for i in range(21)] #Diviso 21 perchè calcola la media regionale

	#-----------------------------------------------COMMIT SU GITHUB-----------------------------------------------------------
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


