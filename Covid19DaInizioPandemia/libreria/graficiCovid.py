#File per i csv con i dati giornalieri da inizio pandemia

#Tutti gli import necessari
import math
import pandas as pd
from github import Github, InputGitTreeElement
from datetime import date as dateImport
from os import environ

#Import degli altri file della stessa cartella
from libreria.numeroDiAbitanti import *
from libreria.graficiCovidRegionePerRegione import *

pd.options.mode.chained_assignment = None #Riga per evitare i warning

#Funzione chiamata da application per leggere il csv della Protezione Civile, elaborarne i dati, generare due nuovi csv e pusharli nella cartella pubblica "Covid" di github
def graficiGiornalieri():
	
	covid19 = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv",sep=",") #Per leggere il csv della Protezione Civile
	covid19['data']=(pd.to_datetime(covid19["data"])) #Trasformazione della colonna contenente le date nel type delle date
	covid19=covid19.fillna(0) #Pulizia dei valori NAN
	listaDate1=list(pd.to_datetime(covid19["data"])) #Lista contenente tutte le date (ogni data è ripetuta 21 volte, cioè una per regione)
	listaDate=[listaDate1[i].strftime("%d-%m-%Y") for i in range(len(listaDate1))] #Conversione delle date nella lista nel formato dd-mm-aaaa

	covid19["data"]=listaDate.copy() #Inserimento delle date nel formato comodo nel csv originario
	covid19.drop(["stato","codice_regione","lat","long","codice_nuts_1", "codice_nuts_2","note","note_test","note_casi"], axis=1, inplace=True) #Eliminazione delle colonne inutili
	covid19.set_index("denominazione_regione",inplace=True) #Le regioni diventano gli indici del DataFrame
	
	#------Pulizia di listaDate------
	#Su listaDate ci saranno le date una e una sola volta
	date=covid19["data"]
	quanteDateCiSonoState=len(listaDate)//21
	listaDate=[]
	listaDate=[date[-21*i-1] for i in range(quanteDateCiSonoState-1,-1,-1)]
	
	#Lista per la generazione dei dati regionali
	listaRegioni=["Abruzzo","Basilicata","Calabria","Campania","Emilia-Romagna","Friuli Venezia Giulia","Lazio","Liguria","Lombardia","Marche","Molise","P.A. Bolzano","P.A. Trento","Piemonte","Puglia","Sardegna","Sicilia","Toscana","Umbria","Valle d'Aosta"]
	
	#------------------------------------------------PRIMO GIORNO DI PANDEMIA-------------------------------------------------
	covid19PrimoGiorno=covid19[covid19["data"]==listaDate[0]]

	#TAMPONI MOLECOLARI 
	#Nelle due liste qui sotto raccoglieremo i valori giorno per giorno relativi rispettivamente a Italia e Veneto
	rapportoPositiviSuTamponiMolecolariGiornalieri=[]
	rapportoPositiviSuTamponiMolecolariGiornalieriInVeneto=[]
	tamponiMolecolariPrimoGiorno=covid19PrimoGiorno["tamponi"] #Questa istruzione genera una series costituita dai valori della colonna "tamponi" regione per regione
	tamponiMolecolariPrimoGiornoInVeneto=tamponiMolecolariPrimoGiorno["Veneto"] #Questa istruzione prende il valore della colonna appena generata dove l'indice è "Veneto"
	nuoviPositiviMolecolariPrimoGiorno=covid19PrimoGiorno["nuovi_positivi"]
	nuoviPositiviMolecolariPrimoGiornoInVeneto=nuoviPositiviMolecolariPrimoGiorno["Veneto"]
	tassoPositiviSuTamponiMolecolariPrimoGiorno=nuoviPositiviMolecolariPrimoGiorno.sum()*100/tamponiMolecolariPrimoGiorno.sum() #Calcoliamo la percentuale italiana (col .sum() si sommano i valori della serie che sono regione per regione)
	tassoPositiviSuTamponiMolecolariPrimoGiornoInVeneto=nuoviPositiviMolecolariPrimoGiornoInVeneto*100/tamponiMolecolariPrimoGiornoInVeneto #Percentuale veneta
	rapportoPositiviSuTamponiMolecolariGiornalieri.append(tassoPositiviSuTamponiMolecolariPrimoGiorno)
	rapportoPositiviSuTamponiMolecolariGiornalieriInVeneto.append(tassoPositiviSuTamponiMolecolariPrimoGiornoInVeneto)

	#POSITIVI SU TAMPONI TOTALI (creiamo solo le liste perché sino al 15 gennaio venivano conteggiati solo i tamponi molecolari)
	rapportoPositiviSuTotaleTamponiGiornalieri=[]
	rapportoPositiviSuTotaleTamponiGiornalieriInVeneto=[]

	#INGRESSI GIORNALIERI IN TERAPIA INTENSIVA SUPPONENDO IL VENETO POPOLOSO QUANTO L'ITALIA
	ingressiIntensivaGiornalieri=[]
	ingressiIntensivaGiornalieriInVeneto=[]
	ingressiPrimoGiornoTerapiaIntensiva=covid19PrimoGiorno["terapia_intensiva"]
	ingressiPrimoGiornoTerapiaIntensivaInVeneto=ingressiPrimoGiornoTerapiaIntensiva["Veneto"]
	ingressiPrimoGiornoTerapiaIntensivaInItalia=ingressiPrimoGiornoTerapiaIntensiva.sum()
	ingressiIntensivaGiornalieri.append(ingressiPrimoGiornoTerapiaIntensivaInItalia)
	ingressiIntensivaGiornalieriInVeneto.append(ingressiPrimoGiornoTerapiaIntensivaInVeneto*moltiplicatore) #Il valore assoluto viene moltiplicato per il rapporto tra popolazione italiana e veneta che viene calcolato nel file numeroDiAbitanti.py

	#INGRESSI GIORNALIERI NON IN TERAPIA INTENSIVA SUPPONENDO IL VENETO POPOLOSO QUANTO L'ITALIA
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

	#LETALITA (PERCENTUALE DI MORTI DA INIZIO PANDEMIA SUL TOTALE DI POSITIVI RISCONTRATI DA INIZIO PANDEMIA)
	letalita=[]
	letalitaInVeneto=[]
	tassoDiMortalitaPrimoGiorno=covid19PrimoGiorno["deceduti"]*100/covid19PrimoGiorno["totale_casi"]
	tassoDiMortalitaPrimoGiornoInVeneto=tassoDiMortalitaPrimoGiorno["Veneto"]
	tassoDiMortalitaNazionalePrimoGiorno=covid19PrimoGiorno["deceduti"].sum()*100/covid19PrimoGiorno["totale_casi"].sum()
	letalitaInVeneto.append(tassoDiMortalitaPrimoGiornoInVeneto)
	letalita.append(tassoDiMortalitaNazionalePrimoGiorno)


	#----------------------------------------- VALORI FINO AL 14 GENNAIO 2021 INCLUSO-----------------------------------------
	#Il 15 gennaio la Protezione Civile ha iniziato a conteggiare anche i tamponi rapidi. Fino al 14 gennaio con la colonna "tamponi" si indicavano i soli tamponi molecolari
	#e di conseguenza, con nuovi_positivi i soli positivi ai molecolari. Dal 15 gennaio, la colonna "tamponi" si riferisce a tutti i tamponi, mentre per i soli 
	#tamponi molecolari sono state introdotte le colonne tamponi_test_molecolari e tolale_positivi_test_molecolare
	
	#Ciclo for per i dati fino al 15 gennaio 2021 escluso
	for i in range(1,listaDate.index("15-01-2021")):
		#Sottoinsiemi del dataframe di partenza con i dati relativi rispettivamente alla giornata i e a quella precedente.
		covid19UltimoGiorno=covid19[covid19["data"]==listaDate[i]]
		covid19PenultimoGiorno=covid19[covid19["data"]==listaDate[i-1]]

		#TAMPONI MOLECOLARI 
		#La colonna tamponi indica il totale dei tamponi effettuati da inizio pandemia
		#La colonna nuovi_positivi indica solo i positivi dell'ultima giornata
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
		#La colonna "terapia_intensiva" indica il numero di persone ricoverate in terapia intensiva al giorno i
		ingressiUltimoGiornoTerapiaIntensiva=covid19UltimoGiorno["terapia_intensiva"]-covid19PenultimoGiorno["terapia_intensiva"]
		ingressiUltimoGiornoTerapiaIntensivaInVeneto=ingressiUltimoGiornoTerapiaIntensiva["Veneto"]
		ingressiUltimoGiornoTerapiaIntensivaInItalia=ingressiUltimoGiornoTerapiaIntensiva.sum()
		ingressiIntensivaGiornalieri.append(ingressiUltimoGiornoTerapiaIntensivaInItalia)
		ingressiIntensivaGiornalieriInVeneto.append(ingressiUltimoGiornoTerapiaIntensivaInVeneto*moltiplicatore)

		#OSPEDALIZZATI
		#La colonna "ricoverati_con_sintomi" indica il numero di persone ricoverate nei reparti ordinari al giorno i
		ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva=covid19UltimoGiorno["ricoverati_con_sintomi"]-covid19PenultimoGiorno["ricoverati_con_sintomi"]
		ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInVeneto=ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva["Veneto"]
		ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia=ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva.sum()
		ingressiNonIntensivaGiornalieriInVeneto.append(ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInVeneto*moltiplicatore)
		ingressiNonIntensivaGiornalieri.append(ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia)
		
		#DECEDUTI 
		#La colonna deceduti indica il numero di deceduti da inizio pandemia
		decedutiUltimoGiornoInVeneto=(covid19UltimoGiorno["deceduti"]-covid19PenultimoGiorno["deceduti"])["Veneto"]
		decedutiUltimoGiorno=covid19UltimoGiorno["deceduti"].sum()-covid19PenultimoGiorno["deceduti"].sum()
		deceduti.append(decedutiUltimoGiorno)
		decedutiInVeneto.append(decedutiUltimoGiornoInVeneto*moltiplicatore)

		#LETALITà
		#La colonna "totale_casi" indica il numero di persone riscontrate positive da inizio pandemia
		tassoDiMortalita=covid19UltimoGiorno["deceduti"]*100/covid19UltimoGiorno["totale_casi"]
		tassoDiMortalitaInVeneto=tassoDiMortalita["Veneto"]
		tassoDiMortalitaNazionale=covid19UltimoGiorno["deceduti"].sum()*100/covid19UltimoGiorno["totale_casi"].sum()
		letalitaInVeneto.append(tassoDiMortalitaInVeneto)
		letalita.append(tassoDiMortalitaNazionale)


	
	#-------------------------------------------------Giorno 15 gennaio 2021---------------------------------------------------
	#In questa data la colonna "tamponi" non ha lo stesso significato che aveva fino al 14 gennaio 2021
	
	#TAMPONI MOLECOLARI
	#Per calcolare il numero di tamponi molecolari effettuati il 15 abbiamo fatto la sottrazione tra i tamponi solo molecolari fino al 15 con i tamponi totali (quindi effettivamente solo molecolari) fino al 14
	#Per calcolare il numero di nuovi positivi del 15 abbiamo sottratto i positivi a tutti i tamponi eseguiti fino al quindici (quindi molecolari fino al 14, molecolari del 15 e rapidi del 15) con i positivi al test rapido del 15
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


	#-------------------------------------------VALORI DAL 16 GENNAIO 2021 IN POI------------------------------------
	
	#Ciclo for per i giorni dal 16 gennaio 2021 ad oggi
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

	#------------------------------------------MODIFICHE--------------------------------------------
	#Ci siamo accorti che alcuni valori erano sbagliato e tramite le note siamo risaliti ai valori corretti che abbiamo sostituito
	
	#Abbiamo visto che quando i deceduti italiani sono -31 dovrebbero essere 30, quindi correggiamo il valore
	deceduti[deceduti.index(-31)]=30	
	#Abbiamo altresì visto che quando i deceduti Veneti sono -1 (il 23/06/2021, ovvero il 486 da inizio pandemia, quindi indicizzato con 485), dovrebbero essere 2, quindi correggiamo il valore
	decedutiInVeneto[485]=2*moltiplicatore

	#Correggiamo alcuni valori delle percentuali negativi o superiori a 100 facendo la media tra il giorno precedente e quello successivo
	rapportoPositiviSuTamponiMolecolariGiornalieri[297]=(rapportoPositiviSuTamponiMolecolariGiornalieri[296]+rapportoPositiviSuTamponiMolecolariGiornalieri[298])/2
	rapportoPositiviSuTamponiMolecolariGiornalieriInVeneto[14]=(rapportoPositiviSuTamponiMolecolariGiornalieriInVeneto[13]+rapportoPositiviSuTamponiMolecolariGiornalieriInVeneto[15])/2

	

	#--------------------------------------------------------GENERAZIONE NOSTRI CSV----------------------------------
	#lista per database (I nomi non possono avere spazi altrimenti html non riesce a leggere la colonna)
	listaRegioniPerDatabase=["Abruzzo","Basilicata","Calabria","Campania","EmiliaRomagna","FriuliVeneziaGiulia","Lazio","Liguria","Lombardia","Marche","Molise","AltoAdige","Trentino","Piemonte","Puglia","Sardegna","Sicilia","Toscana","Umbria","ValleDAosta"]

	#Database con tutti i valori tranne i tamponi totali (non ci sono i valori sino al 14 gennaio 2021)
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

	#Calcoliamo la letalità regione per regione e la mettiamo nel database
	#Per farlo chiama la funzione letalità regione implementata nel file graficiCovidRegionePerRegione.py che fa gli stessi calcoli del veneto generalizzati per la regione passata come input
	for i in range(len(listaRegioniPerDatabase)):
		covid19PerGraficiGiornalieriItaliaVeneto["letalita"+str(listaRegioniPerDatabase[i])]=letalitaRegione(listaRegioni[i],covid19,covid19PrimoGiorno,listaDate,quanteDateCiSonoState)

	#Creazione database con i soli tamponi totali
	covid19PerGraficiTamponiTotali=pd.DataFrame({"Data":listaDate[listaDate.index("15-01-2021"):]})
	covid19PerGraficiTamponiTotali["PositiviSuTotaleTamponiInItalia"]=rapportoPositiviSuTotaleTamponiGiornalieri
	covid19PerGraficiTamponiTotali["PositiviSuTotaleTamponiInVeneto"]=rapportoPositiviSuTotaleTamponiGiornalieriInVeneto

	
	#------------------------------------------COMMIT TO GITHUB----------------------------------------------
	#df1 e df2 sono i due file da committare
	df1=covid19PerGraficiGiornalieriItaliaVeneto.to_csv(sep=",",index=False)
	df2=covid19PerGraficiTamponiTotali.to_csv(sep=",",index=False)
	
	fileList=[df1,df2]
	fileNames=["Covid19GraficiItaliaEVeneto.csv","Covid19GraficiTamponiTotaliItaliaEVeneto.csv"]

	commitMessage=dateImport.today().strftime("%d-%m-%Y")	#Il messaggio del commit
	g=Github(environ["gitToken"]) #g contiene la variabile d'ambiente gitToken indispensabile per i commit pubblici

	#Creazione di una connessione tra il codice e la cartella "Covid"
	repo=g.get_user().get_repo("Covid")
	mainRef= repo.get_git_ref("heads/main")

	#carichiamo il file con le seguenti istruzioni per fare il push su github
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

