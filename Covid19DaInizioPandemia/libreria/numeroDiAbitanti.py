#In questo file calcolo il numero di abitanti in Italia e in ciascuna regione in modo tale da calcolare il rapporto tra gli abitanti italiani e quelli di ciascuna regione

import pandas as pd

#Leggiamo il file contenente gli abitanti di ciascuna regione
databasePopolazione= pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-statistici-riferimento/popolazione-istat-regione-range.csv", sep=",")

numeroDiAbitantiItaliani=databasePopolazione["totale_generale"].sum() #totale abitanti italiani
popolazioneVeneta=databasePopolazione[databasePopolazione["denominazione_regione"]=="Veneto"] #database contenente solo i dati veneti
numeroDiAbitantiVeneti=popolazioneVeneta["totale_generale"].sum() #Totale abitanti veneti
moltiplicatore=numeroDiAbitantiItaliani/numeroDiAbitantiVeneti #rapporto italia/veneto

#Funzione per calcolare il moltiplicatore della regione passata come argomento
def moltiplicatoreRegione(regione):
	#Nel database considerato le regioni non si chiamano "P.A. Trento" e "P.A. Bolzano", ma "Trento" e "Bolzano"
	if regione=="P.A. Trento":
		regione="Trento"
	if regione=="P.A. Bolzano":
		regione="Bolzano"
	popolazioneRegione=databasePopolazione[databasePopolazione["denominazione_regione"]==regione] #Dati della regione 
	numeroDiAbitantiRegione=popolazioneRegione["totale_generale"].sum() #Popolazione italiana
	moltiplicatore=numeroDiAbitantiItaliani/numeroDiAbitantiRegione #Rapporto
	print("Gli italiani sono "+str(moltiplicatore)+" volte gli abitanti di "+str(regione))
	return moltiplicatore

