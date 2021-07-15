#Ora facciamo i grafici dei valori giornalieri giorno dopo giorno da inizio pandemia
import math
import pandas as pd
pd.options.mode.chained_assignment = None
import os
from os import environ
#Codice per commitare su Gthub
from github import Github, InputGitTreeElement
import datetime
from datetime import date as dateImport
from libreria.numeroDiAbitanti import *
from libreria.graficiCovidRegionePerRegione import *

def graficiGiornalieri():

	covid19 = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv",sep=",")
	covid19NostroSenzaTotali=pd.read_csv("https://raw.githubusercontent.com/DigitalChriAri/Covid/main/Covid19GraficiItaliaEVeneto.csv", sep=",")
	covid19NostroSoloTotali = pd.read_csv("https://raw.githubusercontent.com/DigitalChriAri/Covid/main/Covid19GraficiTamponiTotaliItaliaEVeneto.csv", sep=",")

	
	covid19['data']=(pd.to_datetime(covid19["data"]))
	covid19=covid19.fillna(0)

	listaDate1=list(pd.to_datetime(covid19["data"]))
	listaDate=[listaDate1[i].strftime("%d-%m-%Y") for i in range(len(listaDate1))]
	covid19["data"]=listaDate.copy()

	covid19.drop(["stato","codice_regione","lat","long","codice_nuts_1", "codice_nuts_2","note","note_test","note_casi"], axis=1, inplace=True)

	covid19.set_index("denominazione_regione",inplace=True)

	#Prendiamo tutte le date da inizio pandemia
	date=covid19["data"]

	moltiplicatoreVeneto=moltiplicatoreRegione("Veneto")

	listaRegioni=["Abruzzo","Basilicata","Calabria","Campania","Emilia-Romagna","Friuli Venezia Giulia","Lazio","Liguria","Lombardia","Marche","Molise","P.A. Bolzano","P.A. Trento","Piemonte","Puglia","Sardegna","Sicilia","Toscana","Umbria","Valle d'Aosta"]

	covid19UltimoGiorno=covid19[covid19["data"]==date[-1]]
	covid19PenultimoGiorno=covid19[covid19["data"]==date[-22]]

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

	#INGRESSI GIORNALIERI IN TERAPIA INTENSIVA
	ingressiUltimoGiornoTerapiaIntensiva=covid19UltimoGiorno["terapia_intensiva"]-covid19PenultimoGiorno["terapia_intensiva"]
	ingressiUltimoGiornoTerapiaIntensivaInVeneto=ingressiUltimoGiornoTerapiaIntensiva["Veneto"]*moltiplicatoreVeneto
	ingressiUltimoGiornoTerapiaIntensivaInItalia=ingressiUltimoGiornoTerapiaIntensiva.sum()

	#INGRESSI GIORNALIERI NON IN TERAPIA INTENSIVA
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

	#lETALITA REGIONE PER REGIONE
	listaLetalitaRegioni=[]
	for regione in listaRegioni:
		listaLetalitaRegioni.append(letalitaRegione(regione,covid19,covid19UltimoGiorno))

	#------------------------------------AGGIORNAMENTO DATABASE 1----------------------------------
	listaRegioniPerDatabase=["Abruzzo","Basilicata","Calabria","Campania","EmiliaRomagna","FriuliVeneziaGiulia","Lazio","Liguria","Lombardia","Marche","Molise","AltoAdige","Trentino","Piemonte","Puglia","Sardegna","Sicilia","Toscana","Umbria","ValleDAosta"]

	rigaDaAggiungere={"Data": date[-1], "positiviMolecolariInItalia": tassoNazionalePositiviMolecolari,"positiviMolecolariInVeneto": tassoPositiviMolecolariInVeneto,"ingressiTerapiaIntensivaInItalia":ingressiUltimoGiornoTerapiaIntensivaInItalia , "ingressiTerapiaIntensivaInVeneto":ingressiUltimoGiornoTerapiaIntensivaInVeneto , "ingressiFuoriIntensivaInItalia": ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia,"ingressiFuoriIntensivaInVeneto": ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInVeneto, "decedutiInItalia": decedutiUltimoGiorno, "decedutiInVenetoPopolosoQuantoItalia":decedutiUltimoGiornoInVeneto , "letalitaItaliana": tassoDiMortalitaNazionale ,"letalitaVeneta": tassoDiMortalitaInVeneto}

	for i in range(len(listaRegioniPerDatabase)):
		rigaDaAggiungere["letalita"+str(listaRegioniPerDatabase[i])]=listaLetalitaRegioni[i]

	covid19NostroSenzaTotali=covid19NostroSenzaTotali.append(rigaDaAggiungere,ignore_index=True)

	#Creazione database con le sole date in cui nel conteggio hanno aggiunto i tamponi rapidi
	rigaDaAggiungereTotali={"Data": date[-1], "PositiviSuTotaleTamponiInItalia":rapportoPositiviTamponiUltimoGiornoInItalia, "PositiviSuTotaleTamponiInVeneto": rapportoPositiviSuTotaleTamponiUltimoGiornoInVeneto}

	covid19NostroSoloTotali=covid19NostroSoloTotali.append(rigaDaAggiungereTotali,ignore_index=True)

	df1=covid19NostroSenzaTotali.to_csv(sep=",",index=False)
	df2=covid19NostroSoloTotali.to_csv(sep=",",index=False)

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

