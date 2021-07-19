#In questo file calcolo il moltiplicatore per ogni regione (ovvero il rapporto tra popolazione italiana e popolazione regionale)
import pandas as pd

#Leggiamo il csv della Protezione Civile contenente la popolazione delle regioni
databasePopolazione= pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-statistici-riferimento/popolazione-istat-regione-range.csv", sep=",")

numeroDiAbitantiItaliani=datebasePopolazione["totale_generale"].sum() #Totale popolazione italiana

#Funzione che calcola il moltiplicatore della regione passata come input
def moltiplicatoreRegione(regione):
	#Nel database considerato le regioni non si chiamano "P.A. Trento" e "P.A. Bolzano", ma "Trento" e "Bolzano"
	if regione=="P.A. Trento":
		regione="Trento"
	if regione=="P.A. Bolzano":
		regione="Bolzano"
		
	popolazioneRegione=databasePopolazione[databasePopolazione["denominazione_regione"]==regione]
	numeroDiAbitantiRegione=popolazioneRegione["totale_generale"].sum()
	moltiplicatore=numeroDiAbitantiItaliani/numeroDiAbitantiRegione
	print("Gli italiani sono "+str(moltiplicatore)+" volte gli abitanti di "+str(regione))
	
	return moltiplicatore
