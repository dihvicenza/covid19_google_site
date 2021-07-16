import pandas as pd
#import matplotlib.pyplot as plt
import os
from os import environ

import datetime
from datetime import date as dateImport
pd.options.mode.chained_assignment = None
from github import Github, InputGitTreeElement
from datetime import date as dateImport


def mappa():


	covid19 = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv",sep=",")

	covid19['data']=(pd.to_datetime(covid19["data"]))
	covid19=covid19.fillna(0)
	#print (covid19.info())
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



	#ultimoGiorno=date[-1]
	#penultimoGiorno=date[-22]
	#covid19UltimoGiorno=covid19[covid19["data"]==ultimoGiorno]
	#covid19PenultimoGiorno=covid19[covid19["data"]==penultimoGiorno]


	#-----------------------------------------Primo giorno---------------------------------------
	covid19PrimoGiorno=covid19[covid19["data"]==date[0]]

	#---------------Tamponi molecolari primo giorno-------------
	tamponiEffettuatiPrimoGiorno=covid19PrimoGiorno["tamponi"]
	tamponiEffettuatiPrimoGiornoTotale=tamponiEffettuatiPrimoGiorno.sum()
	nuoviPositiviPrimoGiornoInItalia=covid19PrimoGiorno["nuovi_positivi"].sum()
	rapportoPositiviSuTamponiMolecolariPrimoGiorno=covid19PrimoGiorno["nuovi_positivi"]*100/tamponiEffettuatiPrimoGiorno
	rapportoPositiviTamponiPrimoGiornoInItalia=nuoviPositiviPrimoGiornoInItalia*100/tamponiEffettuatiPrimoGiornoTotale

	#---------------terapie intensive primo giorno-------------
	ingressiPrimoGiornoTerapiaIntensiva=covid19PrimoGiorno["terapia_intensiva"]
	ingressiPrimoGiornoTerapiaIntensivaMediaRegionale=ingressiPrimoGiornoTerapiaIntensiva.sum()/21
	 
	#---------------ricoveri ordinari primo giorno-------------
	ingressiOrdinariPrimoGiorno=covid19PrimoGiorno["ricoverati_con_sintomi"]
	ingressiOrdinariPrimoGiornoMediaRegionale=ingressiOrdinariPrimoGiorno.sum()/21

	#-------------------deceduti primo giorno----------------
	decedutiPrimoGiorno=covid19PrimoGiorno["deceduti"]
	decedutiPrimoGiornoMediaRegionale=decedutiPrimoGiorno.sum()/21


	#-----------------creazione csv primo giorno------------
	regioni=covid19PrimoGiorno.index

	covid19MappaPrimoGiorno=pd.DataFrame({"regione":regioni,"rapportoGiornalieroSuTamponiMolecolari":rapportoPositiviSuTamponiMolecolariPrimoGiorno,"ingressiGiornalieriInIntensiva":ingressiPrimoGiornoTerapiaIntensiva,"ingressiGiornalieriFuoriIntensiva":ingressiOrdinariPrimoGiorno,"decedutiGiornalieri":decedutiPrimoGiorno})

	#AGGIUNGIAMO LE COLONNE RELATIVE AL DATO NAZIONALE. Mettiamo in ogni colonna lo stesso valore 21 volte, perché tutte le colonne dei Dataframe devono essere lunghe uguali
	
	covid19MappaPrimoGiorno["rapportoItalianoSuTamponiMolecolari"] = [rapportoPositiviTamponiPrimoGiornoInItalia for i in range(21)]
	covid19MappaPrimoGiorno["ingressiInIntensivaMediaRegionale"]= [ingressiPrimoGiornoTerapiaIntensivaMediaRegionale for i in range(21)]
	covid19MappaPrimoGiorno["ingressiInOspedaleNonIntensivaMediaRegionale"]= [ingressiOrdinariPrimoGiornoMediaRegionale for i in range(21)]
	covid19MappaPrimoGiorno["decedutiMediaRegionale"]= [decedutiPrimoGiornoMediaRegionale  for i in range(21)]


	d=covid19MappaPrimoGiorno.to_csv(sep=",",index=False)
	fileList=[d]

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



	#-------------------------------For sino al 15 gennaio------------------------
	
	for i in range(1,listaDate.index("15-01-2021")):
		covid19UltimoGiorno=covid19[covid19["data"]==listaDate[i]]
		covid19PenultimoGiorno=covid19[covid19["data"]==listaDate[i-1]]

		#Rapporto positivi su  tamponi molecolari ultimo giorno
		tamponiEffettuatuUltimoGiorno=covid19UltimoGiorno["tamponi"]-covid19PenultimoGiorno["tamponi"]
		tamponiEffettuatuUltimoGiornoTotale=tamponiEffettuatuUltimoGiorno.sum()
		nuoviPositiviUltimoGiornoInItalia=covid19UltimoGiorno["nuovi_positivi"].sum()
		rapportoPositiviSuTotaleTamponiUltimoGiorno=covid19UltimoGiorno["nuovi_positivi"]*100/tamponiEffettuatuUltimoGiorno
		rapportoPositiviTamponiUltimoGiornoInItalia=nuoviPositiviUltimoGiornoInItalia*100/tamponiEffettuatuUltimoGiornoTotale

		#Ingressi ultimo giorno in terapia intensiva
		ingressiUltimoGiornoTerapiaIntensiva=covid19UltimoGiorno["terapia_intensiva"]-covid19PenultimoGiorno["terapia_intensiva"]
		ingressiUltimoGiornoTerapiaIntensivaInItalia=ingressiUltimoGiornoTerapiaIntensiva.sum()
		

		#Ingressi ospedalieri ultimo giorno NON in terapia intensiva
		ingressiUltimoGiornoOspedaleCompresaTerapiaIntensiva=covid19UltimoGiorno["totale_ospedalizzati"]-covid19PenultimoGiorno["totale_ospedalizzati"]
		ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva=ingressiUltimoGiornoOspedaleCompresaTerapiaIntensiva-ingressiUltimoGiornoTerapiaIntensiva
		ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia=ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva.sum()
		
		#Morti ultimo giorno
		decedutiUltimoGiorno=covid19UltimoGiorno["deceduti"]-covid19PenultimoGiorno["deceduti"]

		
		#---------Creazione e push csv -------------------
		regioni=covid19UltimoGiorno.index

		covid19Mappa=pd.DataFrame({"regione":regioni,"rapportoGiornalieroSuTamponiMolecolari":rapportoPositiviSuTotaleTamponiUltimoGiorno,"ingressiGiornalieriInIntensiva":ingressiUltimoGiornoTerapiaIntensiva,"ingressiGiornalieriFuoriIntensiva":ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva,"decedutiGiornalieri":decedutiUltimoGiorno})

		#AGGIUNGIAMO LE COLONNE RELATIVE AL DATO NAZIONALE. Mettiamo in ogni colonna lo stesso valore 21 volte, perché tutte le colonne dei Dataframe devono essere lunghe uguali
		
		covid19Mappa["rapportoItalianoSuTamponiMolecolari"] = [rapportoPositiviTamponiUltimoGiornoInItalia for i in range(21)]
		covid19Mappa["ingressiInIntensivaMediaRegionale"]= [ingressiUltimoGiornoTerapiaIntensivaInItalia/21 for i in range(21)]
		covid19Mappa["ingressiInOspedaleNonIntensivaMediaRegionale"]= [ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia/21 for i in range(21)]
		covid19Mappa["decedutiMediaRegionale"]= [(decedutiUltimoGiorno.sum())/21  for i in range(21)]


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
	
	


	#----------------------------Giorno misto (15 gennaio 2021) -----------------------------
	covid19UltimoGiorno=covid19[covid19["data"]=="15-01-2021"]
	covid19PenultimoGiorno=covid19[covid19["data"]=="14-01-2021"]

	#Rapporto positivi su totale tamponi effettuati ultimo giorno
	tamponiEffettuatuUltimoGiorno=covid19UltimoGiorno["tamponi"]-covid19PenultimoGiorno["tamponi"]
	tamponiEffettuatuUltimoGiornoTotale=tamponiEffettuatuUltimoGiorno.sum()
	nuoviPositiviUltimoGiornoInItalia=covid19UltimoGiorno["nuovi_positivi"].sum()
	rapportoPositiviSuTotaleTamponiUltimoGiorno=covid19UltimoGiorno["nuovi_positivi"]*100/tamponiEffettuatuUltimoGiorno
	rapportoPositiviTamponiUltimoGiornoInItalia=nuoviPositiviUltimoGiornoInItalia*100/tamponiEffettuatuUltimoGiornoTotale


	#Rapporto positivi su tamponi molecolari ultimo giorno
	tamponiMolecolariUltimoGiorno=covid19UltimoGiorno["tamponi_test_molecolare"]-covid19PenultimoGiorno["tamponi"]
	nuoviPositiviMolecolare=covid19UltimoGiorno["nuovi_positivi"]-covid19UltimoGiorno["totale_positivi_test_antigenico_rapido"]
	tassoPositiviMolecolari=nuoviPositiviMolecolare*100/tamponiMolecolariUltimoGiorno
	tassoNazionalePositiviMolecolari=nuoviPositiviMolecolare.sum()*100/tamponiMolecolariUltimoGiorno.sum()

	#Ingressi ultimo giorno in terapia intensiva
	ingressiUltimoGiornoTerapiaIntensiva=covid19UltimoGiorno["terapia_intensiva"]-covid19PenultimoGiorno["terapia_intensiva"]
	ingressiUltimoGiornoTerapiaIntensivaInItalia=ingressiUltimoGiornoTerapiaIntensiva.sum()
	

	#Ingressi ospedalieri ultimo giorno NON in terapia intensiva
	ingressiUltimoGiornoOspedaleCompresaTerapiaIntensiva=covid19UltimoGiorno["totale_ospedalizzati"]-covid19PenultimoGiorno["totale_ospedalizzati"]
	ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva=ingressiUltimoGiornoOspedaleCompresaTerapiaIntensiva-ingressiUltimoGiornoTerapiaIntensiva
	ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia=ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva.sum()
	
	#Morti ultimo giorno
	decedutiUltimoGiorno=covid19UltimoGiorno["deceduti"]-covid19PenultimoGiorno["deceduti"]


	#-------Generiamo e pushiamo il csv del giorno misto-----

	regioni=covid19UltimoGiorno.index

	covid19Mappa=pd.DataFrame({"regione":regioni,"rapportoGiornalieroSuTamponiTotali":rapportoPositiviSuTotaleTamponiUltimoGiorno,"rapportoGiornalieroSuTamponiMolecolari":tassoPositiviMolecolari,"ingressiGiornalieriInIntensiva":ingressiUltimoGiornoTerapiaIntensiva,"ingressiGiornalieriFuoriIntensiva":ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva,"decedutiGiornalieri":decedutiUltimoGiorno})

	#AGGIUNGIAMO LE COLONNE RELATIVE AL DATO NAZIONALE. Mettiamo in ogni colonna lo stesso valore 21 volte, perché tutte le colonne dei Dataframe devono essere lunghe uguali
	covid19Mappa["rapportoItalianoSuTamponiTotali"]= [rapportoPositiviTamponiUltimoGiornoInItalia for i in range(21)]
	covid19Mappa["rapportoItalianoSuTamponiMolecolari"] = [tassoNazionalePositiviMolecolari for i in range(21)]
	covid19Mappa["ingressiInIntensivaMediaRegionale"]= [ingressiUltimoGiornoTerapiaIntensivaInItalia/21 for i in range(21)]
	covid19Mappa["ingressiInOspedaleNonIntensivaMediaRegionale"]= [ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia/21 for i in range(21)]
	covid19Mappa["decedutiMediaRegionale"]= [(decedutiUltimoGiorno.sum())/21  for i in range(21)]


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





	#-------------------for finale (dal 16 gennaio in avanti)------------------------


	for i in range(listaDate.index("15-01-2021")+1,quanteDateCiSonoState):
		covid19UltimoGiorno=covid19[covid19["data"]==listaDate[i]]
		covid19PenultimoGiorno=covid19[covid19["data"]==listaDate[i-1]]
	
		#Rapporto positivi su totale tamponi effettuati ultimo giorno
		tamponiEffettuatuUltimoGiorno=covid19UltimoGiorno["tamponi"]-covid19PenultimoGiorno["tamponi"]
		tamponiEffettuatuUltimoGiornoTotale=tamponiEffettuatuUltimoGiorno.sum()
		nuoviPositiviUltimoGiornoInItalia=covid19UltimoGiorno["nuovi_positivi"].sum()
		rapportoPositiviSuTotaleTamponiUltimoGiorno=covid19UltimoGiorno["nuovi_positivi"]*100/tamponiEffettuatuUltimoGiorno
		rapportoPositiviTamponiUltimoGiornoInItalia=nuoviPositiviUltimoGiornoInItalia*100/tamponiEffettuatuUltimoGiornoTotale


		#Rapporto positivi su tamponi molecolari ultimo giorno
		tamponiMolecolariUltimoGiorno=covid19UltimoGiorno["tamponi_test_molecolare"]-covid19PenultimoGiorno["tamponi_test_molecolare"]
		nuoviPositiviMolecolare=covid19UltimoGiorno["totale_positivi_test_molecolare"]-covid19PenultimoGiorno["totale_positivi_test_molecolare"]
		tassoPositiviMolecolari=nuoviPositiviMolecolare*100/tamponiMolecolariUltimoGiorno
		tassoNazionalePositiviMolecolari=nuoviPositiviMolecolare.sum()*100/tamponiMolecolariUltimoGiorno.sum()




		#Ingressi ultimo giorno in terapia intensiva
		ingressiUltimoGiornoTerapiaIntensiva=covid19UltimoGiorno["terapia_intensiva"]-covid19PenultimoGiorno["terapia_intensiva"]
		ingressiUltimoGiornoTerapiaIntensivaInItalia=ingressiUltimoGiornoTerapiaIntensiva.sum()
		

		#Ingressi ospedalieri ultimo giorno NON in terapia intensiva
		ingressiUltimoGiornoOspedaleCompresaTerapiaIntensiva=covid19UltimoGiorno["totale_ospedalizzati"]-covid19PenultimoGiorno["totale_ospedalizzati"]
		ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva=ingressiUltimoGiornoOspedaleCompresaTerapiaIntensiva-ingressiUltimoGiornoTerapiaIntensiva
		ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia=ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva.sum()
		
		#Morti ultimo giorno
		decedutiUltimoGiorno=covid19UltimoGiorno["deceduti"]-covid19PenultimoGiorno["deceduti"]


		#Generazione e push dei csv

		regioni=covid19UltimoGiorno.index

		covid19Mappa=pd.DataFrame({"regione":regioni,"rapportoGiornalieroSuTamponiTotali":rapportoPositiviSuTotaleTamponiUltimoGiorno,"rapportoGiornalieroSuTamponiMolecolari":tassoPositiviMolecolari,"ingressiGiornalieriInIntensiva":ingressiUltimoGiornoTerapiaIntensiva,"ingressiGiornalieriFuoriIntensiva":ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva,"decedutiGiornalieri":decedutiUltimoGiorno})

		#AGGIUNGIAMO LE COLONNE RELATIVE AL DATO NAZIONALE. Mettiamo in ogni colonna lo stesso valore 21 volte, perché tutte le colonne dei Dataframe devono essere lunghe uguali
		covid19Mappa["rapportoItalianoSuTamponiTotali"]= [rapportoPositiviTamponiUltimoGiornoInItalia for i in range(21)]
		covid19Mappa["rapportoItalianoSuTamponiMolecolari"] = [tassoNazionalePositiviMolecolari for i in range(21)]
		covid19Mappa["ingressiInIntensivaMediaRegionale"]= [ingressiUltimoGiornoTerapiaIntensivaInItalia/21 for i in range(21)]
		covid19Mappa["ingressiInOspedaleNonIntensivaMediaRegionale"]= [ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia/21 for i in range(21)]
		covid19Mappa["decedutiMediaRegionale"]= [(decedutiUltimoGiorno.sum())/21  for i in range(21)]


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
	
	

