#In questo file calcolo il numero di abitanti in Italia e in Veneto sulla base del file platea che si trova su github nella cartella dei vaccini. Da qui ricavo il numero di abitanti aventi un età dai 12 anni in su. Il numero di abitanti è quello che si ricava dall'ultimo aggiornamento del file platea
import pandas as pd

vacciniPlatea= pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-statistici-riferimento/popolazione-istat-regione-range.csv", sep=",")

numeroDiAbitantiItaliani=vacciniPlatea["totale_generale"].sum()

#Calcoliamo il moltiplicatore per ogni regione
def moltiplicatoreRegione(regione):
	if regione=="P.A. Trento":
		regione="Trento"
	if regione=="P.A. Bolzano":
		regione="Bolzano"
	vacciniPlateaRegione=vacciniPlatea[vacciniPlatea["denominazione_regione"]==regione]
	numeroDiAbitantiRegione=vacciniPlateaRegione["totale_generale"].sum()
	moltiplicatore=numeroDiAbitantiItaliani/numeroDiAbitantiRegione
	print("Gli italiani sono "+str(moltiplicatore)+" volte gli abitanti di "+str(regione))
	
	return moltiplicatore
