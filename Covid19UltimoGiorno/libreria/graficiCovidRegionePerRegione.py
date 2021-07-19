#File contenente la funzione per calcolare la letalità e tutti gli altri valori settimanali regione per regione 

import math
import pandas as pd
import os

from libreria.numeroDiAbitanti import *

pd.options.mode.chained_assignment = None

# La funzione calcola il tasso di positività a tutti i tamponi nell'ultima settimana di pandemia per una sola regione e ha come argomenti:
# -La regione di cui si vuole calcolare il valore
# -Il dataframe della Protezione Civile pulito
# -La data dell'ultima domenica di pandemia
# -La data della penultima domenica di pandemia

def tamponiTotaliSettimanali(regione,covid19,ultimaDomenica, penultimaDomenica):

	tamponiSettimanali = covid19[covid19['data']==ultimaDomenica]['tamponi'] - covid19[covid19['data']==penultimaDomenica]['tamponi']
	positiviSettimanali = covid19[covid19['data']==ultimaDomenica]['totale_casi'] - covid19[covid19['data']==penultimaDomenica]['totale_casi']
	rapportoSettimanale = positiviSettimanali*100/tamponiSettimanali
	rapportoSettimanaleInRegione= rapportoSettimanale[regione]

	return rapportoSettimanaleInRegione

# La funzione calcola il tasso di positività ai soli tamponi molecolari nell'ultima settimana di pandemia per una sola regione e ha come argomenti:
# -La regione di cui si vuole calcolare il valore
# -Il dataframe della Protezione Civile pulito
# -La data dell'ultima domenica di pandemia
# -La data della penultima domenica di pandemia
def tamponiMolecolariSettimanaliRegione(regione,covid19,ultimaDomenica, penultimaDomenica):
	
	tamponiMolecolariSettimanali = covid19[covid19['data']==ultimaDomenica]['tamponi_test_molecolare'] - covid19[covid19['data']==penultimaDomenica]['tamponi_test_molecolare']
	positiviMolecolariSettimanali=covid19[covid19['data']==ultimaDomenica]['totale_positivi_test_molecolare'] - covid19[covid19['data']==penultimaDomenica]['totale_positivi_test_molecolare']
	rapportoMolecolareSettimanale = positiviMolecolariSettimanali*100/tamponiMolecolariSettimanali
	rapportoMolecolareSettimanaleInRegione= rapportoMolecolareSettimanale[regione]

	return rapportoMolecolareSettimanaleInRegione


# La funzione calcola la variazione di ricoverati in terapia intensiva rispetto alla settimana precedente per una sola regione e ha come argomenti:
# -La regione di cui si vuole calcolare il valore
# -Il dataframe della Protezione Civile pulito
# -La data dell'ultima domenica di pandemia
# -La data della penultima domenica di pandemia
# -Il rapporto tra gli abitanti italiani e gli abitanti della regione considerata
def terapieIntensiveRegione(regione,covid19,ultimaDomenica, penultimaDomenica, moltiplicatore):

	terapiaIntensivaSettimanale=covid19[covid19["data"]==ultimaDomenica]['terapia_intensiva'] - covid19[covid19["data"]==penultimaDomenica]['terapia_intensiva']
	terapiaIntensivaSettimanaleInRegione=terapiaIntensivaSettimanale[regione]*moltiplicatore

	return terapiaIntensivaSettimanaleInRegione


# La funzione calcola la variazione di ricoverati nei reparti ordinari rispetto alla settimana precedente per una sola regione e ha come argomenti:
# -La regione di cui si vuole calcolare il valore
# -Il dataframe della Protezione Civile pulito
# -La data dell'ultima domenica di pandemia
# -La data della penultima domenica di pandemia
# -Il rapporto tra gli abitanti italiani e gli abitanti della regione considerata
def ricoveriRepartiOrdinariRegione(regione,covid19,ultimaDomenica, penultimaDomenica,moltiplicatore):

	ospedalizzatiSenzaIntensiva=covid19[covid19["data"]==ultimaDomenica]['ricoverati_con_sintomi']-covid19[covid19["data"]==penultimaDomenica]['ricoverati_con_sintomi']
	ospedalizzatiNonIntensivaInRegione=ospedalizzatiSenzaIntensiva[regione]*moltiplicatore

	return ospedalizzatiNonIntensivaInRegione


# La funzione calcola il numero di deceduti nell'ultima settimana per una sola regione e ha come argomenti:
# -La regione di cui si vuole calcolare il valore
# -Il dataframe della Protezione Civile pulito
# -La data dell'ultima domenica di pandemia
# -La data della penultima domenica di pandemia
# -Il rapporto tra gli abitanti italiani e gli abitanti della regione considerata
def decedutiRegione(regione,covid19,ultimaDomenica, penultimaDomenica,moltiplicatore):

	decedutiSettimanale=covid19[covid19["data"]==ultimaDomenica]['deceduti']-covid19[covid19["data"]==penultimaDomenica]['deceduti']
	decedutiSettimanaleInRegione=decedutiSettimanale[regione]*moltiplicatore

	return decedutiSettimanaleInRegione


# La funzione calcola la letalità da inizio pandemia per una sola regione e ha come argomenti:
# -La regione di cui si vuole calcolare il valore
# -Il dataframe della Protezione Civile pulito
# -Il dataframe con i soli dati dell'ultimo giorno di pandemia
def letalitaRegione(regione,covid19,covid19UltimoGiorno):
	tassoDiMortalita=covid19UltimoGiorno["deceduti"]*100/covid19UltimoGiorno["totale_casi"]
	tassoDiMortalitaInRegione=tassoDiMortalita[regione]
	return tassoDiMortalitaInRegione
