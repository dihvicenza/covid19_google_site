import pandas as pd
#import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None
from libreria.numeroDiAbitanti import *
from libreria.graficiCovidRegionePerRegione import *

from github import Github, InputGitTreeElement
from datetime import date
from os import environ



def graficiSettimanali():
	covid19 = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv",sep=",")

	covid19['data']=(pd.to_datetime(covid19["data"]))
	covid19=covid19.fillna(0)
	listaDate1=list(pd.to_datetime(covid19["data"]))
	listaDate=[listaDate1[i].strftime("%d-%m-%Y") for i in range(len(listaDate1))]

	covid19["data"]=listaDate.copy()
	covid19.drop(["stato","codice_regione","lat","long","codice_nuts_1", "codice_nuts_2","note","note_test","note_casi"], axis=1, inplace=True)
	covid19.set_index("denominazione_regione",inplace=True)

	listaDatePulita= listaDate[::21] 
	listaDomeniche=listaDatePulita[6::7]

	listaRegioni=["Abruzzo","Basilicata","Calabria","Campania","Emilia-Romagna","Friuli Venezia Giulia","Lazio","Liguria","Lombardia","Marche","Molise","P.A. Bolzano","P.A. Trento","Piemonte","Puglia","Sardegna","Sicilia","Toscana","Umbria","Valle d'Aosta"]

	listaMoltiplicatori=[moltiplicatoreRegione(regione) for regione in listaRegioni]


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

	#INGRESSI GIORNALIERI IN TERAPIA INTENSIVA
	listaSettimanaleTerapiaIntensivaInItalia=[]
	listaSettimanaleTerapiaIntensivaInVeneto=[]

	terapiaIntensivaSettimanale=covid19[covid19["data"]==listaDomeniche[0]]['terapia_intensiva']
	terapiaIntensivaSettimanaleInVeneto=terapiaIntensivaSettimanale["Veneto"]
	terapiaIntensivaSettimanaleInItalia=terapiaIntensivaSettimanale.sum()
	listaSettimanaleTerapiaIntensivaInVeneto.append(terapiaIntensivaSettimanaleInVeneto*moltiplicatore)
	listaSettimanaleTerapiaIntensivaInItalia.append(terapiaIntensivaSettimanaleInItalia)

	#INGRESSI GIORNALIERI NON IN TERAPIA INTENSIVA
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

	for i in range(listaDomeniche.index("17-01-2021")-1):
		#tamponi molecolari
		tamponiMolecolariSettimanali = covid19[covid19['data']==listaDomeniche[i+1]]['tamponi'] - covid19[covid19['data']==listaDomeniche[i]]['tamponi']
		positiviMolecolariSettimanali= covid19[covid19['data']==listaDomeniche[i+1]]['totale_casi'] - covid19[covid19['data']==listaDomeniche[i]]['totale_casi']
		rapportoMolecolareSettimanale = positiviMolecolariSettimanali*100/tamponiMolecolariSettimanali
		rapportoMolecolareSettimanaleInVeneto= rapportoMolecolareSettimanale["Veneto"]
		rapportoMolecolareSettimanaleInItalia = positiviMolecolariSettimanali.sum()*100/tamponiMolecolariSettimanali.sum()
		listaSettimanaleTassoDiPositivitaMolecolareInVeneto.append(rapportoMolecolareSettimanaleInVeneto)
		listaSettimanaleTassoDiPositivitaMolecolareInItalia.append(rapportoMolecolareSettimanaleInItalia)

		#ingressi in intensiva
		terapiaIntensivaSettimanale=covid19[covid19["data"]==listaDomeniche[i+1]]['terapia_intensiva'] - covid19[covid19["data"]==listaDomeniche[i]]['terapia_intensiva']
		terapiaIntensivaSettimanaleInVeneto=terapiaIntensivaSettimanale["Veneto"]
		terapiaIntensivaSettimanaleInItalia=terapiaIntensivaSettimanale.sum()
		listaSettimanaleTerapiaIntensivaInVeneto.append(terapiaIntensivaSettimanaleInVeneto*moltiplicatore)
		listaSettimanaleTerapiaIntensivaInItalia.append(terapiaIntensivaSettimanaleInItalia)

		#ingressi non intensiva
		totaleOspedalizzati=covid19[covid19["data"]==listaDomeniche[i+1]]['totale_ospedalizzati']-covid19[covid19["data"]==listaDomeniche[i]]['totale_ospedalizzati']
		terapiaIntensivaSettimanale=covid19[covid19["data"]==listaDomeniche[i+1]]['terapia_intensiva']-covid19[covid19["data"]==listaDomeniche[i]]['terapia_intensiva']
		ospedalizzatiNonIntensiva=totaleOspedalizzati-terapiaIntensivaSettimanale
		ospedalizzatiNonIntensivaInVeneto=ospedalizzatiNonIntensiva["Veneto"]
		ospedalizzatiNonIntensivaInItalia=ospedalizzatiNonIntensiva.sum()
		listaSettimanaleOspedaliNonIntensivaInItalia.append(ospedalizzatiNonIntensivaInItalia)
		listaSettimanaleOspedaliNonTerapiaIntensivaInVeneto.append(ospedalizzatiNonIntensivaInVeneto*moltiplicatore)

		#deceduti		
		decedutiSettimanale=covid19[covid19["data"]==listaDomeniche[i+1]]['deceduti']-covid19[covid19["data"]==listaDomeniche[i]]['deceduti']
		decedutiSettimanaleInVeneto=decedutiSettimanale["Veneto"]
		decedutiSettimanaleInItalia=decedutiSettimanale.sum()
		listaSettimanaleDecedutiInVeneto.append(decedutiSettimanaleInVeneto*moltiplicatore)
		listaSettimanaleDecedutiInItalia.append(decedutiSettimanaleInItalia)


	#-------------------------------SETTIMANA MISTA--------------------------------
	#tamponi molecolari
	tamponiMolecolariSettimanali = covid19[covid19['data']=='17-01-2021']['tamponi_test_molecolare'] - covid19[covid19['data']=='10-01-2021']['tamponi']
	positiviMolecolariSettimanali = covid19[covid19['data']=='17-01-2021']['totale_positivi_test_molecolare'] - covid19[covid19['data']=='10-01-2021']['totale_casi']
	rapportoMolecolareSettimanale= positiviMolecolariSettimanali*100/tamponiMolecolariSettimanali
	rapportoMolecolareSettimanaleInVeneto= rapportoMolecolareSettimanale["Veneto"]
	rapportoMolecolareSettimanaleInItalia = positiviMolecolariSettimanali.sum()*100/tamponiMolecolariSettimanali.sum()
	listaSettimanaleTassoDiPositivitaMolecolareInVeneto.append(rapportoMolecolareSettimanaleInVeneto)
	listaSettimanaleTassoDiPositivitaMolecolareInItalia.append(rapportoMolecolareSettimanaleInItalia)

	#ingressi in intensiva
	terapiaIntensivaSettimanale=covid19[covid19["data"]=='17-01-2021']['terapia_intensiva'] - covid19[covid19["data"]=='10-01-2021']['terapia_intensiva']
	terapiaIntensivaSettimanaleInVeneto=terapiaIntensivaSettimanale["Veneto"]
	terapiaIntensivaSettimanaleInItalia=terapiaIntensivaSettimanale.sum()
	listaSettimanaleTerapiaIntensivaInVeneto.append(terapiaIntensivaSettimanaleInVeneto*moltiplicatore)
	listaSettimanaleTerapiaIntensivaInItalia.append(terapiaIntensivaSettimanaleInItalia)

	#ingressi non intensiva
	totaleOspedalizzati=covid19[covid19["data"]=='17-01-2021']['totale_ospedalizzati']-covid19[covid19["data"]=='10-01-2021']['totale_ospedalizzati']
	terapiaIntensivaSettimanale=covid19[covid19["data"]=='17-01-2021']['terapia_intensiva']-covid19[covid19["data"]==listaDomeniche[i]]['terapia_intensiva']
	ospedalizzatiNonIntensiva=totaleOspedalizzati-terapiaIntensivaSettimanale
	ospedalizzatiNonIntensivaInVeneto=ospedalizzatiNonIntensiva["Veneto"]
	ospedalizzatiNonIntensivaInItalia=ospedalizzatiNonIntensiva.sum()
	listaSettimanaleOspedaliNonIntensivaInItalia.append(ospedalizzatiNonIntensivaInItalia)
	listaSettimanaleOspedaliNonTerapiaIntensivaInVeneto.append(ospedalizzatiNonIntensivaInVeneto*moltiplicatore)

	#deceduti		
	decedutiSettimanale=covid19[covid19["data"]=='17-01-2021']['deceduti']-covid19[covid19["data"]=='10-01-2021']['deceduti']
	decedutiSettimanaleInVeneto=decedutiSettimanale["Veneto"]
	decedutiSettimanaleInItalia=decedutiSettimanale.sum()
	listaSettimanaleDecedutiInVeneto.append(decedutiSettimanaleInVeneto*moltiplicatore)
	listaSettimanaleDecedutiInItalia.append(decedutiSettimanaleInItalia)

	#---------------------dal 15 gennaio in po---------------------------
	for i in range(listaDomeniche.index("17-01-2021"), len(listaDomeniche)-1):
		#tamponi molecolari
		tamponiMolecolariSettimanali = covid19[covid19['data']==listaDomeniche[i+1]]['tamponi_test_molecolare'] - covid19[covid19['data']==listaDomeniche[i]]['tamponi_test_molecolare']
		positiviMolecolariSettimanali=covid19[covid19['data']==listaDomeniche[i+1]]['totale_positivi_test_molecolare'] - covid19[covid19['data']==listaDomeniche[i]]['totale_positivi_test_molecolare']
		rapportoMolecolareSettimanale = positiviMolecolariSettimanali*100/tamponiMolecolariSettimanali
		rapportoMolecolareSettimanaleInVeneto= rapportoMolecolareSettimanale["Veneto"]
		rapportoMolecolareSettimanaleInItalia = positiviMolecolariSettimanali.sum()*100/tamponiMolecolariSettimanali.sum()
		listaSettimanaleTassoDiPositivitaMolecolareInVeneto.append( rapportoMolecolareSettimanaleInVeneto)
		listaSettimanaleTassoDiPositivitaMolecolareInItalia.append(rapportoMolecolareSettimanaleInItalia)

		#tampooni totali
		tamponiSettimanali = covid19[covid19['data']==listaDomeniche[i+1]]['tamponi'] - covid19[covid19['data']==listaDomeniche[i]]['tamponi']
		positiviSettimanali = covid19[covid19['data']==listaDomeniche[i+1]]['totale_casi'] - covid19[covid19['data']==listaDomeniche[i]]['totale_casi']
		rapportoSettimanale = positiviSettimanali*100/tamponiSettimanali
		rapportoSettimanaleInVeneto= rapportoSettimanale["Veneto"]
		rapportoSettimanaleInItalia = positiviSettimanali.sum()*100/tamponiSettimanali.sum()
		listaSettimanaleTassoDiPositivitaInVeneto.append(rapportoSettimanaleInVeneto)
		listaSettimanaleTassoDiPositivitaInItalia.append(rapportoSettimanaleInItalia)
		
		#ingressi in intensiva
		terapiaIntensivaSettimanale=covid19[covid19["data"]==listaDomeniche[i+1]]['terapia_intensiva'] - covid19[covid19["data"]==listaDomeniche[i]]['terapia_intensiva']
		terapiaIntensivaSettimanaleInVeneto=terapiaIntensivaSettimanale["Veneto"]
		terapiaIntensivaSettimanaleInItalia=terapiaIntensivaSettimanale.sum()
		listaSettimanaleTerapiaIntensivaInVeneto.append(terapiaIntensivaSettimanaleInVeneto*moltiplicatore)
		listaSettimanaleTerapiaIntensivaInItalia.append(terapiaIntensivaSettimanaleInItalia)

		#ingressi non intensiva
		totaleOspedalizzati=covid19[covid19["data"]==listaDomeniche[i+1]]['totale_ospedalizzati']-covid19[covid19["data"]==listaDomeniche[i]]['totale_ospedalizzati']
		terapiaIntensivaSettimanale=covid19[covid19["data"]==listaDomeniche[i+1]]['terapia_intensiva']-covid19[covid19["data"]==listaDomeniche[i]]['terapia_intensiva']

		ospedalizzatiNonIntensiva=totaleOspedalizzati-terapiaIntensivaSettimanale
		ospedalizzatiNonIntensivaInVeneto=ospedalizzatiNonIntensiva["Veneto"]
		ospedalizzatiNonIntensivaInItalia=ospedalizzatiNonIntensiva.sum()
		listaSettimanaleOspedaliNonIntensivaInItalia.append(ospedalizzatiNonIntensivaInItalia)
		listaSettimanaleOspedaliNonTerapiaIntensivaInVeneto.append(ospedalizzatiNonIntensivaInVeneto*moltiplicatore)

		#deceduti		
		decedutiSettimanale=covid19[covid19["data"]==listaDomeniche[i+1]]['deceduti']-covid19[covid19["data"]==listaDomeniche[i]]['deceduti']
		decedutiSettimanaleInVeneto=decedutiSettimanale["Veneto"]
		decedutiSettimanaleInItalia=decedutiSettimanale.sum()
		listaSettimanaleDecedutiInVeneto.append(decedutiSettimanaleInVeneto*moltiplicatore)
		listaSettimanaleDecedutiInItalia.append(decedutiSettimanaleInItalia)
	

	'''
	#Grafico per il tasso di positivita ai tamponi totali
	plt.figure(figsize=(16,10))
	italia,=plt.plot(listaDomeniche[listaDomeniche.index("17-01-2021")+1:],listaSettimanaleTassoDiPositivitaInItalia,label="Italia")
	veneto,=plt.plot(listaDomeniche[listaDomeniche.index("17-01-2021")+1:],listaSettimanaleTassoDiPositivitaInVeneto,label="Veneto")
	plt.legend([veneto,italia],["Veneto","Italia"])
	plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0)
	plt.xticks(listaDomeniche[listaDomeniche.index("17-01-2021")+1::10])
	plt.title('Tasso di positivita totale')
	plt.xlabel('Date')
	plt.ylabel('Percentuale')
	plt.grid(axis='y')
	plt.show()

	#Grafico per il tasso di positivita ai tamponi totali
	plt.figure(figsize=(16,10))
	italia,=plt.plot(listaDomeniche[1:],listaSettimanaleTassoDiPositivitaMolecolareInItalia,label="Italia")
	veneto,=plt.plot(listaDomeniche[1:],listaSettimanaleTassoDiPositivitaMolecolareInVeneto,label="Veneto")
	plt.legend([veneto,italia],["Veneto","Italia"])
	plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0)
	plt.xticks(listaDomeniche[1::10])
	plt.title('Tasso di positivita molecolare')
	plt.xlabel('Date')
	plt.ylabel('Percentuale')
	plt.grid(axis='y')
	plt.show()

	#Grafico intensiva
	plt.figure(figsize=(16,10))
	italia,=plt.plot(listaDomeniche[1:],listaSettimanaleTerapiaIntensivaInItalia,label="Media regionale")
	veneto,=plt.plot(listaDomeniche[1:],listaSettimanaleTerapiaIntensivaInVeneto,label="Veneto")
	plt.legend([veneto,italia],["Veneto","Media \nRegionale"])
	plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0)
	plt.xticks(listaDomeniche[1::10])
	plt.title('Ingressi settimanali in terapia intensiva')
	plt.xlabel('Date')
	plt.ylabel('Nuove terapie intensive')
	plt.grid(axis='y')
	plt.show()

	#grafico ospdali non intensiva
	plt.figure(figsize=(16,10))
	italia,=plt.plot(listaDomeniche[1:],listaSettimanaleOspedaliNonIntensivaInItalia,label="Media regionale")
	veneto,=plt.plot(listaDomeniche[1:],listaSettimanaleOspedaliNonTerapiaIntensivaInVeneto,label="Veneto")
	plt.legend([veneto,italia],["Veneto","Media \nRegionale"])
	plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0)
	plt.xticks(listaDomeniche[1::10])
	plt.title('Ingressi giornalieri in ospendale non in terapia intensiva')
	plt.xlabel('Date')
	plt.ylabel('Nuovi ospedalizzati non intensiva')
	plt.grid(axis='y')
	plt.show()

	#deceduti grafico
	plt.figure(figsize=(16,10))
	italia,=plt.plot(listaDomeniche[1:],listaSettimanaleDecedutiInItalia,label="Media regionale")
	veneto,=plt.plot(listaDomeniche[1:],listaSettimanaleDecedutiInVeneto,label="Veneto")
	plt.legend([veneto,italia],["Veneto","Media \nRegionale"])
	plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0)
	plt.xticks(listaDomeniche[1::10])
	plt.title('Deceduti settimanali')
	plt.xlabel('Date')
	plt.ylabel('Nuovi ospedalizzati non intensiva')
	plt.grid(axis='y')
	plt.show()
	'''

	#------------------Creazione database-------------------
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

	#CSV per i soli tamponi totali
	covid19PerGraficiSettimanaliItaliaVenetoTamponiTotali=pd.DataFrame({"Data":listaDomeniche[listaDomeniche.index("24-01-2021"):]})
	covid19PerGraficiSettimanaliItaliaVenetoTamponiTotali['TassoDiPositivitaAiTamponiTotaliItalia']=listaSettimanaleTassoDiPositivitaInItalia
	covid19PerGraficiSettimanaliItaliaVenetoTamponiTotali['TassoDiPositivitaAiTamponiTotaliVeneto']=listaSettimanaleTassoDiPositivitaInVeneto


	#FACCIAMO I CALCOLI REGIONE PER REGIONE E METTIAMO NEI DATABASE
	for i in range(len(listaRegioniPerDatabase)):

		#Molecolari
		covid19PerGraficiSettimanaliItaliaVeneto["tassoDiPositivitaAiTamponiMolecolari"+str(listaRegioniPerDatabase[i])]=tamponiMolecolariSettimanaliRegione(listaRegioni[i],covid19,listaDomeniche)

		#intensiva
		covid19PerGraficiSettimanaliItaliaVeneto["ingressiInTerapiaIntensiva"+str(listaRegioniPerDatabase[i])]=terapieIntensiveRegione(listaRegioni[i],covid19,listaDomeniche,listaMoltiplicatori[i])

		#non intensiva
		covid19PerGraficiSettimanaliItaliaVeneto["ingressiNeiRepartiOrdinari"+str(listaRegioniPerDatabase[i])]=ricoveriRepartiOrdinariRegione(listaRegioni[i],covid19,listaDomeniche,listaMoltiplicatori[i])

		#deceduti
		covid19PerGraficiSettimanaliItaliaVeneto["deceduti"+str(listaRegioniPerDatabase[i])]=decedutiRegione(listaRegioni[i],covid19,listaDomeniche,listaMoltiplicatori[i])

		#Tamponi totali
		covid19PerGraficiSettimanaliItaliaVenetoTamponiTotali["TassoDiPostitivitaAiTamponiTotali"+str(listaRegioniPerDatabase[i])]=tamponiTotaliSettimanali(listaRegioni[i],covid19,listaDomeniche)


	#------------------------------COMMIT TO GITHUB-----------------------------------
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
