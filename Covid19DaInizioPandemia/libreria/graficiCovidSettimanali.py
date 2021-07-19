#file csv per dati settimanali da inizio pandemia
#Per i commenti dettagliati leggere il file graficiCovid.py
import pandas as pd
from github import Github, InputGitTreeElement
from datetime import date
from os import environ

from libreria.numeroDiAbitanti import *
from libreria.graficiCovidRegionePerRegione import *

pd.options.mode.chained_assignment = None

#Funzione chiamata da application per leggere il csv della Protezione Civile, elaborarne i dati, generare due nuovi csv e pusharli nella cartella pubblica "Covid" di github
def graficiSettimanali():
	
	covid19 = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv",sep=",")#per leggere il csv della protezione civile
	covid19['data']=(pd.to_datetime(covid19["data"]))
	covid19=covid19.fillna(0)
	listaDate1=list(pd.to_datetime(covid19["data"]))
	listaDate=[listaDate1[i].strftime("%d-%m-%Y") for i in range(len(listaDate1))]

	covid19["data"]=listaDate.copy()
	covid19.drop(["stato","codice_regione","lat","long","codice_nuts_1", "codice_nuts_2","note","note_test","note_casi"], axis=1, inplace=True)
	covid19.set_index("denominazione_regione",inplace=True)

	listaDatePulita= listaDate[::21]#lista con le date una sola volta
	listaDomeniche=listaDatePulita[6::7]#lista delle domeniche da inizio pandemia

	listaRegioni=["Abruzzo","Basilicata","Calabria","Campania","Emilia-Romagna","Friuli Venezia Giulia","Lazio","Liguria","Lombardia","Marche","Molise","P.A. Bolzano","P.A. Trento","Piemonte","Puglia","Sardegna","Sicilia","Toscana","Umbria","Valle d'Aosta"]

	#lista contenente i moltiplicatori (rapporto tra popolazione italiana e regionale) di ciascuna regione
	#La funzione moltiplicatoreRegione è presente nel file numeroDiAbitanti.py
	listaMoltiplicatori=[moltiplicatoreRegione(regione) for regione in listaRegioni]
	
	#-------------------------------------------------------PRIMA SETTIMANA-----------------------------------------------------------
	#In tutte le sottrazioni il minuendo è il dato relativo ad una domenica e il sottraendo è il dato relativo alla domenica precedente
	
	#TASSO TAMPONI MOLECOLARI
	listaSettimanaleTassoDiPositivitaMolecolareInVeneto=[]
	listaSettimanaleTassoDiPositivitaMolecolareInItalia=[]
	tamponiMolecolariSettimanali = covid19[covid19['data']==listaDomeniche[0]]['tamponi'] 
	positiviMolecolariSettimanali= covid19[covid19['data']==listaDomeniche[0]]['totale_casi'] 
	rapportoMolecolareSettimanale = positiviMolecolariSettimanali*100/tamponiMolecolariSettimanali
	rapportoMolecolareSettimanaleInVeneto= rapportoMolecolareSettimanale["Veneto"]
	rapportoMolecolareSettimanaleInItalia = positiviMolecolariSettimanali.sum()*100/tamponiMolecolariSettimanali.sum()
	listaSettimanaleTassoDiPositivitaMolecolareInVeneto.append(rapportoMolecolareSettimanaleInVeneto)
	listaSettimanaleTassoDiPositivitaMolecolareInItalia.append(rapportoMolecolareSettimanaleInItalia)  
	
	#POSITIVI SU TAMPONI TOTALI
	listaSettimanaleTassoDiPositivitaInVeneto=[]
	listaSettimanaleTassoDiPositivitaInItalia=[]

	#INGRESSI IN TERAPIA INTENSIVA
	listaSettimanaleTerapiaIntensivaInItalia=[]
	listaSettimanaleTerapiaIntensivaInVeneto=[]
	terapiaIntensivaSettimanale=covid19[covid19["data"]==listaDomeniche[0]]['terapia_intensiva']
	terapiaIntensivaSettimanaleInVeneto=terapiaIntensivaSettimanale["Veneto"]
	terapiaIntensivaSettimanaleInItalia=terapiaIntensivaSettimanale.sum()
	listaSettimanaleTerapiaIntensivaInVeneto.append(terapiaIntensivaSettimanaleInVeneto*moltiplicatore)
	listaSettimanaleTerapiaIntensivaInItalia.append(terapiaIntensivaSettimanaleInItalia)

	#INGRESSI NEI REPARTI ORDINARI
	#la colonna totale_ospedalizzati indica il numero di persone presenti in ospedale (sia in intensiva che nei reparti ordinari)
	listaSettimanaleOspedaliNonIntensivaInItalia=[]
	listaSettimanaleOspedaliNonTerapiaIntensivaInVeneto=[]
	totaleOspedalizzati=covid19[covid19["data"]==listaDomeniche[0]]['totale_ospedalizzati']
	terapiaIntensivaSettimanale=covid19[covid19["data"]==listaDomeniche[0]]['terapia_intensiva']
	ospedalizzatiNonIntensiva=totaleOspedalizzati-terapiaIntensivaSettimanale
	ospedalizzatiNonIntensivaInVeneto=ospedalizzatiNonIntensiva["Veneto"]
	ospedalizzatiNonIntensivaInItalia=ospedalizzatiNonIntensiva.sum()
	listaSettimanaleOspedaliNonIntensivaInItalia.append(ospedalizzatiNonIntensivaInItalia)
	listaSettimanaleOspedaliNonTerapiaIntensivaInVeneto.append(ospedalizzatiNonIntensivaInVeneto*moltiplicatore)

	#DECEDUTI
	listaSettimanaleDecedutiInItalia=[]
	listaSettimanaleDecedutiInVeneto=[]
	decedutiSettimanale=covid19[covid19["data"]==listaDomeniche[0]]['deceduti']
	decedutiSettimanaleInVeneto=decedutiSettimanale["Veneto"]
	decedutiSettimanaleInItalia=decedutiSettimanale.sum()
	listaSettimanaleDecedutiInVeneto.append(decedutiSettimanaleInVeneto*moltiplicatore)
	listaSettimanaleDecedutiInItalia.append(decedutiSettimanaleInItalia)
	
	#------------------------------------FINO ALLA SETTIMANA PRIMA DI QUELLA CONTENENTE IL 14 GENNAIO 2021-----------------------------
	for i in range(listaDomeniche.index("17-01-2021")-1):
		
		#TAMPONI MOLECOLARI
		tamponiMolecolariSettimanali = covid19[covid19['data']==listaDomeniche[i+1]]['tamponi'] - covid19[covid19['data']==listaDomeniche[i]]['tamponi']
		positiviMolecolariSettimanali= covid19[covid19['data']==listaDomeniche[i+1]]['totale_casi'] - covid19[covid19['data']==listaDomeniche[i]]['totale_casi']
		rapportoMolecolareSettimanale = positiviMolecolariSettimanali*100/tamponiMolecolariSettimanali
		rapportoMolecolareSettimanaleInVeneto= rapportoMolecolareSettimanale["Veneto"]
		rapportoMolecolareSettimanaleInItalia = positiviMolecolariSettimanali.sum()*100/tamponiMolecolariSettimanali.sum()
		listaSettimanaleTassoDiPositivitaMolecolareInVeneto.append(rapportoMolecolareSettimanaleInVeneto)
		listaSettimanaleTassoDiPositivitaMolecolareInItalia.append(rapportoMolecolareSettimanaleInItalia)

		#INGRESSI IN INTENSIVA
		terapiaIntensivaSettimanale=covid19[covid19["data"]==listaDomeniche[i+1]]['terapia_intensiva'] - covid19[covid19["data"]==listaDomeniche[i]]['terapia_intensiva']
		terapiaIntensivaSettimanaleInVeneto=terapiaIntensivaSettimanale["Veneto"]
		terapiaIntensivaSettimanaleInItalia=terapiaIntensivaSettimanale.sum()
		listaSettimanaleTerapiaIntensivaInVeneto.append(terapiaIntensivaSettimanaleInVeneto*moltiplicatore)
		listaSettimanaleTerapiaIntensivaInItalia.append(terapiaIntensivaSettimanaleInItalia)

		#INGRESSI NEI REPARTI ORDINARI
		totaleOspedalizzati=covid19[covid19["data"]==listaDomeniche[i+1]]['totale_ospedalizzati']-covid19[covid19["data"]==listaDomeniche[i]]['totale_ospedalizzati']
		terapiaIntensivaSettimanale=covid19[covid19["data"]==listaDomeniche[i+1]]['terapia_intensiva']-covid19[covid19["data"]==listaDomeniche[i]]['terapia_intensiva']
		ospedalizzatiNonIntensiva=totaleOspedalizzati-terapiaIntensivaSettimanale
		ospedalizzatiNonIntensivaInVeneto=ospedalizzatiNonIntensiva["Veneto"]
		ospedalizzatiNonIntensivaInItalia=ospedalizzatiNonIntensiva.sum()
		listaSettimanaleOspedaliNonIntensivaInItalia.append(ospedalizzatiNonIntensivaInItalia)
		listaSettimanaleOspedaliNonTerapiaIntensivaInVeneto.append(ospedalizzatiNonIntensivaInVeneto*moltiplicatore)

		#DECEDUTI		
		decedutiSettimanale=covid19[covid19["data"]==listaDomeniche[i+1]]['deceduti']-covid19[covid19["data"]==listaDomeniche[i]]['deceduti']
		decedutiSettimanaleInVeneto=decedutiSettimanale["Veneto"]
		decedutiSettimanaleInItalia=decedutiSettimanale.sum()
		listaSettimanaleDecedutiInVeneto.append(decedutiSettimanaleInVeneto*moltiplicatore)
		listaSettimanaleDecedutiInItalia.append(decedutiSettimanaleInItalia)


	#--------------------------------------------------SETTIMANA CONTENENTE IL 15 DI GENNAIO----------------------------------------------
	
	#TAMPONI MOLEOLARI
	tamponiMolecolariSettimanali = covid19[covid19['data']=='17-01-2021']['tamponi_test_molecolare'] - covid19[covid19['data']=='10-01-2021']['tamponi']
	positiviMolecolariSettimanali = covid19[covid19['data']=='17-01-2021']['totale_positivi_test_molecolare'] - covid19[covid19['data']=='10-01-2021']['totale_casi']
	rapportoMolecolareSettimanale= positiviMolecolariSettimanali*100/tamponiMolecolariSettimanali
	rapportoMolecolareSettimanaleInVeneto= rapportoMolecolareSettimanale["Veneto"]
	rapportoMolecolareSettimanaleInItalia = positiviMolecolariSettimanali.sum()*100/tamponiMolecolariSettimanali.sum()
	listaSettimanaleTassoDiPositivitaMolecolareInVeneto.append(rapportoMolecolareSettimanaleInVeneto)
	listaSettimanaleTassoDiPositivitaMolecolareInItalia.append(rapportoMolecolareSettimanaleInItalia)

	#INGRESSI IN INTENSIVA
	terapiaIntensivaSettimanale=covid19[covid19["data"]=='17-01-2021']['terapia_intensiva'] - covid19[covid19["data"]=='10-01-2021']['terapia_intensiva']
	terapiaIntensivaSettimanaleInVeneto=terapiaIntensivaSettimanale["Veneto"]
	terapiaIntensivaSettimanaleInItalia=terapiaIntensivaSettimanale.sum()
	listaSettimanaleTerapiaIntensivaInVeneto.append(terapiaIntensivaSettimanaleInVeneto*moltiplicatore)
	listaSettimanaleTerapiaIntensivaInItalia.append(terapiaIntensivaSettimanaleInItalia)

	#INGRESSI NEI REPARTI ORDINARI
	totaleOspedalizzati=covid19[covid19["data"]=='17-01-2021']['totale_ospedalizzati']-covid19[covid19["data"]=='10-01-2021']['totale_ospedalizzati']
	terapiaIntensivaSettimanale=covid19[covid19["data"]=='17-01-2021']['terapia_intensiva']-covid19[covid19["data"]==listaDomeniche[i]]['terapia_intensiva']
	ospedalizzatiNonIntensiva=totaleOspedalizzati-terapiaIntensivaSettimanale
	ospedalizzatiNonIntensivaInVeneto=ospedalizzatiNonIntensiva["Veneto"]
	ospedalizzatiNonIntensivaInItalia=ospedalizzatiNonIntensiva.sum()
	listaSettimanaleOspedaliNonIntensivaInItalia.append(ospedalizzatiNonIntensivaInItalia)
	listaSettimanaleOspedaliNonTerapiaIntensivaInVeneto.append(ospedalizzatiNonIntensivaInVeneto*moltiplicatore)

	#DECEDUTI		
	decedutiSettimanale=covid19[covid19["data"]=='17-01-2021']['deceduti']-covid19[covid19["data"]=='10-01-2021']['deceduti']
	decedutiSettimanaleInVeneto=decedutiSettimanale["Veneto"]
	decedutiSettimanaleInItalia=decedutiSettimanale.sum()
	listaSettimanaleDecedutiInVeneto.append(decedutiSettimanaleInVeneto*moltiplicatore)
	listaSettimanaleDecedutiInItalia.append(decedutiSettimanaleInItalia)

	#-------------------------------------DATI DALLA SETTIMANA SUCESSIVA A QUELLA CONTENTENTE IL 15 GENNAIO 2021----------------------
	for i in range(listaDomeniche.index("17-01-2021"), len(listaDomeniche)-1):
		
		#TAMPONI MOLECOLARI
		tamponiMolecolariSettimanali = covid19[covid19['data']==listaDomeniche[i+1]]['tamponi_test_molecolare'] - covid19[covid19['data']==listaDomeniche[i]]['tamponi_test_molecolare']
		positiviMolecolariSettimanali=covid19[covid19['data']==listaDomeniche[i+1]]['totale_positivi_test_molecolare'] - covid19[covid19['data']==listaDomeniche[i]]['totale_positivi_test_molecolare']
		rapportoMolecolareSettimanale = positiviMolecolariSettimanali*100/tamponiMolecolariSettimanali
		rapportoMolecolareSettimanaleInVeneto= rapportoMolecolareSettimanale["Veneto"]
		rapportoMolecolareSettimanaleInItalia = positiviMolecolariSettimanali.sum()*100/tamponiMolecolariSettimanali.sum()
		listaSettimanaleTassoDiPositivitaMolecolareInVeneto.append( rapportoMolecolareSettimanaleInVeneto)
		listaSettimanaleTassoDiPositivitaMolecolareInItalia.append(rapportoMolecolareSettimanaleInItalia)

		#TAMPONI TOTALI
		tamponiSettimanali = covid19[covid19['data']==listaDomeniche[i+1]]['tamponi'] - covid19[covid19['data']==listaDomeniche[i]]['tamponi']
		positiviSettimanali = covid19[covid19['data']==listaDomeniche[i+1]]['totale_casi'] - covid19[covid19['data']==listaDomeniche[i]]['totale_casi']
		rapportoSettimanale = positiviSettimanali*100/tamponiSettimanali
		rapportoSettimanaleInVeneto= rapportoSettimanale["Veneto"]
		rapportoSettimanaleInItalia = positiviSettimanali.sum()*100/tamponiSettimanali.sum()
		listaSettimanaleTassoDiPositivitaInVeneto.append(rapportoSettimanaleInVeneto)
		listaSettimanaleTassoDiPositivitaInItalia.append(rapportoSettimanaleInItalia)
		
		#INGRESSI IN INTENSIVA
		terapiaIntensivaSettimanale=covid19[covid19["data"]==listaDomeniche[i+1]]['terapia_intensiva'] - covid19[covid19["data"]==listaDomeniche[i]]['terapia_intensiva']
		terapiaIntensivaSettimanaleInVeneto=terapiaIntensivaSettimanale["Veneto"]
		terapiaIntensivaSettimanaleInItalia=terapiaIntensivaSettimanale.sum()
		listaSettimanaleTerapiaIntensivaInVeneto.append(terapiaIntensivaSettimanaleInVeneto*moltiplicatore)
		listaSettimanaleTerapiaIntensivaInItalia.append(terapiaIntensivaSettimanaleInItalia)

		#INGRESSI NEI REPARTI ORDINARI
		totaleOspedalizzati=covid19[covid19["data"]==listaDomeniche[i+1]]['totale_ospedalizzati']-covid19[covid19["data"]==listaDomeniche[i]]['totale_ospedalizzati']
		terapiaIntensivaSettimanale=covid19[covid19["data"]==listaDomeniche[i+1]]['terapia_intensiva']-covid19[covid19["data"]==listaDomeniche[i]]['terapia_intensiva']
		ospedalizzatiNonIntensiva=totaleOspedalizzati-terapiaIntensivaSettimanale
		ospedalizzatiNonIntensivaInVeneto=ospedalizzatiNonIntensiva["Veneto"]
		ospedalizzatiNonIntensivaInItalia=ospedalizzatiNonIntensiva.sum()
		listaSettimanaleOspedaliNonIntensivaInItalia.append(ospedalizzatiNonIntensivaInItalia)
		listaSettimanaleOspedaliNonTerapiaIntensivaInVeneto.append(ospedalizzatiNonIntensivaInVeneto*moltiplicatore)

		#DECEDUTI		
		decedutiSettimanale=covid19[covid19["data"]==listaDomeniche[i+1]]['deceduti']-covid19[covid19["data"]==listaDomeniche[i]]['deceduti']
		decedutiSettimanaleInVeneto=decedutiSettimanale["Veneto"]
		decedutiSettimanaleInItalia=decedutiSettimanale.sum()
		listaSettimanaleDecedutiInVeneto.append(decedutiSettimanaleInVeneto*moltiplicatore)
		listaSettimanaleDecedutiInItalia.append(decedutiSettimanaleInItalia)
	

	#-------------------------------------------------------------CREAZIONE DATABASE-------------------------------------------------
	listaRegioniPerDatabase=["Abruzzo","Basilicata","Calabria","Campania","EmiliaRomagna","FriuliVeneziaGiulia","Lazio","Liguria","Lombardia","Marche","Molise","AltoAdige","Trentino","Piemonte","Puglia","Sardegna","Sicilia","Toscana","Umbria","ValleDAosta"]

	#CSV CON TUTTI I DATI (ESCLUSI I TAMPONI TOTALI)
	covid19PerGraficiSettimanaliItaliaVeneto=pd.DataFrame({"Data":listaDomeniche})
	covid19PerGraficiSettimanaliItaliaVeneto['tassoDiPositivitaAiTamponiMolecolariItalia']=listaSettimanaleTassoDiPositivitaMolecolareInItalia
	covid19PerGraficiSettimanaliItaliaVeneto['tassoDiPositivitaAiTamponiMolecolariVeneto']=listaSettimanaleTassoDiPositivitaMolecolareInVeneto
	covid19PerGraficiSettimanaliItaliaVeneto['ingressiInTerapiaIntensivaMediaRegionale']=listaSettimanaleTerapiaIntensivaInItalia
	covid19PerGraficiSettimanaliItaliaVeneto['ingressiInTerapiaIntensivaVeneto']=listaSettimanaleTerapiaIntensivaInVeneto
	covid19PerGraficiSettimanaliItaliaVeneto['ingressiNeiRepartiOrdinariMediaRegionale']=listaSettimanaleOspedaliNonIntensivaInItalia
	covid19PerGraficiSettimanaliItaliaVeneto['ingressiNeiRepartiOrdinariVeneto']=listaSettimanaleOspedaliNonTerapiaIntensivaInVeneto
	covid19PerGraficiSettimanaliItaliaVeneto['decedutiItalia']=listaSettimanaleDecedutiInItalia
	covid19PerGraficiSettimanaliItaliaVeneto['decedutiVeneto']=listaSettimanaleDecedutiInVeneto

	#CSV PER I SOLI TAMPONI TOTALI
	covid19PerGraficiSettimanaliItaliaVenetoTamponiTotali=pd.DataFrame({"Data":listaDomeniche[listaDomeniche.index("24-01-2021"):]})
	covid19PerGraficiSettimanaliItaliaVenetoTamponiTotali['TassoDiPositivitaAiTamponiTotaliItalia']=listaSettimanaleTassoDiPositivitaInItalia
	covid19PerGraficiSettimanaliItaliaVenetoTamponiTotali['TassoDiPositivitaAiTamponiTotaliVeneto']=listaSettimanaleTassoDiPositivitaInVeneto

	#FACCIAMO I CALCOLI REGIONE PER REGIONE E METTIAMO NEI DATABASE
	for i in range(len(listaRegioniPerDatabase)):

		#Molecolari
		covid19PerGraficiSettimanaliItaliaVeneto["tassoDiPositivitaAiTamponiMolecolari"+str(listaRegioniPerDatabase[i])]=tamponiMolecolariSettimanaliRegione(listaRegioni[i],covid19,listaDomeniche)

		#intensiva
		covid19PerGraficiSettimanaliItaliaVeneto["ingressiInTerapiaIntensiva"+str(listaRegioniPerDatabase[i])]=terapieIntensiveRegione(listaRegioni[i],covid19,listaDomeniche,listaMoltiplicatori[i])

		#ricoveri ordinari
		covid19PerGraficiSettimanaliItaliaVeneto["ingressiNeiRepartiOrdinari"+str(listaRegioniPerDatabase[i])]=ricoveriRepartiOrdinariRegione(listaRegioni[i],covid19,listaDomeniche,listaMoltiplicatori[i])

		#deceduti
		covid19PerGraficiSettimanaliItaliaVeneto["deceduti"+str(listaRegioniPerDatabase[i])]=decedutiRegione(listaRegioni[i],covid19,listaDomeniche,listaMoltiplicatori[i])

		#Tamponi totali
		covid19PerGraficiSettimanaliItaliaVenetoTamponiTotali["TassoDiPostitivitaAiTamponiTotali"+str(listaRegioniPerDatabase[i])]=tamponiTotaliSettimanali(listaRegioni[i],covid19,listaDomeniche)


	#----------------------------------------------------COMMIT TO GITHUB--------------------------------------------------------------
	df1=covid19PerGraficiSettimanaliItaliaVeneto.to_csv(sep=",",index=False)
	df2=covid19PerGraficiSettimanaliItaliaVenetoTamponiTotali.to_csv(sep=",",index=False)

	fileList=[df1,df2]
	fileNames=["Covid19GraficiSettimanaliItaliaEVeneto.csv","Covid19GraficiSettimanaliTamponiTotaliItaliaEVeneto.csv"]

	commitMessage=date.today().strftime("%d-%m-%Y")
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
