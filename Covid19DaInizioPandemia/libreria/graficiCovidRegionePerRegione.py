#File contentete la funzione per calcolare la letalità regione per regione e tutti i valori settimanali regione per regione 
import math
import pandas as pd

from libreria.numeroDiAbitanti import *

pd.options.mode.chained_assignment = None

#Funzione che calcola i rapporto ai tamponi totali settimanale della regione passata come input
#ARGOMENTI: 
#-regione di cui si vuole calcolare il dato
#-database della Protezione Civile pulito
#-lista delle Domeniche da inizio pandemia
#RESTITUISCE una lista contenente i valori settimanali del tasso sui tamoni totali della regione in input
def tamponiTotaliSettimanali(regione,covid19,listaDomeniche):

	listaSettimanaleTassoDiPositivitaInRegione=[]

	#I tamponi totali sono calcolati solo a partire dalla settimana dopo in 15 gennaio
	for i in range(listaDomeniche.index("17-01-2021"), len(listaDomeniche)-1):

		tamponiSettimanali = covid19[covid19['data']==listaDomeniche[i+1]]['tamponi'] - covid19[covid19['data']==listaDomeniche[i]]['tamponi']
		positiviSettimanali = covid19[covid19['data']==listaDomeniche[i+1]]['totale_casi'] - covid19[covid19['data']==listaDomeniche[i]]['totale_casi']
		rapportoSettimanale = positiviSettimanali*100/tamponiSettimanali
		rapportoSettimanaleInRegione= rapportoSettimanale[regione]
		listaSettimanaleTassoDiPositivitaInRegione.append(rapportoSettimanaleInRegione)
		
	return listaSettimanaleTassoDiPositivitaInRegione

#Funzione che calcola i rapporto ai tamponi molecolari settimanale della regione passata come input
#ARGOMENTI: 
#-regione di cui si vuole calcolare il dato
#-database della Protezione Civile pulito
#-lista delle Domeniche da inizio pandemia
#RESTITUISCE una lista contenente i valori settimanali del tasso sui tamponi molecolari della regione in input
def tamponiMolecolariSettimanaliRegione(regione,covid19,listaDomeniche):
	
	listaSettimanaleTassoDiPositivitaMolecolareInRegione=[]
	
	#-------------------------PRIMA SETTIMANA----------------------------
	tamponiMolecolariSettimanali = covid19[covid19['data']==listaDomeniche[0]]['tamponi'] 
	positiviMolecolariSettimanali= covid19[covid19['data']==listaDomeniche[0]]['totale_casi'] 
	rapportoMolecolareSettimanale = positiviMolecolariSettimanali*100/tamponiMolecolariSettimanali
	rapportoMolecolareSettimanaleInRegione= rapportoMolecolareSettimanale[regione]
	listaSettimanaleTassoDiPositivitaMolecolareInRegione.append(rapportoMolecolareSettimanaleInRegione)

	#-----------------FINO ALLA SETTIMANA PRIMA DEL 15 GENNAIO------------------------
	for i in range(listaDomeniche.index("17-01-2021")-1):
		tamponiMolecolariSettimanali = covid19[covid19['data']==listaDomeniche[i+1]]['tamponi'] - covid19[covid19['data']==listaDomeniche[i]]['tamponi']
		positiviMolecolariSettimanali= covid19[covid19['data']==listaDomeniche[i+1]]['totale_casi'] - covid19[covid19['data']==listaDomeniche[i]]['totale_casi']
		rapportoMolecolareSettimanale = positiviMolecolariSettimanali*100/tamponiMolecolariSettimanali
		rapportoMolecolareSettimanaleInRegione= rapportoMolecolareSettimanale[regione]
		listaSettimanaleTassoDiPositivitaMolecolareInRegione.append(rapportoMolecolareSettimanaleInRegione)

	#------------------------------SETTIMANA DEL 15 GENNAIO----------------------------
	tamponiMolecolariSettimanali = covid19[covid19['data']=='17-01-2021']['tamponi_test_molecolare'] - covid19[covid19['data']=='10-01-2021']['tamponi']
	positiviMolecolariSettimanali = covid19[covid19['data']=='17-01-2021']['totale_positivi_test_molecolare'] - covid19[covid19['data']=='10-01-2021']['totale_casi']
	rapportoMolecolareSettimanale= positiviMolecolariSettimanali*100/tamponiMolecolariSettimanali
	rapportoMolecolareSettimanaleInRegione= rapportoMolecolareSettimanale[regione]
	listaSettimanaleTassoDiPositivitaMolecolareInRegione.append(rapportoMolecolareSettimanaleInRegione)

	#------------------------------DALLA SETTIMANA DOPO IL 15 GENNAIO AD OGGI--------------------------
	for i in range(listaDomeniche.index("17-01-2021"),len(listaDomeniche)-1):
		tamponiMolecolariSettimanali = covid19[covid19['data']==listaDomeniche[i+1]]['tamponi_test_molecolare'] - covid19[covid19['data']==listaDomeniche[i]]['tamponi_test_molecolare']
		positiviMolecolariSettimanali=covid19[covid19['data']==listaDomeniche[i+1]]['totale_positivi_test_molecolare'] - covid19[covid19['data']==listaDomeniche[i]]['totale_positivi_test_molecolare']
		rapportoMolecolareSettimanale = positiviMolecolariSettimanali*100/tamponiMolecolariSettimanali
		rapportoMolecolareSettimanaleInRegione= rapportoMolecolareSettimanale[regione]
		listaSettimanaleTassoDiPositivitaMolecolareInRegione.append( rapportoMolecolareSettimanaleInRegione)
		
	return listaSettimanaleTassoDiPositivitaMolecolareInRegione


#Funzione che calcola la varizione settimanale delle persone ricoverate in terapia intensiva della regione passata come input
#ARGOMENTI: 
#-regione di cui si vuole calcolare il dato
#-database della Protezione Civile pulito
#-lista delle Domeniche da inizio pandemia
#-moltiplicatore della regione
#RESTITUISCE una lista contenente i valori settimanali della variazione in intensiva della regione in input
def terapieIntensiveRegione(regione,covid19,listaDomeniche,moltiplicatore):
	listaSettimanaleTerapiaIntensivaInRegione=[]

	#------------------PRIMA SETTIMANA DI PANDEMIA--------------------
	terapiaIntensivaSettimanale=covid19[covid19["data"]==listaDomeniche[0]]['terapia_intensiva']
	terapiaIntensivaSettimanaleInRegione=terapiaIntensivaSettimanale[regione]
	terapiaIntensivaSettimanaleInItalia=terapiaIntensivaSettimanale.sum()
	listaSettimanaleTerapiaIntensivaInRegione.append(terapiaIntensivaSettimanaleInRegione*moltiplicatore)
	
	#------------------ DALLA SECONDA SETTIMANA AD OGGI-------------------
	for i in range(len(listaDomeniche)-1):
		terapiaIntensivaSettimanale=covid19[covid19["data"]==listaDomeniche[i+1]]['terapia_intensiva'] - covid19[covid19["data"]==listaDomeniche[i]]['terapia_intensiva']
		terapiaIntensivaSettimanaleInRegione=terapiaIntensivaSettimanale[regione]
		listaSettimanaleTerapiaIntensivaInRegione.append(terapiaIntensivaSettimanaleInRegione*moltiplicatore)
	return listaSettimanaleTerapiaIntensivaInRegione

#Funzione che calcola la varizione settimanale delle persone ricoverate nei ricoveri ordinari della regione passata come input
#ARGOMENTI: 
#-regione di cui si vuole calcolare il dato
#-database della Protezione Civile pulito
#-lista delle Domeniche da inizio pandemia
#-moltiplicatore della regione
#RESTITUISCE una lista contenente i valori settimanali della variazione nei ricoveri ordinari della regione in input
def ricoveriRepartiOrdinariRegione(regione,covid19,listaDomeniche,moltiplicatore):
	listaSettimanaleOspedaliNonTerapiaIntensivaInRegione=[]

	#-----------------PRIMA SETTIMANA------------------------------
	totaleOspedalizzati=covid19[covid19["data"]==listaDomeniche[0]]['totale_ospedalizzati']
	terapiaIntensivaSettimanale=covid19[covid19["data"]==listaDomeniche[0]]['terapia_intensiva']
	ospedalizzatiNonIntensiva=totaleOspedalizzati-terapiaIntensivaSettimanale
	ospedalizzatiNonIntensivaInRegione=ospedalizzatiNonIntensiva[regione]
	listaSettimanaleOspedaliNonTerapiaIntensivaInRegione.append(ospedalizzatiNonIntensivaInRegione*moltiplicatore)

	#-------------DALLA SECONDA SETTIMANA IN POI----------------
	for i in range(len(listaDomeniche)-1):
		totaleOspedalizzati=covid19[covid19["data"]==listaDomeniche[i+1]]['totale_ospedalizzati']-covid19[covid19["data"]==listaDomeniche[i]]['totale_ospedalizzati']
		terapiaIntensivaSettimanale=covid19[covid19["data"]==listaDomeniche[i+1]]['terapia_intensiva']-covid19[covid19["data"]==listaDomeniche[i]]['terapia_intensiva']
		ospedalizzatiNonIntensiva=totaleOspedalizzati-terapiaIntensivaSettimanale
		ospedalizzatiNonIntensivaInRegione=ospedalizzatiNonIntensiva[regione]
		listaSettimanaleOspedaliNonTerapiaIntensivaInRegione.append(ospedalizzatiNonIntensivaInRegione*moltiplicatore)
		
	return listaSettimanaleOspedaliNonTerapiaIntensivaInRegione

#Funzione che calcola la varizione settimanale dei deceduti della regione passata come input
#ARGOMENTI: 
#-regione di cui si vuole calcolare il dato
#-database della Protezione Civile pulito
#-lista delle Domeniche da inizio pandemia
#-moltiplicatore della regione
#RESTITUISCE una lista contenente i valori settimanali del numero di deceduti della regione in input
def decedutiRegione(regione,covid19,listaDomeniche,moltiplicatore):
	listaSettimanaleDecedutiInRegione=[]

	#-----------------PRIMA SETTIMANA---------------------
	decedutiSettimanale=covid19[covid19["data"]==listaDomeniche[0]]['deceduti']
	decedutiSettimanaleInRegione=decedutiSettimanale[regione]
	listaSettimanaleDecedutiInRegione.append(decedutiSettimanaleInRegione*moltiplicatore)
	
	#-------------------DALLA SECONDA SETTIMANA AD OGGI-----------------
	for i in range(len(listaDomeniche)-1):
		decedutiSettimanale=covid19[covid19["data"]==listaDomeniche[i+1]]['deceduti']-covid19[covid19["data"]==listaDomeniche[i]]['deceduti']
		decedutiSettimanaleInRegione=decedutiSettimanale[regione]
		listaSettimanaleDecedutiInRegione.append(decedutiSettimanaleInRegione*moltiplicatore)
		
	return listaSettimanaleDecedutiInRegione

#ARGOMENTI: -regione di cui si vuole calcolare la letalità
#	    -dataFrame covid19
#	    -dataFrame con i dati del solo primo giorno di pandemia
#	    -lista di tutte le date una e una sola volta
#	    -numero di giornate di pandemia
def letalitaRegione(regione,covid19,covid19PrimoGiorno,listaDate,quanteDateCiSonoState):
	#questa sarà una lista contenente i valori della letalità della regione passata com input, giorno per giorno da inizio pandemia
	letalitaInRegione=[]
	
	#-------------------------------PRIMO GIORNO DI PANDEMIA---------------------------------
	tassoDiMortalitaPrimoGiorno=covid19PrimoGiorno["deceduti"]*100/covid19PrimoGiorno["totale_casi"]
	tassoDiMortalitaPrimoGiornoInRegione=tassoDiMortalitaPrimoGiorno[regione]
	letalitaInRegione.append(tassoDiMortalitaPrimoGiornoInRegione)
	
	#-----------------------------VALORI DAL SECONDO GIORNO AD OGGI--------------------
	for i in range(1,quanteDateCiSonoState):
		covid19UltimoGiorno=covid19[covid19["data"]==listaDate[i]]
		covid19PenultimoGiorno=covid19[covid19["data"]==listaDate[i-1]]
		tassoDiMortalita=covid19UltimoGiorno["deceduti"]*100/covid19UltimoGiorno["totale_casi"]
		tassoDiMortalitaInRegione=tassoDiMortalita[regione]
		letalitaInRegione.append(tassoDiMortalitaInRegione)
		
	return letalitaInRegione
