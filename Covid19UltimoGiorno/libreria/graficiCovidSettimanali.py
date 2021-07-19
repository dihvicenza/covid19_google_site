#File per l'aggiunta dei dati relativi all'ultima settimana ai csv contenenti i dati settimanali generati dal file "graficiCovidSettimanali.py" nella cartella "covid19DaInizioPandemia/libreria" 
#Per i commenti dettagliati leggere il file graficiCovid.py di questa cartella 

import pandas as pd
import os
from os import environ
from github import Github, InputGitTreeElement
from datetime import date as dateImport
import datetime

from libreria.numeroDiAbitanti import *
from libreria.graficiCovidRegionePerRegione import *

pd.options.mode.chained_assignment = None

#Funzione chiamata da application per leggere il csv della protezione civile, elaborarne i dati, aggiungere una riga ai nostri csv settimanali e ripusharli nella cartella pubblica "Covid" di github
def graficiSettimanali():
	
	oggi=dateImport.today().weekday() #Su oggi c'è un numero che ci dice in che giorno della settimana siamo (0 per lunedì, 6 per domenica) 
	
	#Questo codice deve partire solo la domenica, quindi se oggi==6
	if oggi ==6:
		ultimaDomenica=dateImport.today() #prendiamo la data dell'ultima domenica (coincidente con la data nel quale si lancia il programma)
		variazione=datetime.timedelta(7) #Per risalire alla domenica precedente bisogna tornare indietro di 7 giorni 
		penultimaDomenica=(ultimaDomenica-variazione).strftime("%d-%m-%Y") #Scriviamo quindi la data dell'ultima domenica nel formato dd-mm-yyyy
		ultimaDomenica=ultimaDomenica.strftime("%d-%m-%Y") #Format gradevole anche per l'ultima domenica

		covid19 = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv",sep=",") #Lettura del file della Protezione Civile
		covid19NostroSenzaTotali=pd.read_csv("https://raw.githubusercontent.com/DigitalChriAri/Covid/main/Covid19GraficiSettimanaliItaliaEVeneto.csv", sep=",") #Lettura del nostro csv senza tamponi totali
		covid19NostroSoloTotali = pd.read_csv("https://raw.githubusercontent.com/DigitalChriAri/Covid/main/Covid19GraficiSettimanaliTamponiTotaliItaliaEVeneto.csv", sep=",") #Lettura del nostro csv con i tamponi totali


		covid19['data']=(pd.to_datetime(covid19["data"]))
		covid19=covid19.fillna(0)
		
		listaDate1=list(pd.to_datetime(covid19["data"]))
		listaDate=[listaDate1[i].strftime("%d-%m-%Y") for i in range(len(listaDate1))]
		covid19["data"]=listaDate.copy()
		
		covid19.drop(["stato","codice_regione","lat","long","codice_nuts_1", "codice_nuts_2","note","note_test","note_casi"], axis=1, inplace=True)

		covid19.set_index("denominazione_regione",inplace=True)

		date=covid19["data"] #Prendiamo tutte le date da inizio pandemia
		listaRegioni=["Abruzzo","Basilicata","Calabria","Campania","Emilia-Romagna","Friuli Venezia Giulia","Lazio","Liguria","Lombardia","Marche","Molise","P.A. Bolzano","P.A. Trento","Piemonte","Puglia","Sardegna","Sicilia","Toscana","Umbria","Valle d'Aosta"]
		moltiplicatoreVeneto=moltiplicatoreRegione("Veneto")

		#TAMPONI TOTALI
		tamponiSettimanali = covid19[covid19['data']==ultimaDomenica]['tamponi'] - covid19[covid19['data']==penultimaDomenica]['tamponi']
		positiviSettimanali = covid19[covid19['data']==ultimaDomenica]['totale_casi'] - covid19[covid19['data']==penultimaDomenica]['totale_casi']
		rapportoSettimanale = positiviSettimanali*100/tamponiSettimanali
		rapportoSettimanaleInVeneto= rapportoSettimanale["Veneto"]
		rapportoSettimanaleInItalia = positiviSettimanali.sum()*100/tamponiSettimanali.sum()
		    
		#TAMPONI MOLECOLARI
		tamponiMolecolariSettimanali = covid19[covid19['data']==ultimaDomenica]['tamponi_test_molecolare'] - covid19[covid19['data']==penultimaDomenica]['tamponi_test_molecolare']
		positiviMolecolariSettimanali=covid19[covid19['data']==ultimaDomenica]['totale_positivi_test_molecolare'] - covid19[covid19['data']==penultimaDomenica]['totale_positivi_test_molecolare']
		rapportoMolecolareSettimanale = positiviMolecolariSettimanali*100/tamponiMolecolariSettimanali
		rapportoMolecolareSettimanaleInVeneto= rapportoMolecolareSettimanale["Veneto"]
		rapportoMolecolareSettimanaleInItalia = positiviMolecolariSettimanali.sum()*100/tamponiMolecolariSettimanali.sum()


		#TERAPIE INTENSIVE
		terapiaIntensivaSettimanale=covid19[covid19["data"]==ultimaDomenica]['terapia_intensiva'] - covid19[covid19["data"]==penultimaDomenica]['terapia_intensiva']
		terapiaIntensivaSettimanaleInVeneto=terapiaIntensivaSettimanale["Veneto"]*moltiplicatoreVeneto
		terapiaIntensivaSettimanaleInItalia=terapiaIntensivaSettimanale.sum()

		#RICOVERI ORDINARI
		ospedalizzatiFuoriIntensiva=covid19[covid19["data"]==ultimaDomenica]['ricoverati_con_sintomi']-covid19[covid19["data"]==penultimaDomenica]['ricoverati_con_sintomi']
		ospedalizzatiNonIntensivaInVeneto=ospedalizzatiFuoriIntensiva["Veneto"]*moltiplicatoreVeneto
		ospedalizzatiNonIntensivaInItalia=ospedalizzatiFuoriIntensiva.sum()


		#DECEDUTI SUPPONENDO IL VENETO POPOLOSO QUANTO L'ITALIA
		decedutiSettimanale=covid19[covid19["data"]==ultimaDomenica]['deceduti']-covid19[covid19["data"]==penultimaDomenica]['deceduti']
		decedutiSettimanaleInVeneto=decedutiSettimanale["Veneto"]*moltiplicatoreVeneto
		decedutiSettimanaleInItalia=decedutiSettimanale.sum()


		#------------------------------------AGGIORNAMENTO DATABASE SENZA TOTALI----------------------------------

		#lista per database
		listaRegioniPerDatabase=["Abruzzo","Basilicata","Calabria","Campania","EmiliaRomagna","FriuliVeneziaGiulia","Lazio","Liguria","Lombardia","Marche","Molise","AltoAdige","Trentino","Piemonte","Puglia","Sardegna","Sicilia","Toscana","Umbria","ValleDAosta"]

		rigaDaAggiungereSenzaTotali={"Data": ultimaDomenica, "tassoDiPositivitaAiTamponiMolecolariItalia": rapportoMolecolareSettimanaleInItalia,'tassoDiPositivitaAiTamponiMolecolariVeneto': rapportoMolecolareSettimanaleInVeneto,'ingressiInTerapiaIntensivaMediaRegionale':terapiaIntensivaSettimanaleInItalia, 'ingressiInTerapiaIntensivaVeneto':terapiaIntensivaSettimanaleInVeneto , 'ingressiNeiRepartiOrdinariMediaRegionale': ospedalizzatiNonIntensivaInItalia,'ingressiNeiRepartiOrdinariVeneto': ospedalizzatiNonIntensivaInVeneto, 'decedutiItalia': decedutiSettimanaleInItalia, 'decedutiVeneto':decedutiSettimanaleInVeneto}

		#------------------------------------AGGIORNAMENTO DATABASE CON I TAMPONI TOTALI----------------------------------

		rigaDaAggiungereSoloTotali={"Data": ultimaDomenica,'TassoDiPositivitaAiTamponiTotaliItalia': rapportoSettimanaleInItalia,'TassoDiPositivitaAiTamponiTotaliVeneto':rapportoSettimanaleInVeneto }

		#--------------------------------------------------------CALCOLI REGIONE PER REGIONE---------------------------------------------
		for i in range(len(listaRegioniPerDatabase)):
			#La funzione "moltiplicatoreRegione" presente nel file numeroDiAbitanti.py calcola il rapporto tra la popolazione italiana e la popolazione della regione passata come input
			moltiplicatore=moltiplicatoreRegione(listaRegioni[i]) 
			
			#Per calcolare ogni dato e inserirlo come value della chiave corrispondente nel dizionario rigaDaAggiungere, dobbiamo chiamare
			#la corrispondente funzione presente nel file covid19RegionePerRegione passandogli il nome della regione.
			#Chiamandole con listaRegioni[i] all'interno di questo ciclo for riesco a ottenere i valori per ogni regione.
			
			#tamponi totali
			rigaDaAggiungereSoloTotali["TassoDiPostitivitaAiTamponiTotali"+str(listaRegioniPerDatabase[i])]=tamponiTotaliSettimanali(listaRegioni[i],covid19,ultimaDomenica,penultimaDomenica)

			#tamponi molecolari
			rigaDaAggiungereSenzaTotali["tassoDiPositivitaAiTamponiMolecolari"+str(listaRegioniPerDatabase[i])]=tamponiMolecolariSettimanaliRegione(listaRegioni[i],covid19,ultimaDomenica,penultimaDomenica)

			#intensiva
			rigaDaAggiungereSenzaTotali["ingressiInTerapiaIntensiva"+str(listaRegioniPerDatabase[i])]=terapieIntensiveRegione(listaRegioni[i],covid19,ultimaDomenica,penultimaDomenica,moltiplicatore)

			#non intensiva
			rigaDaAggiungereSenzaTotali["ingressiNeiRepartiOrdinari"+str(listaRegioniPerDatabase[i])]=ricoveriRepartiOrdinariRegione(listaRegioni[i],covid19,ultimaDomenica,penultimaDomenica,moltiplicatore)

			#deceduti
			rigaDaAggiungereSenzaTotali["deceduti"+str(listaRegioniPerDatabase[i])]=decedutiRegione(listaRegioni[i],covid19,ultimaDomenica,penultimaDomenica,moltiplicatore)

		#Aggiungiamo la riga giusta al database giusto
		covid19NostroSenzaTotali=covid19NostroSenzaTotali.append(rigaDaAggiungereSenzaTotali,ignore_index=True)
		covid19NostroSoloTotali=covid19NostroSoloTotali.append(rigaDaAggiungereSoloTotali,ignore_index=True)
		
		
		#----------------------------------------PUSH GITHUB--------------------------------------

		df1=covid19NostroSenzaTotali.to_csv(sep=",",index=False)
		df2=covid19NostroSoloTotali.to_csv(sep=",",index=False)

		fileList=[df1,df2]
		fileNames=["Covid19GraficiSettimanaliItaliaEVeneto.csv","Covid19GraficiSettimanaliTamponiTotaliItaliaEVeneto.csv"]

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
		
		print("Aggiornamento settimanale completato")
