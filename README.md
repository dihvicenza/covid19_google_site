# Andamento dell'epidemia da Covid19

>Il progetto è parte del Operativo Regionale del Fondo Europeo di Sviluppo Regionale (POR FESR 2014 - 2020) del Veneto, nell'ambito del bando dell'azione 231 volto alla "costituzione di Innovation Lab diretti al consolidamento/sviluppo del network Centri P3@-Palestre Digitali e alla diffusione della cultura degli Open Data."

![license logo](docs/logos.png)

Il sito web (https://sites.google.com/view/datiregionveneto/dati-giornalieri?authuser=0) è suddiviso in due macroaree:

1. Dati giornalieri dove è possibile vedere i dati relativi a singole giornate
2. Andamento epidemia dove è possibile osservare l'evoluzione dei dati pandemici a partire da inizio pandemia

### 1. Dati giornalieri
In questa sezione si possono visualizzare delle mappe interattive che rappresentano l'Italia suddivisa regione per regione (Trentino e Alto-Adige sono considerate due regioni distinte) e cliccando su una regione si vede il dato relativo alla regione selezionata e il dato Italiano. Ogni regione viene colorata di bianco, giallo, arancione o rosso a seconda del valore del dato considerato. Di default viene visualizzata l'ultima giornata e dei paramentri fissati determinano la colorazione della mappa. Tuttavia, è possibile cambiare sia la data che i paramentri.

Questa sezione è suddivisa a sua volta in tre aree:

1. Tassi regione per regione
2. Ricoveri regione per regione
3. Deceduti regione per regione

#### 1.1 Tassi regione per regione
Qui vengono rappresentate due mappe:
- La prima relativa al tasso di positività su tutti i tamponi effettuati nelle 24 ore (la prima data selezionabile è il 15 gennaio 2021 perchè prima venivano conteggiati soltanto i tamponi molecolari)
- La seconda relativa al tasso di positività sui soli tamponi molecolari.

#### 1.2 Ricoveri regione per regione
Anche qui vengono rappresentate due mappe:
- La prima relativa alla variazione di ricoverati in terapia intensiva (il dato italiano è diviso per 21 in modo tale da confrontare ogni regione con la media regionale)
- La seconda relativa alla variazione di ricoverati nei reparti ordinari (il dato italiano è diviso per 21 in modo tale da confrontare ogni regione con la media regionale)

#### 1.3 Deceduti regione per regione
Qui viene visulizzata una sola mappa che rappresenta il numero di deceduti (il dato italiano è diviso per 21 in modo tale da confrontare ogni regione con la media regionale)

### 2. Andamento epidemia
In questa sezione si possono visualizzare dei grafici interattivi che rappresentano l'evoluzione del virus nel tempo. 
Questa parte è suddivisa a sua volta in tre sezioni:
- La prima sezione è relativa ai dati giornalieri
- La seconda sezione è relativa ai dati settimanali
- La terza sezione è relativa alla letalità

#### 2.1 Dati giornalieri
Qui vengono rappresentati 5 grafici interattivi:
- Il primo è realitvo alla percentuale di positivi su tutti i tamponi effettuati nell'ultima giornata(sono presenti due linee: una rossa per il tasso di positività veneto e una blu per quello italiano). Questo grafico è l'unico che non parte da inizio pandemia, ma comincia dal 15 gennaio 2021, giacché precedentemente venivano conteggiati soltanto i tampini molecolari.
- Il secondo è realitvo alla percentuale di positivi sui soli tamponi molecolari effettuati nell'ultima giornata (sono presenti due linee: una rossa per il tasso di positività veneto e una blu per quello italiano).
- Il terzo è relativo alla variazione di ricoveri in terapia intensiva rispetto al giorno precedente. In questo caso il valore veneto è moltiplicato per il rapporto tra la popolazione italiana e quella veneta, ovvero circa 12.2. Questo perché a differenza dei grafici precedenti, non vengono rappresentate percentuali, bensì valori assoluti e il confronto tra il valore italiano e quello veneto sarebbe privo di significato. In questo modo viene confrontato il dato italiano con una stima del dato veneto supponendolo popoloso quanto l'Italia.
- Il quarto è relativo alla variazione di ricoveri nei reparti ordinari rispetto al giorno precedente. Anche in questo caso, per lo stesso motivo, il valore veneto è moltiplicato per il rapporto tra la popolazione italiana e quella veneta, ovvero circa 12.2. 
-  Il quinto è relativo al numero di deceduti nell'ultima giornata. Anche in questo caso, per lo stesso motivo, il valore veneto è moltiplicato per il rapporto tra la popolazione italiana e quella veneta, ovvero circa 12.2. 

#### 2.2 Dati settimanali
Anche qui vengono rappresentati 5 grafici interattivi, ma a differenza dei precedenti i dati non si riferiscono all'ultima giornata, ma all'ultima settimana (da lunedì a domenica) in modo da visualizzare meglio l'andamento ed evitare le fisiologiche oscillazioni giornaliere. Inoltre non confrontiamo solamente Italia e Veneto, ma diamo la possibilità di confrontare tra loro tutte le regioni. Di default i grafici rappresentano il confronto Italia/Veneto, ma tutte le regioni sono selezionabili e deselezionabili.
 Il primo grafico è realitvo alla percentuale di positivi su tutti i tamponi effettuati nell'ultima settimana. Questo grafico è l'unico che non parte dalla prima settimana di pandemia, ma comincia dalla settimana 17-24 gennaio 2021, giacché prima del 15 gennaio venivano conteggiati soltanto i tampini molecolari.
- Il secondo è realitvo alla percentuale di positivi sui soli tamponi molecolari effettuati nell'ultima settimana.
- Il terzo è relativo alla variazione di ricoveri in terapia intensiva rispetto alla settimana precedente. In questo caso i dati regionali sono moltiplicati per il rapporto tra la popolazione italiana e la popolazione della regione considerata. Questo perché a differenza dei grafici precedenti, non vengono rappresentate percentuali, bensì valori assoluti e il confronto tra le varie regioni risentirebbe della popolazione delle stesse. In questo modo vengono stimati i dati regionali, supponendo tutte le regioni popolose quanto l'Italia.
- Il quarto è relativo alla variazione di ricoveri nei reparti ordinari rispetto alla settimana precedente. Anche in questo caso, per lo stesso motivo, i valori regionali sono moltiplicati per il rapporto tra la popolazione italiana e quella della regione considerata. 
-  Il quinto è relativo al numero di deceduti nell'ultima settimana. Anche in questo caso, per lo stesso motivo, i valori regionali sono moltiplicati per il rapporto tra la popolazione italiana e quella della regione considerata.

#### 2.3 Letalità
Qui viene rappresentato soltanto un grafico interattivo che rappresenta la letalità dell'italia e di ciascuna regione (di default viene visualizzato il grafico italiano e quello veneto). Per ogni giornato il valore rappresentato è calcolato come rapporto percentuale tra tutti i deceduti a causa del coronavirus da inizio pandemia e il numero totale di positivi riscontrati fino a quel giorno.




