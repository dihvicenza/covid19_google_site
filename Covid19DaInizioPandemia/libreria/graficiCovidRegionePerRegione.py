#File contentete la funzione per calcolare la letalità regione per regione
import math
import pandas as pd

from libreria.numeroDiAbitanti import *

pd.options.mode.chained_assignment = None

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
