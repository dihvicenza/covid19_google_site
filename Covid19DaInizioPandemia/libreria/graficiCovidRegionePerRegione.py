#Funzioni che mi fanno le liste con i dati settimanali sul covid di una determinata regione passata come parametro
import math
import pandas as pd
pd.options.mode.chained_assignment = None
from libreria.numeroDiAbitanti import *


def tamponiTotaliSettimanali(regione,covid19,listaDomeniche):

	#Positivi su tutti i tamponi
	listaSettimanaleTassoDiPositivitaInRegione=[]

	for i in range(listaDomeniche.index("17-01-2021"), len(listaDomeniche)-1):

		tamponiSettimanali = covid19[covid19['data']==listaDomeniche[i+1]]['tamponi'] - covid19[covid19['data']==listaDomeniche[i]]['tamponi']
		positiviSettimanali = covid19[covid19['data']==listaDomeniche[i+1]]['totale_casi'] - covid19[covid19['data']==listaDomeniche[i]]['totale_casi']

		rapportoSettimanale = positiviSettimanali*100/tamponiSettimanali
		rapportoSettimanaleInRegione= rapportoSettimanale[regione]

		listaSettimanaleTassoDiPositivitaInRegione.append(rapportoSettimanaleInRegione)
	return listaSettimanaleTassoDiPositivitaInRegione


def tamponiMolecolariSettimanaliRegione(regione,covid19,listaDomeniche):
	
	#Tasso di positivita ai tamponi molecolari
	listaSettimanaleTassoDiPositivitaMolecolareInRegione=[]
	

	tamponiMolecolariSettimanali = covid19[covid19['data']==listaDomeniche[0]]['tamponi'] 
	positiviMolecolariSettimanali= covid19[covid19['data']==listaDomeniche[0]]['totale_casi'] 

	rapportoMolecolareSettimanale = positiviMolecolariSettimanali*100/tamponiMolecolariSettimanali
	rapportoMolecolareSettimanaleInRegione= rapportoMolecolareSettimanale[regione]

	listaSettimanaleTassoDiPositivitaMolecolareInRegione.append(rapportoMolecolareSettimanaleInRegione)

	for i in range(listaDomeniche.index("17-01-2021")-1):
		tamponiMolecolariSettimanali = covid19[covid19['data']==listaDomeniche[i+1]]['tamponi'] - covid19[covid19['data']==listaDomeniche[i]]['tamponi']

		positiviMolecolariSettimanali= covid19[covid19['data']==listaDomeniche[i+1]]['totale_casi'] - covid19[covid19['data']==listaDomeniche[i]]['totale_casi']
		    
		rapportoMolecolareSettimanale = positiviMolecolariSettimanali*100/tamponiMolecolariSettimanali
		rapportoMolecolareSettimanaleInRegione= rapportoMolecolareSettimanale[regione]
		listaSettimanaleTassoDiPositivitaMolecolareInRegione.append(rapportoMolecolareSettimanaleInRegione)

	#settimanaMista
	tamponiMolecolariSettimanali = covid19[covid19['data']=='17-01-2021']['tamponi_test_molecolare'] - covid19[covid19['data']=='10-01-2021']['tamponi']
	positiviMolecolariSettimanali = covid19[covid19['data']=='17-01-2021']['totale_positivi_test_molecolare'] - covid19[covid19['data']=='10-01-2021']['totale_casi']

	rapportoMolecolareSettimanale= positiviMolecolariSettimanali*100/tamponiMolecolariSettimanali

	rapportoMolecolareSettimanaleInRegione= rapportoMolecolareSettimanale[regione]
	listaSettimanaleTassoDiPositivitaMolecolareInRegione.append(rapportoMolecolareSettimanaleInRegione)

	#Settimane dal 15 in poi
	for i in range(listaDomeniche.index("17-01-2021"),len(listaDomeniche)-1):
		tamponiMolecolariSettimanali = covid19[covid19['data']==listaDomeniche[i+1]]['tamponi_test_molecolare'] - covid19[covid19['data']==listaDomeniche[i]]['tamponi_test_molecolare']

		positiviMolecolariSettimanali=covid19[covid19['data']==listaDomeniche[i+1]]['totale_positivi_test_molecolare'] - covid19[covid19['data']==listaDomeniche[i]]['totale_positivi_test_molecolare']

		rapportoMolecolareSettimanale = positiviMolecolariSettimanali*100/tamponiMolecolariSettimanali
		rapportoMolecolareSettimanaleInRegione= rapportoMolecolareSettimanale[regione]
		listaSettimanaleTassoDiPositivitaMolecolareInRegione.append( rapportoMolecolareSettimanaleInRegione)
	return listaSettimanaleTassoDiPositivitaMolecolareInRegione


#Terapie intensive
def terapieIntensiveRegione(regione,covid19,listaDomeniche,moltiplicatore):
	listaSettimanaleTerapiaIntensivaInRegione=[]

	terapiaIntensivaSettimanale=covid19[covid19["data"]==listaDomeniche[0]]['terapia_intensiva']
	terapiaIntensivaSettimanaleInRegione=terapiaIntensivaSettimanale[regione]
	terapiaIntensivaSettimanaleInItalia=terapiaIntensivaSettimanale.sum()
	listaSettimanaleTerapiaIntensivaInRegione.append(terapiaIntensivaSettimanaleInRegione*moltiplicatore)
	for i in range(len(listaDomeniche)-1):
		terapiaIntensivaSettimanale=covid19[covid19["data"]==listaDomeniche[i+1]]['terapia_intensiva'] - covid19[covid19["data"]==listaDomeniche[i]]['terapia_intensiva']
		terapiaIntensivaSettimanaleInRegione=terapiaIntensivaSettimanale[regione]
		listaSettimanaleTerapiaIntensivaInRegione.append(terapiaIntensivaSettimanaleInRegione*moltiplicatore)
	return listaSettimanaleTerapiaIntensivaInRegione


	#Terapie non intensive

def ricoveriRepartiOrdinariRegione(regione,covid19,listaDomeniche,moltiplicatore):
	listaSettimanaleOspedaliNonTerapiaIntensivaInRegione=[]


	totaleOspedalizzati=covid19[covid19["data"]==listaDomeniche[0]]['totale_ospedalizzati']
	terapiaIntensivaSettimanale=covid19[covid19["data"]==listaDomeniche[0]]['terapia_intensiva']
	ospedalizzatiNonIntensiva=totaleOspedalizzati-terapiaIntensivaSettimanale
	ospedalizzatiNonIntensivaInRegione=ospedalizzatiNonIntensiva[regione]
	listaSettimanaleOspedaliNonTerapiaIntensivaInRegione.append(ospedalizzatiNonIntensivaInRegione*moltiplicatore)

	for i in range(len(listaDomeniche)-1):
		totaleOspedalizzati=covid19[covid19["data"]==listaDomeniche[i+1]]['totale_ospedalizzati']-covid19[covid19["data"]==listaDomeniche[i]]['totale_ospedalizzati']
		terapiaIntensivaSettimanale=covid19[covid19["data"]==listaDomeniche[i+1]]['terapia_intensiva']-covid19[covid19["data"]==listaDomeniche[i]]['terapia_intensiva']

		ospedalizzatiNonIntensiva=totaleOspedalizzati-terapiaIntensivaSettimanale

		ospedalizzatiNonIntensivaInRegione=ospedalizzatiNonIntensiva[regione]
		listaSettimanaleOspedaliNonTerapiaIntensivaInRegione.append(ospedalizzatiNonIntensivaInRegione*moltiplicatore)
	return listaSettimanaleOspedaliNonTerapiaIntensivaInRegione

def decedutiRegione(regione,covid19,listaDomeniche,moltiplicatore):
	listaSettimanaleDecedutiInRegione=[]

	decedutiSettimanale=covid19[covid19["data"]==listaDomeniche[0]]['deceduti']
	decedutiSettimanaleInRegione=decedutiSettimanale[regione]
	listaSettimanaleDecedutiInRegione.append(decedutiSettimanaleInRegione*moltiplicatore)
	for i in range(len(listaDomeniche)-1):
		decedutiSettimanale=covid19[covid19["data"]==listaDomeniche[i+1]]['deceduti']-covid19[covid19["data"]==listaDomeniche[i]]['deceduti']
		decedutiSettimanaleInRegione=decedutiSettimanale[regione]
		listaSettimanaleDecedutiInRegione.append(decedutiSettimanaleInRegione*moltiplicatore)
	return listaSettimanaleDecedutiInRegione

def letalitaRegione(regione,covid19,covid19PrimoGiorno,listaDate,quanteDateCiSonoState):
	letalitaInRegione=[]
	tassoDiMortalitaPrimoGiorno=covid19PrimoGiorno["deceduti"]*100/covid19PrimoGiorno["totale_casi"]
	tassoDiMortalitaPrimoGiornoInRegione=tassoDiMortalitaPrimoGiorno[regione]
	letalitaInRegione.append(tassoDiMortalitaPrimoGiornoInRegione)

	for i in range(1,quanteDateCiSonoState):
		covid19UltimoGiorno=covid19[covid19["data"]==listaDate[i]]
		covid19PenultimoGiorno=covid19[covid19["data"]==listaDate[i-1]]
		tassoDiMortalita=covid19UltimoGiorno["deceduti"]*100/covid19UltimoGiorno["totale_casi"]
		tassoDiMortalitaInRegione=tassoDiMortalita[regione]
		letalitaInRegione.append(tassoDiMortalitaInRegione)
	return letalitaInRegione
