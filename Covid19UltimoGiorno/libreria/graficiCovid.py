#File per l'aggiunta dei dati relativi all'ultimo giorno ai csv contenenti i dati giornalieri generati dal file "graficiCovid.py" nella cartella "Covid19DaInizioPandemia/libreria"

#import necessari
import math
import pandas as pd
import os
from os import environ
from github import Github, InputGitTreeElement
import datetime
from datetime import date as dateImport

#import dei file della stessa cartella
from libreria.numeroDiAbitanti import *
from libreria.graficiCovidRegionePerRegione import *

#Riga per evitare warning di pandas
pd.options.mode.chained_assignment = None

#Funzione chiamata da application per leggere il csv della Protezione Civile, elaborarne i dati, aggiungere una riga ai nostri csv giornalieri e ripusharli nella cartella pubblica "Covid" di github
def graficiGiornalieri():

	covid19 = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv",sep=",") #Lettura csv della Protezione Civile
	covid19NostroSenzaTotali=pd.read_csv("https://raw.githubusercontent.com/DigitalChriAri/Covid/main/Covid19GraficiItaliaEVeneto.csv", sep=",") #Lettura nostro csv giornaliero senza tamponi totali
	covid19NostroSoloTotali = pd.read_csv("https://raw.githubusercontent.com/DigitalChriAri/Covid/main/Covid19GraficiTamponiTotaliItaliaEVeneto.csv", sep=",") #Lettura nostro csv gionraliero con solo i tamponi totali

	
	covid19['data']=(pd.to_datetime(covid19["data"])) #Trasformazione della colonna contenente le date nel type delle date
	covid19=covid19.fillna(0) #sostituzione dei valori NAN con 0

	listaDate1=list(pd.to_datetime(covid19["data"])) #Lista contenente tutte le date (ogni data è ripetuta 21 volte, cioè una per regione)
	listaDate=[listaDate1[i].strftime("%d-%m-%Y") for i in range(len(listaDate1))] #Conversione delle date nella lista nel formato dd-mm-aaaa
	covid19["data"]=listaDate.copy() #Inserimento delle date nel formato comodo nel csv originario

	covid19.drop(["stato","codice_regione","lat","long","codice_nuts_1", "codice_nuts_2","note","note_test","note_casi"], axis=1, inplace=True) #Eliminazione delle colonne inutili
	covid19.set_index("denominazione_regione",inplace=True) #Le regioni diventano gli indici del DataFrame

	#Prendiamo tutte le date da inizio pandemia
	date=covid19["data"]

	#moltiplicatoreRegione è una funzione nel file "numeroDiAbitanti.py" cha calcola il rapporto tra popolazione italiana e quella della regione passata come input
	moltiplicatoreVeneto=moltiplicatoreRegione("Veneto")

	#lista delle regioni utilizzata per calcolare i valori della letalità regione per regione
	listaRegioni=["Abruzzo","Basilicata","Calabria","Campania","Emilia-Romagna","Friuli Venezia Giulia","Lazio","Liguria","Lombardia","Marche","Molise","P.A. Bolzano","P.A. Trento","Piemonte","Puglia","Sardegna","Sicilia","Toscana","Umbria","Valle d'Aosta"]

	#-------------------------------------------------- DATI ULTIMO GIORNO------------------------------------------------------------------
	#I due dataFrame sono dei sottoinsiemi del dataFrame originario, uno è relativo all'ultimo giorno e uno al penultimo
	covid19UltimoGiorno=covid19[covid19["data"]==date[-1]]
	covid19PenultimoGiorno=covid19[covid19["data"]==date[-22]] # -22 perchè ogni data è ripetuta 21 volte

	#TASSO TAMPONI MOLECOLARI
	tamponiMolecolariUltimoGiorno=covid19UltimoGiorno["tamponi_test_molecolare"]-covid19PenultimoGiorno["tamponi_test_molecolare"]
	tamponiMolecolariUltimoGiornoInVeneto=tamponiMolecolariUltimoGiorno["Veneto"]
	nuoviPositiviMolecolare=covid19UltimoGiorno["totale_positivi_test_molecolare"]-covid19PenultimoGiorno["totale_positivi_test_molecolare"]
	nuoviPositiviMolecolareInVeneto=nuoviPositiviMolecolare["Veneto"]
	tassoPositiviMolecolari=nuoviPositiviMolecolare*100/tamponiMolecolariUltimoGiorno
	tassoPositiviMolecolariInVeneto=nuoviPositiviMolecolareInVeneto*100/tamponiMolecolariUltimoGiornoInVeneto
	tassoNazionalePositiviMolecolari=nuoviPositiviMolecolare.sum()*100/tamponiMolecolariUltimoGiorno.sum()
	
	#TASSO TAMPONI TOTALI
	tamponiEffettuatuUltimoGiorno=covid19UltimoGiorno["tamponi"]-covid19PenultimoGiorno["tamponi"]
	tamponiEffettuatuUltimoGiornoInVeneto=tamponiEffettuatuUltimoGiorno["Veneto"]
	tamponiEffettuatuUltimoGiornoTotale=tamponiEffettuatuUltimoGiorno.sum()
	nuoviPositiviUltimoGiorno=covid19UltimoGiorno["nuovi_positivi"]
	nuoviPositiviUltimoGiornoInVeneto=nuoviPositiviUltimoGiorno["Veneto"]
	nuoviPositiviUltimoGiornoInItalia=nuoviPositiviUltimoGiorno.sum()
	rapportoPositiviSuTotaleTamponiUltimoGiorno=nuoviPositiviUltimoGiorno*100/tamponiEffettuatuUltimoGiorno
	rapportoPositiviSuTotaleTamponiUltimoGiornoInVeneto=rapportoPositiviSuTotaleTamponiUltimoGiorno["Veneto"]
	rapportoPositiviTamponiUltimoGiornoInItalia=nuoviPositiviUltimoGiornoInItalia*100/tamponiEffettuatuUltimoGiornoTotale

	#INGRESSI GIORNALIERI IN TERAPIA INTENSIVA SUPPONENDO CHE IL VENETO ABBIA LO STESSO NUMERO DI ABITANTI DELL'ITALIA
	ingressiUltimoGiornoTerapiaIntensiva=covid19UltimoGiorno["terapia_intensiva"]-covid19PenultimoGiorno["terapia_intensiva"]
	ingressiUltimoGiornoTerapiaIntensivaInVeneto=ingressiUltimoGiornoTerapiaIntensiva["Veneto"]*moltiplicatoreVeneto
	ingressiUltimoGiornoTerapiaIntensivaInItalia=ingressiUltimoGiornoTerapiaIntensiva.sum()

	#INGRESSI GIORNALIERI NEI RICOVERI ORDINARI SUPPONENDO CHE IL VENETO ABBIA LO STESSO NUMERO DI ABITANTI DELL'ITALIA
	ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva=covid19UltimoGiorno["ricoverati_con_sintomi"]-covid19PenultimoGiorno["ricoverati_con_sintomi"]
	ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInVeneto=ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva["Veneto"]*moltiplicatoreVeneto
	ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia=ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva.sum()

	#DECEDUTI SUPPONENDO CHE IL VENETO ABBIA LO STESSO NUMERO DI ABITANTI DELL'ITALIA
	decedutiUltimoGiornoInVeneto=((covid19UltimoGiorno["deceduti"]-covid19PenultimoGiorno["deceduti"])["Veneto"])*moltiplicatoreVeneto
	decedutiUltimoGiorno=covid19UltimoGiorno["deceduti"].sum()-covid19PenultimoGiorno["deceduti"].sum()

	#LETALITA
	tassoDiMortalita=covid19UltimoGiorno["deceduti"]*100/covid19UltimoGiorno["totale_casi"]
	tassoDiMortalitaInVeneto=tassoDiMortalita["Veneto"]
	tassoDiMortalitaNazionale=covid19UltimoGiorno["deceduti"].sum()*100/covid19UltimoGiorno["totale_casi"].sum()

	#LETALITA REGIONE PER REGIONE
	#In questa lista ci saranno i valori dell'ultima giornata regione per regione
	listaLetalitaRegioni=[]
	for regione in listaRegioni:
		listaLetalitaRegioni.append(letalitaRegione(regione,covid19,covid19UltimoGiorno)) #La funzione letalitaRegione calcola la letalità nella regione passata come input

	#------------------------------------AGGIORNAMENTO DATABASE SENZA TASSO SUI TAMPONI TOTALI----------------------------------
	listaRegioniPerDatabase=["Abruzzo","Basilicata","Calabria","Campania","EmiliaRomagna","FriuliVeneziaGiulia","Lazio","Liguria","Lombardia","Marche","Molise","AltoAdige","Trentino","Piemonte","Puglia","Sardegna","Sicilia","Toscana","Umbria","ValleDAosta"]

	#rigaDaAggiungere è un dizionario contenente come chiavi i nomi delle colonne e come valori i dati relativi all'ultimo giorno
	rigaDaAggiungere={"Data": date[-1], "positiviMolecolariInItalia": tassoNazionalePositiviMolecolari,"positiviMolecolariInVeneto": tassoPositiviMolecolariInVeneto,"ingressiTerapiaIntensivaInItalia":ingressiUltimoGiornoTerapiaIntensivaInItalia , "ingressiTerapiaIntensivaInVeneto":ingressiUltimoGiornoTerapiaIntensivaInVeneto , "ingressiFuoriIntensivaInItalia": ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia,"ingressiFuoriIntensivaInVeneto": ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInVeneto, "decedutiInItalia": decedutiUltimoGiorno, "decedutiInVenetoPopolosoQuantoItalia":decedutiUltimoGiornoInVeneto , "letalitaItaliana": tassoDiMortalitaNazionale ,"letalitaVeneta": tassoDiMortalitaInVeneto}

	#aggiungiamo al dizionario i valori della letalità per ciascuna regione
	for i in range(len(listaRegioniPerDatabase)):
		rigaDaAggiungere["letalita"+str(listaRegioniPerDatabase[i])]=listaLetalitaRegioni[i]
		
	#aggiungiamo la riga al nostro database	
	covid19NostroSenzaTotali=covid19NostroSenzaTotali.append(rigaDaAggiungere,ignore_index=True)

	#------------------------------------AGGIORNAMENTO DATABASE COL SOLO TASSO SUI TAMPONI TOTALI----------------------------------
	
	#rigaDaAggiungereTotali contiene soltanto i valori del tasso sui tamponi totali di Italia e Veneto
	rigaDaAggiungereTotali={"Data": date[-1], "PositiviSuTotaleTamponiInItalia":rapportoPositiviTamponiUltimoGiornoInItalia, "PositiviSuTotaleTamponiInVeneto": rapportoPositiviSuTotaleTamponiUltimoGiornoInVeneto}

	#aggiungiamo la riga al nostro database	
	covid19NostroSoloTotali=covid19NostroSoloTotali.append(rigaDaAggiungereTotali,ignore_index=True)

	#---------------------------------------------------COMMIT SU GITHUB------------------------------------------------
	#df1 e df2 sono rispettivamente i database senza e con i tamponi totali
	df1=covid19NostroSenzaTotali.to_csv(sep=",",index=False)
	df2=covid19NostroSoloTotali.to_csv(sep=",",index=False)

	fileList=[df1,df2]
	fileNames=["Covid19GraficiItaliaEVeneto.csv","Covid19GraficiTamponiTotaliItaliaEVeneto.csv"]#nomi del csv

	#testo del commit ch sarà del tipo "dd-mm-aaaa"
	commitMessage=dateImport.today().strftime("%d-%m-%Y")
	g=Github(environ["gitToken"]) #token dell'account Github DigitalChriAri con la repository "Covid". Il token è indispensabile per il commit su una cartella pubblica

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

