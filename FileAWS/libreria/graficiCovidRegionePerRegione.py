#Funzioni che mi fanno le liste con i dati settimanali sul covid di una determinata regione passata come parametro

import math
import pandas as pd
pd.options.mode.chained_assignment = None
import os
from libreria.numeroDiAbitanti import *


def tamponiTotaliSettimanali(regione,covid19,ultimaDomenica, penultimaDomenica):

	tamponiSettimanali = covid19[covid19['data']==ultimaDomenica]['tamponi'] - covid19[covid19['data']==penultimaDomenica]['tamponi']
	positiviSettimanali = covid19[covid19['data']==ultimaDomenica]['totale_casi'] - covid19[covid19['data']==penultimaDomenica]['totale_casi']
	rapportoSettimanale = positiviSettimanali*100/tamponiSettimanali
	rapportoSettimanaleInRegione= rapportoSettimanale[regione]

	return rapportoSettimanaleInRegione


def tamponiMolecolariSettimanaliRegione(regione,covid19,ultimaDomenica, penultimaDomenica):
	
	tamponiMolecolariSettimanali = covid19[covid19['data']==ultimaDomenica]['tamponi_test_molecolare'] - covid19[covid19['data']==penultimaDomenica]['tamponi_test_molecolare']
	positiviMolecolariSettimanali=covid19[covid19['data']==ultimaDomenica]['totale_positivi_test_molecolare'] - covid19[covid19['data']==penultimaDomenica]['totale_positivi_test_molecolare']
	rapportoMolecolareSettimanale = positiviMolecolariSettimanali*100/tamponiMolecolariSettimanali
	rapportoMolecolareSettimanaleInRegione= rapportoMolecolareSettimanale[regione]

	return rapportoMolecolareSettimanaleInRegione


#Terapie intensive
def terapieIntensiveRegione(regione,covid19,ultimaDomenica, penultimaDomenica, moltiplicatore):

	terapiaIntensivaSettimanale=covid19[covid19["data"]==ultimaDomenica]['terapia_intensiva'] - covid19[covid19["data"]==penultimaDomenica]['terapia_intensiva']
	terapiaIntensivaSettimanaleInRegione=terapiaIntensivaSettimanale[regione]*moltiplicatore

	return terapiaIntensivaSettimanaleInRegione


#Terapie non intensive
def ricoveriRepartiOrdinariRegione(regione,covid19,ultimaDomenica, penultimaDomenica,moltiplicatore):

	ospedalizzatiSenzaIntensiva=covid19[covid19["data"]==ultimaDomenica]['ricoverati_con_sintomi']-covid19[covid19["data"]==penultimaDomenica]['ricoverati_con_sintomi']
	ospedalizzatiNonIntensivaInRegione=ospedalizzatiSenzaIntensiva[regione]*moltiplicatore

	return ospedalizzatiNonIntensivaInRegione

def decedutiRegione(regione,covid19,ultimaDomenica, penultimaDomenica,moltiplicatore):

	decedutiSettimanale=covid19[covid19["data"]==ultimaDomenica]['deceduti']-covid19[covid19["data"]==penultimaDomenica]['deceduti']
	decedutiSettimanaleInRegione=decedutiSettimanale[regione]*moltiplicatore

	return decedutiSettimanaleInRegione

def letalitaRegione(regione,covid19,covid19UltimoGiorno):
	tassoDiMortalita=covid19UltimoGiorno["deceduti"]*100/covid19UltimoGiorno["totale_casi"]
	tassoDiMortalitaInRegione=tassoDiMortalita[regione]
	return tassoDiMortalitaInRegione
