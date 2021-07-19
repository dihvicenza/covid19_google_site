#In questo file la funzione per ottenere i csv (uno per ogni giornata) da cui si realizzeranno le mappe con l'Italia suddivisa in regioni
#PER I COMMENTI DETTAGLIATI VEDERE IL FILE "graficiCovid.py"


import pandas as pd
import os
from os import environ
import datetime
from datetime import date as dateImport
from github import Github, InputGitTreeElement
from datetime import date as dateImport

pd.options.mode.chained_assignment = None

#Funzione chiamata da application per leggere il csv della Protezione Civile, elaborarne i dati, generare i nuovi csv e pusharli nella cartella pubblica "Covid" di github
def mappa():

	covid19 = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv",sep=",")
	covid19['data']=(pd.to_datetime(covid19["data"]))
	covid19=covid19.fillna(0)
	listaDate=list(pd.to_datetime(covid19["data"]))
	for i in range(len(listaDate)):
		listaDate[i]=listaDate[i].strftime("%d-%m-%Y")
	
	covid19["data"]=listaDate.copy()
	date=covid19["data"]
	quanteDateCiSonoState=len(date)//21
	listaDate=[]
	listaDate=[date[21*i] for i in range(quanteDateCiSonoState)]


	covid19.drop(["stato","codice_regione","lat","long","codice_nuts_1", "codice_nuts_2","note","note_test","note_casi"], axis=1, inplace=True)
	covid19.set_index("denominazione_regione",inplace=True)


	#---------------------------------------------------------------PRIMO GIORNO------------------------------------------------------
	covid19PrimoGiorno=covid19[covid19["data"]==date[0]]
	
	#TAMPONI MOLECOLARI
	tamponiEffettuatiPrimoGiorno=covid19PrimoGiorno["tamponi"]
	tamponiEffettuatiPrimoGiornoTotale=tamponiEffettuatiPrimoGiorno.sum()
	nuoviPositiviPrimoGiornoInItalia=covid19PrimoGiorno["nuovi_positivi"].sum()
	rapportoPositiviSuTamponiMolecolariPrimoGiorno=covid19PrimoGiorno["nuovi_positivi"]*100/tamponiEffettuatiPrimoGiorno
	rapportoPositiviTamponiPrimoGiornoInItalia=nuoviPositiviPrimoGiornoInItalia*100/tamponiEffettuatiPrimoGiornoTotale

	#TERAPIE INTENSIVE
	ingressiPrimoGiornoTerapiaIntensiva=covid19PrimoGiorno["terapia_intensiva"]
	ingressiPrimoGiornoTerapiaIntensivaMediaRegionale=ingressiPrimoGiornoTerapiaIntensiva.sum()/21 #/21 perchè voglio la media regionale
	 
	#RICOVERI ORDINARI
	ingressiOrdinariPrimoGiorno=covid19PrimoGiorno["ricoverati_con_sintomi"]
	ingressiOrdinariPrimoGiornoMediaRegionale=ingressiOrdinariPrimoGiorno.sum()/21 #/21 perchè voglio la media regionale

	#DECEDUTI
	decedutiPrimoGiorno=covid19PrimoGiorno["deceduti"]
	decedutiPrimoGiornoMediaRegionale=decedutiPrimoGiorno.sum()/21 #/21 perchè voglio la media regionale


	#-------------------------------------CREAZIONE CSV PRIMO GIORNO----------------------------------------
	regioni=covid19PrimoGiorno.index #regioni è la serie costituita dagli indici del dataframe, cioè tutte le regioni
	covid19MappaPrimoGiorno=pd.DataFrame({"regione":regioni,"rapportoGiornalieroSuTamponiMolecolari":rapportoPositiviSuTamponiMolecolariPrimoGiorno,"ingressiGiornalieriInIntensiva":ingressiPrimoGiornoTerapiaIntensiva,"ingressiGiornalieriFuoriIntensiva":ingressiOrdinariPrimoGiorno,"decedutiGiornalieri":decedutiPrimoGiorno})

	#AGGIUNGIAMO LE COLONNE RELATIVE AL DATO NAZIONALE. 
	#Mettiamo in ogni colonna lo stesso valore 21 volte, perché tutte le colonne dei Dataframe devono essere lunghe uguali
	covid19MappaPrimoGiorno["rapportoItalianoSuTamponiMolecolari"] = [rapportoPositiviTamponiPrimoGiornoInItalia for i in range(21)]
	covid19MappaPrimoGiorno["ingressiInIntensivaMediaRegionale"]= [ingressiPrimoGiornoTerapiaIntensivaMediaRegionale for i in range(21)]
	covid19MappaPrimoGiorno["ingressiInOspedaleNonIntensivaMediaRegionale"]= [ingressiOrdinariPrimoGiornoMediaRegionale for i in range(21)]
	covid19MappaPrimoGiorno["decedutiMediaRegionale"]= [decedutiPrimoGiornoMediaRegionale  for i in range(21)]

	#-----------------------------------COMMITT SU GITHUB DEL CSV PER IL PRIMO GIORNO-----------------------------
	d=covid19MappaPrimoGiorno.to_csv(sep=",",index=False)
	fileList=[d]
	
	#Il nome del file sarà una stringa del tipo Covid19-aaaa-mm-dd.csv
	listaGiornoMeseAnno=listaDate[0].split("-")
	fileNames=["Covid19-"+listaGiornoMeseAnno[2]+"-"+listaGiornoMeseAnno[1]+"-"+listaGiornoMeseAnno[0]+".csv"]

	commitMessage=dateImport.today().strftime("%d-%m-%Y")
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
	print("Aggiornamento giorno 0 completato")


	#----------------------------------------------------DATI FINO AL 14 GENNAIO 2021 COMPRESO ------------------------------------------------------------
	
	for i in range(1,listaDate.index("15-01-2021")):
		covid19UltimoGiorno=covid19[covid19["data"]==listaDate[i]]
		covid19PenultimoGiorno=covid19[covid19["data"]==listaDate[i-1]]

		#RAPPORTO TAMPONI MOLECOLARI
		tamponiEffettuatuUltimoGiorno=covid19UltimoGiorno["tamponi"]-covid19PenultimoGiorno["tamponi"]
		tamponiEffettuatuUltimoGiornoTotale=tamponiEffettuatuUltimoGiorno.sum()
		nuoviPositiviUltimoGiornoInItalia=covid19UltimoGiorno["nuovi_positivi"].sum()
		rapportoPositiviSuTotaleTamponiUltimoGiorno=covid19UltimoGiorno["nuovi_positivi"]*100/tamponiEffettuatuUltimoGiorno
		rapportoPositiviTamponiUltimoGiornoInItalia=nuoviPositiviUltimoGiornoInItalia*100/tamponiEffettuatuUltimoGiornoTotale

		#TERAPIA INTENSIVA
		ingressiUltimoGiornoTerapiaIntensiva=covid19UltimoGiorno["terapia_intensiva"]-covid19PenultimoGiorno["terapia_intensiva"]
		ingressiUltimoGiornoTerapiaIntensivaInItalia=ingressiUltimoGiornoTerapiaIntensiva.sum()
		

		#RICOVERI ORDINARE
		ingressiUltimoGiornoOspedaleCompresaTerapiaIntensiva=covid19UltimoGiorno["totale_ospedalizzati"]-covid19PenultimoGiorno["totale_ospedalizzati"]
		ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva=ingressiUltimoGiornoOspedaleCompresaTerapiaIntensiva-ingressiUltimoGiornoTerapiaIntensiva
		ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia=ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva.sum()
		
		#DECEDUTI
		decedutiUltimoGiorno=covid19UltimoGiorno["deceduti"]-covid19PenultimoGiorno["deceduti"]

		
		#----------------------------CREAZIONE DEI CSV FINO AL 14 GENNAIO INCLUSO--------------------------------
		regioni=covid19UltimoGiorno.index

		covid19Mappa=pd.DataFrame({"regione":regioni,"rapportoGiornalieroSuTamponiMolecolari":rapportoPositiviSuTotaleTamponiUltimoGiorno,"ingressiGiornalieriInIntensiva":ingressiUltimoGiornoTerapiaIntensiva,"ingressiGiornalieriFuoriIntensiva":ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva,"decedutiGiornalieri":decedutiUltimoGiorno})

		#AGGIUNGIAMO LE COLONNE RELATIVE AL DATO NAZIONALE.
		#Mettiamo in ogni colonna lo stesso valore 21 volte, perché tutte le colonne dei Dataframe devono essere lunghe uguali
		covid19Mappa["rapportoItalianoSuTamponiMolecolari"] = [rapportoPositiviTamponiUltimoGiornoInItalia for i in range(21)]
		covid19Mappa["ingressiInIntensivaMediaRegionale"]= [ingressiUltimoGiornoTerapiaIntensivaInItalia/21 for i in range(21)]
		covid19Mappa["ingressiInOspedaleNonIntensivaMediaRegionale"]= [ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia/21 for i in range(21)]
		covid19Mappa["decedutiMediaRegionale"]= [(decedutiUltimoGiorno.sum())/21  for i in range(21)]
		
		#------------------------------------COMMIT SU GITHUB DEI CSV FINO AL 14 GENNAIO---------------------------------
		d=covid19Mappa.to_csv(sep=",",index=False)
		fileList=[d]

		listaGiornoMeseAnno=listaDate[i].split("-")
		fileNames=["Covid19-"+listaGiornoMeseAnno[2]+"-"+listaGiornoMeseAnno[1]+"-"+listaGiornoMeseAnno[0]+".csv"]


		commitMessage=dateImport.today().strftime("%d-%m-%Y")
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

		print("Aggiornamento mappa giorno "+str(listaDate[i])+" completato")
	
	


	#-----------------------------------------GIORNO MISTO (15 gennaio 2021) -----------------------------
	covid19UltimoGiorno=covid19[covid19["data"]=="15-01-2021"]
	covid19PenultimoGiorno=covid19[covid19["data"]=="14-01-2021"]

	#TAMPONI TOTALI
	tamponiEffettuatuUltimoGiorno=covid19UltimoGiorno["tamponi"]-covid19PenultimoGiorno["tamponi"]
	tamponiEffettuatuUltimoGiornoTotale=tamponiEffettuatuUltimoGiorno.sum()
	nuoviPositiviUltimoGiornoInItalia=covid19UltimoGiorno["nuovi_positivi"].sum()
	rapportoPositiviSuTotaleTamponiUltimoGiorno=covid19UltimoGiorno["nuovi_positivi"]*100/tamponiEffettuatuUltimoGiorno
	rapportoPositiviTamponiUltimoGiornoInItalia=nuoviPositiviUltimoGiornoInItalia*100/tamponiEffettuatuUltimoGiornoTotale


	#TAMPONI MOLECOLARI
	tamponiMolecolariUltimoGiorno=covid19UltimoGiorno["tamponi_test_molecolare"]-covid19PenultimoGiorno["tamponi"]
	nuoviPositiviMolecolare=covid19UltimoGiorno["nuovi_positivi"]-covid19UltimoGiorno["totale_positivi_test_antigenico_rapido"]
	tassoPositiviMolecolari=nuoviPositiviMolecolare*100/tamponiMolecolariUltimoGiorno
	tassoNazionalePositiviMolecolari=nuoviPositiviMolecolare.sum()*100/tamponiMolecolariUltimoGiorno.sum()

	#TERAPIE INTENSIVE
	ingressiUltimoGiornoTerapiaIntensiva=covid19UltimoGiorno["terapia_intensiva"]-covid19PenultimoGiorno["terapia_intensiva"]
	ingressiUltimoGiornoTerapiaIntensivaInItalia=ingressiUltimoGiornoTerapiaIntensiva.sum()
	

	#RICOVERI ORDINARI
	ingressiUltimoGiornoOspedaleCompresaTerapiaIntensiva=covid19UltimoGiorno["totale_ospedalizzati"]-covid19PenultimoGiorno["totale_ospedalizzati"]
	ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva=ingressiUltimoGiornoOspedaleCompresaTerapiaIntensiva-ingressiUltimoGiornoTerapiaIntensiva
	ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia=ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva.sum()
	
	#DECEDUTI
	decedutiUltimoGiorno=covid19UltimoGiorno["deceduti"]-covid19PenultimoGiorno["deceduti"]


	#-----------------------------------------------GENERAZIONE CSV 15 GENNAIO-------------------------------------------

	regioni=covid19UltimoGiorno.index

	covid19Mappa=pd.DataFrame({"regione":regioni,"rapportoGiornalieroSuTamponiTotali":rapportoPositiviSuTotaleTamponiUltimoGiorno,"rapportoGiornalieroSuTamponiMolecolari":tassoPositiviMolecolari,"ingressiGiornalieriInIntensiva":ingressiUltimoGiornoTerapiaIntensiva,"ingressiGiornalieriFuoriIntensiva":ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva,"decedutiGiornalieri":decedutiUltimoGiorno})

	#AGGIUNGIAMO LE COLONNE RELATIVE AL DATO NAZIONALE. 
	#Mettiamo in ogni colonna lo stesso valore 21 volte, perché tutte le colonne dei Dataframe devono essere lunghe uguali
	covid19Mappa["rapportoItalianoSuTamponiTotali"]= [rapportoPositiviTamponiUltimoGiornoInItalia for i in range(21)]
	covid19Mappa["rapportoItalianoSuTamponiMolecolari"] = [tassoNazionalePositiviMolecolari for i in range(21)]
	covid19Mappa["ingressiInIntensivaMediaRegionale"]= [ingressiUltimoGiornoTerapiaIntensivaInItalia/21 for i in range(21)]
	covid19Mappa["ingressiInOspedaleNonIntensivaMediaRegionale"]= [ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia/21 for i in range(21)]
	covid19Mappa["decedutiMediaRegionale"]= [(decedutiUltimoGiorno.sum())/21  for i in range(21)]

	#--------------------------------------------COMMIT 15 GENNAIO SU GITHUB-----------------------------------------
	d=covid19Mappa.to_csv(sep=",",index=False)
	fileList=[d]

	listaGiornoMeseAnno="15-01-2021".split("-")
	fileNames=["Covid19-"+listaGiornoMeseAnno[2]+"-"+listaGiornoMeseAnno[1]+"-"+listaGiornoMeseAnno[0]+".csv"]

	commitMessage=dateImport.today().strftime("%d-%m-%Y")
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
	
	print("Aggiornamento mappa giorno misto completato")


	#-------------------------------------FOR FINALE (dal 16 gennaio in avanti)--------------------------------------------------

	for i in range(listaDate.index("15-01-2021")+1,quanteDateCiSonoState):
		covid19UltimoGiorno=covid19[covid19["data"]==listaDate[i]]
		covid19PenultimoGiorno=covid19[covid19["data"]==listaDate[i-1]]
	
		#TAMPONI TOTALI
		tamponiEffettuatuUltimoGiorno=covid19UltimoGiorno["tamponi"]-covid19PenultimoGiorno["tamponi"]
		tamponiEffettuatuUltimoGiornoTotale=tamponiEffettuatuUltimoGiorno.sum()
		nuoviPositiviUltimoGiornoInItalia=covid19UltimoGiorno["nuovi_positivi"].sum()
		rapportoPositiviSuTotaleTamponiUltimoGiorno=covid19UltimoGiorno["nuovi_positivi"]*100/tamponiEffettuatuUltimoGiorno
		rapportoPositiviTamponiUltimoGiornoInItalia=nuoviPositiviUltimoGiornoInItalia*100/tamponiEffettuatuUltimoGiornoTotale


		#TAMPONI MOLECOLARI
		tamponiMolecolariUltimoGiorno=covid19UltimoGiorno["tamponi_test_molecolare"]-covid19PenultimoGiorno["tamponi_test_molecolare"]
		nuoviPositiviMolecolare=covid19UltimoGiorno["totale_positivi_test_molecolare"]-covid19PenultimoGiorno["totale_positivi_test_molecolare"]
		tassoPositiviMolecolari=nuoviPositiviMolecolare*100/tamponiMolecolariUltimoGiorno
		tassoNazionalePositiviMolecolari=nuoviPositiviMolecolare.sum()*100/tamponiMolecolariUltimoGiorno.sum()

		#TERAPIE INTENSIVE
		ingressiUltimoGiornoTerapiaIntensiva=covid19UltimoGiorno["terapia_intensiva"]-covid19PenultimoGiorno["terapia_intensiva"]
		ingressiUltimoGiornoTerapiaIntensivaInItalia=ingressiUltimoGiornoTerapiaIntensiva.sum()

		#RICOVERI ORDINARI
		ingressiUltimoGiornoOspedaleCompresaTerapiaIntensiva=covid19UltimoGiorno["totale_ospedalizzati"]-covid19PenultimoGiorno["totale_ospedalizzati"]
		ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva=ingressiUltimoGiornoOspedaleCompresaTerapiaIntensiva-ingressiUltimoGiornoTerapiaIntensiva
		ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia=ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva.sum()
		
		#DECEDUTI
		decedutiUltimoGiorno=covid19UltimoGiorno["deceduti"]-covid19PenultimoGiorno["deceduti"]

		#------------------------GENERAZIONE CSV PER LE GIORNATE DAL 16 GENNAIO AD OGGI-----------------------------
		regioni=covid19UltimoGiorno.index
		covid19Mappa=pd.DataFrame({"regione":regioni,"rapportoGiornalieroSuTamponiTotali":rapportoPositiviSuTotaleTamponiUltimoGiorno,"rapportoGiornalieroSuTamponiMolecolari":tassoPositiviMolecolari,"ingressiGiornalieriInIntensiva":ingressiUltimoGiornoTerapiaIntensiva,"ingressiGiornalieriFuoriIntensiva":ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva,"decedutiGiornalieri":decedutiUltimoGiorno})

		#AGGIUNGIAMO LE COLONNE RELATIVE AL DATO NAZIONALE.
		#Mettiamo in ogni colonna lo stesso valore 21 volte, perché tutte le colonne dei Dataframe devono essere lunghe uguali
		covid19Mappa["rapportoItalianoSuTamponiTotali"]= [rapportoPositiviTamponiUltimoGiornoInItalia for i in range(21)]
		covid19Mappa["rapportoItalianoSuTamponiMolecolari"] = [tassoNazionalePositiviMolecolari for i in range(21)]
		covid19Mappa["ingressiInIntensivaMediaRegionale"]= [ingressiUltimoGiornoTerapiaIntensivaInItalia/21 for i in range(21)]
		covid19Mappa["ingressiInOspedaleNonIntensivaMediaRegionale"]= [ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia/21 for i in range(21)]
		covid19Mappa["decedutiMediaRegionale"]= [(decedutiUltimoGiorno.sum())/21  for i in range(21)]

		#-----------------------------------------COMMIT SU GITHUB CSV DAL 16 GENNAIO AD OGGI-----------------------
		d=covid19Mappa.to_csv(sep=",",index=False)
		fileList=[d]

		listaGiornoMeseAnno=listaDate[i].split("-")
		fileNames=["Covid19-"+listaGiornoMeseAnno[2]+"-"+listaGiornoMeseAnno[1]+"-"+listaGiornoMeseAnno[0]+".csv"]
		commitMessage=dateImport.today().strftime("%d-%m-%Y")
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
		
		print("Aggiornamento mappa giorno "+str(listaDate[i])+" completato")
	
	

