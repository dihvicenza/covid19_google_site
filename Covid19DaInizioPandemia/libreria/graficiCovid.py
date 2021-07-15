#Ora facciamo i grafici dei valori giornalieri giorno dopo giorno da inizio pandemia
import math
import pandas as pd
pd.options.mode.chained_assignment = None

from libreria.numeroDiAbitanti import *
from libreria.graficiCovidRegionePerRegione import *

from github import Github, InputGitTreeElement
from datetime import date as dateImport
from os import environ



def graficiGiornalieri():

	covid19 = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv",sep=",")
	covid19['data']=(pd.to_datetime(covid19["data"]))
	covid19=covid19.fillna(0)
	listaDate1=list(pd.to_datetime(covid19["data"]))
	listaDate=[listaDate1[i].strftime("%d-%m-%Y") for i in range(len(listaDate1))]

	covid19["data"]=listaDate.copy()
	covid19.drop(["stato","codice_regione","lat","long","codice_nuts_1", "codice_nuts_2","note","note_test","note_casi"], axis=1, inplace=True)
	covid19.set_index("denominazione_regione",inplace=True)
	
	#Prendiamo tutte le date da inizio pandemia
	date=covid19["data"]
	quanteDateCiSonoState=len(listaDate)//21
	listaDate=[]

	listaDate=[date[-21*i-1] for i in range(quanteDateCiSonoState-1,-1,-1)]

	listaRegioni=["Abruzzo","Basilicata","Calabria","Campania","Emilia-Romagna","Friuli Venezia Giulia","Lazio","Liguria","Lombardia","Marche","Molise","P.A. Bolzano","P.A. Trento","Piemonte","Puglia","Sardegna","Sicilia","Toscana","Umbria","Valle d'Aosta"]

	covid19PrimoGiorno=covid19[covid19["data"]==listaDate[0]]

	#TAMPONI MOLECOLARI
	rapportoPositiviSuTamponiMolecolariGiornalieri=[]
	rapportoPositiviSuTamponiMolecolariGiornalieriInVeneto=[]
	tamponiMolecolariPrimoGiorno=covid19PrimoGiorno["tamponi"]
	tamponiMolecolariPrimoGiornoInVeneto=tamponiMolecolariPrimoGiorno["Veneto"]
	nuoviPositiviMolecolariPrimoGiorno=covid19PrimoGiorno["nuovi_positivi"]
	nuoviPositiviMolecolariPrimoGiornoInVeneto=nuoviPositiviMolecolariPrimoGiorno["Veneto"]
	tassoPositiviSuTamponiMolecolariPrimoGiorno=nuoviPositiviMolecolariPrimoGiorno.sum()*100/tamponiMolecolariPrimoGiorno.sum()
	tassoPositiviSuTamponiMolecolariPrimoGiornoInVeneto=nuoviPositiviMolecolariPrimoGiornoInVeneto*100/tamponiMolecolariPrimoGiornoInVeneto
	rapportoPositiviSuTamponiMolecolariGiornalieri.append(tassoPositiviSuTamponiMolecolariPrimoGiorno)
	rapportoPositiviSuTamponiMolecolariGiornalieriInVeneto.append(tassoPositiviSuTamponiMolecolariPrimoGiornoInVeneto)

	#POSITIVI SU TAMPONI TOTALI
	rapportoPositiviSuTotaleTamponiGiornalieri=[]
	rapportoPositiviSuTotaleTamponiGiornalieriInVeneto=[]

	#INGRESSI GIORNALIERI IN TERAPIA INTENSIVA
	ingressiIntensivaGiornalieri=[]
	ingressiIntensivaGiornalieriInVeneto=[]
	ingressiPrimoGiornoTerapiaIntensiva=covid19PrimoGiorno["terapia_intensiva"]
	ingressiPrimoGiornoTerapiaIntensivaInVeneto=ingressiPrimoGiornoTerapiaIntensiva["Veneto"]
	ingressiPrimoGiornoTerapiaIntensivaInItalia=ingressiPrimoGiornoTerapiaIntensiva.sum()
	ingressiIntensivaGiornalieri.append(ingressiPrimoGiornoTerapiaIntensivaInItalia)
	ingressiIntensivaGiornalieriInVeneto.append(ingressiPrimoGiornoTerapiaIntensivaInVeneto*moltiplicatore)

	#INGRESSI GIORNALIERI NON IN TERAPIA INTENSIVA
	ingressiNonIntensivaGiornalieri=[]
	ingressiNonIntensivaGiornalieriInVeneto=[]
	ingressiOspedaleSenzaTerapiaIntensivaPrimoGiorno=covid19PrimoGiorno["ricoverati_con_sintomi"]
	ingressiNonIntensivaPrimoGiornoInVeneto=ingressiOspedaleSenzaTerapiaIntensivaPrimoGiorno["Veneto"]
	ingressiNonIntensivaPrimoGiornoInItalia=ingressiOspedaleSenzaTerapiaIntensivaPrimoGiorno.sum()
	ingressiNonIntensivaGiornalieri.append(ingressiNonIntensivaPrimoGiornoInItalia)
	ingressiNonIntensivaGiornalieriInVeneto.append(ingressiNonIntensivaPrimoGiornoInVeneto*moltiplicatore)

	#DECEDUTI SUPPONENDO CHE IL VENETO ABBIA LO STESSO NUMERO DI ABITANTI DELL'ITALIA
	deceduti=[]
	decedutiInVeneto=[]
	decedutiPrimoGiorno=covid19PrimoGiorno["deceduti"]
	decedutiPrimoGiornoInVeneto=decedutiPrimoGiorno["Veneto"]
	decedutiPrimoGiornoInItalia=decedutiPrimoGiorno.sum()
	decedutiInVeneto.append(decedutiPrimoGiornoInVeneto*moltiplicatore)
	deceduti.append(decedutiPrimoGiornoInItalia)

	#LETALITA
	letalita=[]
	letalitaInVeneto=[]
	tassoDiMortalitaPrimoGiorno=covid19PrimoGiorno["deceduti"]*100/covid19PrimoGiorno["totale_casi"]
	tassoDiMortalitaPrimoGiornoInVeneto=tassoDiMortalitaPrimoGiorno["Veneto"]
	tassoDiMortalitaNazionalePrimoGiorno=covid19PrimoGiorno["deceduti"].sum()*100/covid19PrimoGiorno["totale_casi"].sum()
	letalitaInVeneto.append(tassoDiMortalitaPrimoGiornoInVeneto)
	letalita.append(tassoDiMortalitaNazionalePrimoGiorno)


	#-----------------------------FINO AL 15 GENNAIO---------------------------------
	for i in range(1,listaDate.index("15-01-2021")):
		covid19UltimoGiorno=covid19[covid19["data"]==listaDate[i]]
		covid19PenultimoGiorno=covid19[covid19["data"]==listaDate[i-1]]

		#TAMPONI MOLECOLARI
		tamponiMolecolariEffettuatuUltimoGiorno=covid19UltimoGiorno["tamponi"]-covid19PenultimoGiorno["tamponi"]
		tamponiMolecolariEffettuatuUltimoGiornoInVeneto=tamponiMolecolariEffettuatuUltimoGiorno["Veneto"]
		tamponiMolecolariEffettuatuUltimoGiornoTotale=tamponiMolecolariEffettuatuUltimoGiorno.sum()
		nuoviPositiviMolecolariUltimoGiorno=covid19UltimoGiorno["nuovi_positivi"]
		nuoviPositiviMolecolariUltimoGiornoInVeneto=nuoviPositiviMolecolariUltimoGiorno["Veneto"]
		nuoviPositiviMolecolariUltimoGiornoInItalia=nuoviPositiviMolecolariUltimoGiorno.sum()
		tassoPositiviSuTamponiMolecolariGiornalieri=nuoviPositiviMolecolariUltimoGiornoInItalia*100/tamponiMolecolariEffettuatuUltimoGiornoTotale
		tassoPositiviSuTamponiMolecolariGiornalieriInVeneto=nuoviPositiviMolecolariUltimoGiornoInVeneto*100/tamponiMolecolariEffettuatuUltimoGiornoInVeneto
		rapportoPositiviSuTamponiMolecolariGiornalieriInVeneto.append(tassoPositiviSuTamponiMolecolariGiornalieriInVeneto)
		rapportoPositiviSuTamponiMolecolariGiornalieri.append(tassoPositiviSuTamponiMolecolariGiornalieri)

		#TERAPIA INTENSIVA
		ingressiUltimoGiornoTerapiaIntensiva=covid19UltimoGiorno["terapia_intensiva"]-covid19PenultimoGiorno["terapia_intensiva"]
		ingressiUltimoGiornoTerapiaIntensivaInVeneto=ingressiUltimoGiornoTerapiaIntensiva["Veneto"]
		ingressiUltimoGiornoTerapiaIntensivaInItalia=ingressiUltimoGiornoTerapiaIntensiva.sum()
		ingressiIntensivaGiornalieri.append(ingressiUltimoGiornoTerapiaIntensivaInItalia)
		ingressiIntensivaGiornalieriInVeneto.append(ingressiUltimoGiornoTerapiaIntensivaInVeneto*moltiplicatore)

		#OSPEDALIZZATI
		ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva=covid19UltimoGiorno["ricoverati_con_sintomi"]-covid19PenultimoGiorno["ricoverati_con_sintomi"]
		ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInVeneto=ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva["Veneto"]
		ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia=ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva.sum()
		ingressiNonIntensivaGiornalieriInVeneto.append(ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInVeneto*moltiplicatore)
		ingressiNonIntensivaGiornalieri.append(ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia)
		
		#DECEDUTI
		decedutiUltimoGiornoInVeneto=(covid19UltimoGiorno["deceduti"]-covid19PenultimoGiorno["deceduti"])["Veneto"]
		decedutiUltimoGiorno=covid19UltimoGiorno["deceduti"].sum()-covid19PenultimoGiorno["deceduti"].sum()
		deceduti.append(decedutiUltimoGiorno)
		decedutiInVeneto.append(decedutiUltimoGiornoInVeneto*moltiplicatore)

		#LETALITà
		tassoDiMortalita=covid19UltimoGiorno["deceduti"]*100/covid19UltimoGiorno["totale_casi"]
		tassoDiMortalitaInVeneto=tassoDiMortalita["Veneto"]
		tassoDiMortalitaNazionale=covid19UltimoGiorno["deceduti"].sum()*100/covid19UltimoGiorno["totale_casi"].sum()
		letalitaInVeneto.append(tassoDiMortalitaInVeneto)
		letalita.append(tassoDiMortalitaNazionale)


	#Calcoliamo la percentuale del giorno 15/01. Data nella quale è cambiato il modo di ragionare sui tamponi
	covid19UltimoGiorno=covid19[covid19["data"]=="15-01-2021"]
	covid19PenultimoGiorno=covid19[covid19["data"]=="14-01-2021"]
	tamponiMolecolariUltimoGiorno=covid19UltimoGiorno["tamponi_test_molecolare"]-covid19PenultimoGiorno["tamponi"]
	tamponiMolecolariUltimoGiornoInVeneto=tamponiMolecolariUltimoGiorno["Veneto"]
	tamponiMolecolariUltimoGiornoInItalia=tamponiMolecolariUltimoGiorno.sum()
	positiviMolecolariUltimoGiorno=covid19UltimoGiorno["nuovi_positivi"]-covid19UltimoGiorno["totale_positivi_test_antigenico_rapido"]
	positiviMolecolariUltimoGiornoInVeneto=positiviMolecolariUltimoGiorno["Veneto"]
	positiviMolecolariUltimoGiornoInItalia=positiviMolecolariUltimoGiorno.sum()
	tassoPositiviMolecolariInVeneto=positiviMolecolariUltimoGiornoInVeneto*100/tamponiMolecolariUltimoGiornoInVeneto
	tassoPositiviMolecolariInItalia=positiviMolecolariUltimoGiornoInItalia*100/tamponiMolecolariUltimoGiornoInItalia
	rapportoPositiviSuTamponiMolecolariGiornalieriInVeneto.append(tassoPositiviMolecolariInVeneto)
	rapportoPositiviSuTamponiMolecolariGiornalieri.append(tassoPositiviMolecolariInItalia)

	#TAMPONI TOTALI
	tamponiEffettuatuUltimoGiorno=covid19UltimoGiorno["tamponi"]-covid19PenultimoGiorno["tamponi"]
	tamponiEffettuatuUltimoGiornoInVeneto=tamponiEffettuatuUltimoGiorno["Veneto"]
	tamponiEffettuatuUltimoGiornoTotale=tamponiEffettuatuUltimoGiorno.sum()
	nuoviPositiviUltimoGiorno=covid19UltimoGiorno["nuovi_positivi"]
	nuoviPositiviUltimoGiornoInVeneto=nuoviPositiviUltimoGiorno["Veneto"]
	nuoviPositiviUltimoGiornoInItalia=nuoviPositiviUltimoGiorno.sum()
	rapportoPositiviSuTotaleTamponiUltimoGiorno=nuoviPositiviUltimoGiorno*100/tamponiEffettuatuUltimoGiorno
	rapportoPositiviSuTotaleTamponiUltimoGiornoInVeneto=rapportoPositiviSuTotaleTamponiUltimoGiorno["Veneto"]
	rapportoPositiviSuTotaleTamponiGiornalieriInVeneto.append(rapportoPositiviSuTotaleTamponiUltimoGiornoInVeneto)
	covid19UltimoGiorno["ultimo_giorno_rapporto_positivi_tamponi"]=rapportoPositiviSuTotaleTamponiUltimoGiorno
	rapportoPositiviTamponiUltimoGiornoInItalia=nuoviPositiviUltimoGiornoInItalia*100/tamponiEffettuatuUltimoGiornoTotale
	rapportoPositiviSuTotaleTamponiGiornalieri.append(rapportoPositiviTamponiUltimoGiornoInItalia)

	#TERAPIA INTENSIVA
	ingressiUltimoGiornoTerapiaIntensiva=covid19UltimoGiorno["terapia_intensiva"]-covid19PenultimoGiorno["terapia_intensiva"]
	ingressiUltimoGiornoTerapiaIntensivaInVeneto=ingressiUltimoGiornoTerapiaIntensiva["Veneto"]
	ingressiUltimoGiornoTerapiaIntensivaInItalia=ingressiUltimoGiornoTerapiaIntensiva.sum()
	ingressiIntensivaGiornalieri.append(ingressiUltimoGiornoTerapiaIntensivaInItalia)
	ingressiIntensivaGiornalieriInVeneto.append(ingressiUltimoGiornoTerapiaIntensivaInVeneto*moltiplicatore)

	#OSPEDALIZZATI
	ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva=covid19UltimoGiorno["ricoverati_con_sintomi"]-covid19PenultimoGiorno["ricoverati_con_sintomi"]
	ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInVeneto=ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva["Veneto"]
	ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia=ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva.sum()
	ingressiNonIntensivaGiornalieriInVeneto.append(ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInVeneto*moltiplicatore)
	ingressiNonIntensivaGiornalieri.append(ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia)
	
	#DECEDUTI
	decedutiUltimoGiornoInVeneto=(covid19UltimoGiorno["deceduti"]-covid19PenultimoGiorno["deceduti"])["Veneto"]
	decedutiUltimoGiorno=covid19UltimoGiorno["deceduti"].sum()-covid19PenultimoGiorno["deceduti"].sum()
	deceduti.append(decedutiUltimoGiorno)
	decedutiInVeneto.append(decedutiUltimoGiornoInVeneto*moltiplicatore)

	#LETALITà
	tassoDiMortalita=covid19UltimoGiorno["deceduti"]*100/covid19UltimoGiorno["totale_casi"]
	tassoDiMortalitaInVeneto=tassoDiMortalita["Veneto"]
	tassoDiMortalitaNazionale=covid19UltimoGiorno["deceduti"].sum()*100/covid19UltimoGiorno["totale_casi"].sum()
	letalitaInVeneto.append(tassoDiMortalitaInVeneto)
	letalita.append(tassoDiMortalitaNazionale)


	#-------------------DAL 15 GENNAIO IN POI-------------------------
	for i in range(listaDate.index("15-01-2021")+1,quanteDateCiSonoState):
		covid19UltimoGiorno=covid19[covid19["data"]==listaDate[i]]
		covid19PenultimoGiorno=covid19[covid19["data"]==listaDate[i-1]]

		#TAMPONI MOLECOLARI
		tamponiMolecolariUltimoGiorno=covid19UltimoGiorno["tamponi_test_molecolare"]-covid19PenultimoGiorno["tamponi_test_molecolare"]
		tamponiMolecolariUltimoGiornoInVeneto=tamponiMolecolariUltimoGiorno["Veneto"]
		nuoviPositiviMolecolare=covid19UltimoGiorno["totale_positivi_test_molecolare"]-covid19PenultimoGiorno["totale_positivi_test_molecolare"]
		nuoviPositiviMolecolareInVeneto=nuoviPositiviMolecolare["Veneto"]
		tassoPositiviMolecolari=nuoviPositiviMolecolare*100/tamponiMolecolariUltimoGiorno
		tassoPositiviMolecolariInVeneto=nuoviPositiviMolecolareInVeneto*100/tamponiMolecolariUltimoGiornoInVeneto
		tassoNazionalePositiviMolecolari=nuoviPositiviMolecolare.sum()*100/tamponiMolecolariUltimoGiorno.sum()
		rapportoPositiviSuTamponiMolecolariGiornalieri.append(tassoNazionalePositiviMolecolari)
		rapportoPositiviSuTamponiMolecolariGiornalieriInVeneto.append(tassoPositiviMolecolariInVeneto)

		#TAMPONI TOTALI
		tamponiEffettuatuUltimoGiorno=covid19UltimoGiorno["tamponi"]-covid19PenultimoGiorno["tamponi"]
		tamponiEffettuatuUltimoGiornoInVeneto=tamponiEffettuatuUltimoGiorno["Veneto"]
		tamponiEffettuatuUltimoGiornoTotale=tamponiEffettuatuUltimoGiorno.sum()
		nuoviPositiviUltimoGiorno=covid19UltimoGiorno["nuovi_positivi"]
		nuoviPositiviUltimoGiornoInVeneto=nuoviPositiviUltimoGiorno["Veneto"]
		nuoviPositiviUltimoGiornoInItalia=nuoviPositiviUltimoGiorno.sum()
		rapportoPositiviSuTotaleTamponiUltimoGiorno=nuoviPositiviUltimoGiorno*100/tamponiEffettuatuUltimoGiorno
		rapportoPositiviSuTotaleTamponiUltimoGiornoInVeneto=rapportoPositiviSuTotaleTamponiUltimoGiorno["Veneto"]
		rapportoPositiviSuTotaleTamponiGiornalieriInVeneto.append(rapportoPositiviSuTotaleTamponiUltimoGiornoInVeneto)
		covid19UltimoGiorno["ultimo_giorno_rapporto_positivi_tamponi"]=rapportoPositiviSuTotaleTamponiUltimoGiorno
		rapportoPositiviTamponiUltimoGiornoInItalia=nuoviPositiviUltimoGiornoInItalia*100/tamponiEffettuatuUltimoGiornoTotale
		rapportoPositiviSuTotaleTamponiGiornalieri.append(rapportoPositiviTamponiUltimoGiornoInItalia)

		#TERAPIA INTENSIVA
		ingressiUltimoGiornoTerapiaIntensiva=covid19UltimoGiorno["terapia_intensiva"]-covid19PenultimoGiorno["terapia_intensiva"]
		ingressiUltimoGiornoTerapiaIntensivaInVeneto=ingressiUltimoGiornoTerapiaIntensiva["Veneto"]
		ingressiUltimoGiornoTerapiaIntensivaInItalia=ingressiUltimoGiornoTerapiaIntensiva.sum()
		ingressiIntensivaGiornalieri.append(ingressiUltimoGiornoTerapiaIntensivaInItalia)
		ingressiIntensivaGiornalieriInVeneto.append(ingressiUltimoGiornoTerapiaIntensivaInVeneto*moltiplicatore)

		#OSPEDALIZZATI
		ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva=covid19UltimoGiorno["ricoverati_con_sintomi"]-covid19PenultimoGiorno["ricoverati_con_sintomi"]
		ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInVeneto=ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva["Veneto"]
		ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia=ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva.sum()
		ingressiNonIntensivaGiornalieriInVeneto.append(ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInVeneto*moltiplicatore)
		ingressiNonIntensivaGiornalieri.append(ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia)
		
		#DECEDUTI
		decedutiUltimoGiornoInVeneto=(covid19UltimoGiorno["deceduti"]-covid19PenultimoGiorno["deceduti"])["Veneto"]
		decedutiUltimoGiorno=covid19UltimoGiorno["deceduti"].sum()-covid19PenultimoGiorno["deceduti"].sum()
		deceduti.append(decedutiUltimoGiorno)
		decedutiInVeneto.append(decedutiUltimoGiornoInVeneto*moltiplicatore)

		#LETALITà
		tassoDiMortalita=covid19UltimoGiorno["deceduti"]*100/covid19UltimoGiorno["totale_casi"]
		tassoDiMortalitaInVeneto=tassoDiMortalita["Veneto"]
		tassoDiMortalitaNazionale=covid19UltimoGiorno["deceduti"].sum()*100/covid19UltimoGiorno["totale_casi"].sum()
		letalitaInVeneto.append(tassoDiMortalitaInVeneto)
		letalita.append(tassoDiMortalitaNazionale)

	#-----------------------------MODIFICHE-----------------------------------------

	#Abbiamo visto che quando i deceduti italiani sono -31 dovrebbero essere 30, quindi correggiamo il valore con mezza riga
	deceduti[deceduti.index(-31)]=30	
	#Abbiamo altresì visto che quando i deceduti Veneti sono -1 (il 23/06/2021), dovrebbero essere 2, quindi correggiamo il valore
	decedutiInVeneto[485]=2*moltiplicatore

	#Correggiamo i valori negativi o superiori a 100
	rapportoPositiviSuTamponiMolecolariGiornalieri[297]=(rapportoPositiviSuTamponiMolecolariGiornalieri[296]+rapportoPositiviSuTamponiMolecolariGiornalieri[298])/2

	rapportoPositiviSuTamponiMolecolariGiornalieriInVeneto[14]=(rapportoPositiviSuTamponiMolecolariGiornalieriInVeneto[13]+rapportoPositiviSuTamponiMolecolariGiornalieriInVeneto[15])/2


	'''
	#Grafico positivi test molecolari
	plt.figure(figsize=(16,10))
	veneto,=plt.plot(listaDate,rapportoPositiviSuTamponiMolecolariGiornalieriInVeneto,label="Veneto")
	italia,=plt.plot(listaDate,rapportoPositiviSuTamponiMolecolariGiornalieri,label="Italia")
	plt.legend([veneto,italia],["Veneto","Italia"])
	plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0)
	plt.xticks(listaDate[1::30])
	plt.title('Tasso di positivita giornaliero ai tamponi molecolari da inizio pandemia')
	plt.xlabel('Date')
	plt.ylabel('Tasso di positivita')
	plt.grid(axis='y')
	plt.show()

	#Grafico positivi test totali
	plt.figure(figsize=(16,10))
	veneto,=plt.plot(listaDate,rapportoPositiviSuTotaleTamponiGiornalieriInVeneto,label="Veneto")
	italia,=plt.plot(listaDate,rapportoPositiviSuTotaleTamponiGiornalieri,label="Italia")
	plt.legend([veneto,italia],["Veneto","Italia"])
	plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0)
	plt.xticks(listaDate[1::30])
	plt.title('Tasso di positivita giornaliero a tutti i tamponi dal 15 gennaio')
	plt.xlabel('Date')
	plt.ylabel('Tasso di positivita')
	plt.grid(axis='y')
	plt.show()

	#Grafico intensiva
	plt.figure(figsize=(16,10))
	veneto,=plt.plot(listaDate,ingressiIntensivaGiornalieriInVeneto,label="Veneto")
	italia,=plt.plot(listaDate,ingressiIntensivaGiornalieri,label="Media \nRegionale")
	plt.legend([veneto,italia],["Veneto","Media \nRegionale"])
	plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0)
	plt.xticks(listaDate[1::30])
	plt.title('Ingressi giornalieri in terapia intensiva')
	plt.xlabel('Date')
	plt.ylabel('Nuove terapie intensive')
	plt.grid(axis='y')
	plt.show()

	#Grafico non intensiva
	plt.figure(figsize=(16,10))
	veneto,=plt.plot(listaDate,ingressiNonIntensivaGiornalieriInVeneto,label="Veneto")
	italia,=plt.plot(listaDate,ingressiNonIntensivaGiornalieri,label="Media \nRegionale")
	plt.legend([veneto,italia],["Veneto","Media \nRegionale"])
	plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0)
	plt.xticks(listaDate[1::30])
	plt.title('Ingressi giornalieri in ospendale non in terapia intensiva')
	plt.xlabel('Date')
	plt.ylabel('Nuovi ospedalizzati non intensivi')
	plt.grid(axis='y')
	plt.show()

	#Grafico deceduti
	plt.figure(figsize=(16,10))
	veneto,=plt.plot(listaDate,decedutiInVeneto,label="Veneto") 
	italia,=plt.plot(listaDate,deceduti,label="Media \nRegionale")
	plt.legend([veneto,italia],["Veneto","Media \nRegionale"])
	plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0)
	plt.xticks(listaDate[1::30])
	plt.title('Deceduti giornalieri')
	plt.xlabel('Date')
	plt.ylabel('Deceduti')
	plt.grid(axis='y')
	plt.show()

	#Grafico letalita
	plt.figure(figsize=(16,10))
	veneto,=plt.plot(listaDate,letalitaInVeneto,label="Veneto")
	italia,=plt.plot(listaDate,letalita,label="Italia")
	plt.legend([veneto,italia],["Veneto","Italia"])
	plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0)
	plt.xticks(listaDate[1::30])
	plt.title('Tasso di letalita da inizio pandemia')
	plt.xlabel('Date')
	plt.ylabel('Letalita')
	plt.grid(axis='y')
	plt.show()
	'''

	#------------------Creazione database-------------------
	#lista per database
	listaRegioniPerDatabase=["Abruzzo","Basilicata","Calabria","Campania","EmiliaRomagna","FriuliVeneziaGiulia","Lazio","Liguria","Lombardia","Marche","Molise","AltoAdige","Trentino","Piemonte","Puglia","Sardegna","Sicilia","Toscana","Umbria","ValleDAosta"]

	covid19PerGraficiGiornalieriItaliaVeneto=pd.DataFrame({"Data":listaDate})

	covid19PerGraficiGiornalieriItaliaVeneto["positiviMolecolariInItalia"]=rapportoPositiviSuTamponiMolecolariGiornalieri
	covid19PerGraficiGiornalieriItaliaVeneto["positiviMolecolariInVeneto"]=rapportoPositiviSuTamponiMolecolariGiornalieriInVeneto
	covid19PerGraficiGiornalieriItaliaVeneto["ingressiTerapiaIntensivaInItalia"]=ingressiIntensivaGiornalieri
	covid19PerGraficiGiornalieriItaliaVeneto["ingressiTerapiaIntensivaInVeneto"]=ingressiIntensivaGiornalieriInVeneto
	covid19PerGraficiGiornalieriItaliaVeneto["ingressiFuoriIntensivaInItalia"]=ingressiNonIntensivaGiornalieri
	covid19PerGraficiGiornalieriItaliaVeneto["ingressiFuoriIntensivaInVeneto"]=ingressiNonIntensivaGiornalieriInVeneto

	covid19PerGraficiGiornalieriItaliaVeneto["decedutiInItalia"]= deceduti
	covid19PerGraficiGiornalieriItaliaVeneto["decedutiInVenetoPopolosoQuantoItalia"]=decedutiInVeneto
	covid19PerGraficiGiornalieriItaliaVeneto["letalitaItaliana"]=letalita
	covid19PerGraficiGiornalieriItaliaVeneto["letalitaVeneta"]=letalitaInVeneto

	#CALCOLIAMO LA LETALITà REGIONE PER REGIONE E LA METTIAMO NEL DATABASE
	for i in range(len(listaRegioniPerDatabase)):
		covid19PerGraficiGiornalieriItaliaVeneto["letalita"+str(listaRegioniPerDatabase[i])]=letalitaRegione(listaRegioni[i],covid19,covid19PrimoGiorno,listaDate,quanteDateCiSonoState)

	#Creazione database con le sole date in cui nel conteggio hanno aggiunto i tamponi rapidi
	covid19PerGraficiTamponiTotali=pd.DataFrame({"Data":listaDate[listaDate.index("15-01-2021"):]})
	covid19PerGraficiTamponiTotali["PositiviSuTotaleTamponiInItalia"]=rapportoPositiviSuTotaleTamponiGiornalieri
	covid19PerGraficiTamponiTotali["PositiviSuTotaleTamponiInVeneto"]=rapportoPositiviSuTotaleTamponiGiornalieriInVeneto

	#------------------------------COMMIT TO GITHUB-----------------------------------
	df1=covid19PerGraficiGiornalieriItaliaVeneto.to_csv(sep=",",index=False)
	df2=covid19PerGraficiTamponiTotali.to_csv(sep=",",index=False)

	fileList=[df1,df2]
	fileNames=["Covid19GraficiItaliaEVeneto.csv","Covid19GraficiTamponiTotaliItaliaEVeneto.csv"]

	commitMessage=dateImport.today().strftime("%d-%m-%Y")

	g=Github(environ["gitToken"])

	#creo connessione
	repo=g.get_user().get_repo("Covid")
	mainRef= repo.get_git_ref("heads/main")

	#carichiamo il file
	mainSha=mainRef.object.sha
	baseTree= repo.get_git_tree(mainSha)

	elementList=[]
	for i in range(len(fileList)):
		element=InputGitTreeElement(fileNames[i],'100644','blob',fileList[i])#100644 è per file normale, 'blob' binary large object per caricare su gihub file
		elementList.append(element)

	tree=repo.create_git_tree(elementList, baseTree)
	parent=repo.get_git_commit(mainSha)
	commit=repo.create_git_commit(commitMessage,tree,[parent])
	mainRef.edit(commit.sha)
	print("Aggiornamento giornaliero completato")

