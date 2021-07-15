import pandas as pd


vaccini=pd.read_csv("https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.csv", sep=",")
vacciniPlatea= pd.read_csv("https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/platea.csv", sep=",")

print(vaccini.info())

#print(list(vaccini["fornitore"]))
print(vacciniPlatea.info())
print(vacciniPlatea.head(20))
print(vaccini.head(20)["fascia_anagrafica"])


numeroDiOttantenni=vacciniPlatea[vacciniPlatea["fascia_anagrafica"]=="80+"]['totale_popolazione'].sum()
print("Numero di 80-89",numeroDiOttantenni)

#Janssen=

secondaDose= vaccini[(vaccini['fascia_anagrafica']=='80-89') | (vaccini['fascia_anagrafica']=='90+')]['seconda_dose'].sum()
Janssen=vaccini[((vaccini['fornitore']=="Janssen") & (vaccini['fascia_anagrafica']=="80-89")) | ( (vaccini['fornitore']=="Janssen") & (vaccini['fascia_anagrafica']=="90+"))]['prima_dose'].sum()
secondaDoseEJanssen= secondaDose+Janssen
print(secondaDose)
print(Janssen)
print("Seconda dose + janssen",secondaDoseEJanssen)

primaDose=vaccini[vaccini['fascia_anagrafica']=='70-79']['prima_dose'].sum()
primaDoseSenzaJanssen=primaDose-Janssen
print("Prima dose",primaDoseSenzaJanssen)
