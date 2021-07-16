# Andamento dell'epidemia da Covid19

>Il progetto è parte del Programma Operativo Regionale del Fondo Europeo di Sviluppo Regionale (POR FESR 2014 - 2020) del Veneto, nell'ambito del bando dell'azione 231 volto alla "costituzione di Innovation Lab diretti al consolidamento/sviluppo del network Centri P3@-Palestre Digitali e alla diffusione della cultura degli Open Data."

![license logo](docs/logos.png)

## Indice

1. [Struttura del sito](#struttura-del-sito)
2. [Struttura della repository](#struttura-della-repository)
3. [OpenData utilizzati](#opendata-utilizzati)
4. [Funzionamento della webapp](#funzionamento-della-webapp)
5. [Hardware e software necessari](#hardware-e-software-necessari)



## Struttura del sito
Il sito web (https://sites.google.com/view/datiregionveneto/dati-giornalieri?authuser=0) è suddiviso in due macroaree:

1. Dati giornalieri dove è possibile vedere i dati relativi a singole giornate
2. Andamento epidemia dove è possibile osservare l'evoluzione dei dati pandemici a partire da inizio pandemia

Il sito si aggiorna in maniera automatica ogni giorno alle ore 19:00

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


## Struttura della repository


    - Covid19DaInizioPandemia # Cartella con il codice per generare i csv da inizio pandemia 
      - .venv # environment per utilizzare flask e generare i requirements.txt
      - libreria # Sottocartella con i vari file di codice python
        - graficiCovid.py # File per creare i csv con i dati giorno per giorno
        - graficiCovidRegionePerRegione.py # File con le funzioni per calcolare i dati settimanali regione per regione
        - graficiCovidSettimanali.py # File con la funzione per creare i csv con i dati settimanali
        - mappaCovid.py # File per creare i csv da inizio pandemia con i dati suddivisi regioni per regione (i csv per fare le mappe)
        - numeroDiAbitanti.py # File con le funzioni per avere il rapporto tra abitanti Italiani e delle varie regioni
      - templates 
        - update.html # File html necessario per AWS
      - applications.py # Programma principale che esegue tutto il codice
      - requirements.txt # File necessario per AWS contenente tutte le librerie python utilizzate
    - Covid19UltimoGiorno # Cartella con i codici per generare i dati dell'ultima giornata
      - .venv # environment per utilizzare flask e generare i requirements.txt
      - libreria # Sottocartella con i vari file di codice python
        - graficiCovid.py  # File per creare i csv con i dati dell'ultimo giorno 
        - graficiCovidRegionePerRegione.py # File con le funzioni per calcolare i dati dell'ultima settimana regione per regione
        - graficiCovidSettimanali.py # File con la funzione per creare i csv con i dati dell'ultima settimana
        - mappaCovid.py # File per creare i csv  con i dati dell'ultimo giorno suddivisi regioni per regione (i csv per fare le mappe)
        - numeroDiAbitanti.py # File con le funzioni per avere il rapporto tra abitanti Italiani e delle varie regioni
      - templates
        - update.html # File html necessario per AWS 
      - application.py # Programma principale che esegue tutto il codice
      - requirements.txt # File necessario per AWS contenente tutte le librerie python utilizzate
    - FileAWS # Cartella contenente soltanto i file necessari per l'esecuzione automatica su AWS
      - libreria # La stessa libreria di covid19UltimoGiorno
        - graficiCovid.py # Stesso file di covid19UltimoGiorno
        - graficiCovidRegionePerRegione.py # Stesso file di covid19UltimoGiorno
        - graficiCovidSettimanali.py # Stesso file di covid19UltimoGiorno
        - mappaCovid.py # Stesso file di covid19UltimoGiorno
        - numeroDiAbitanti.py # Stesso file di covid19UltimoGiorno
      - templates # Stesso file di covid19UltimoGiorno
        - update.htm # Stesso file di covid19UltimoGiornol
      - application.py # Stesso file di covid19UltimoGiorno
      - requirements.txt # Stesso file di covid19UltimoGiorno
    - docs # Cartella con i file e altre immagini usate in questo readme
      - logos.png # Il logo
    - templatesGoogleSite # Cartella con un html per ogni mappa o grafico
      - deceduti.html # Grafico per i deceduti giornalieri
      - decedutiSettimanali.html # Grafico per i deceduti giornalieri settimanali
      - intensiva.html # Grafico per i ricoveri in intensiva giornalieri
      - intensivaSettimanale.html # Grafico per i ricoveri in intensiva settimanali
      - letalita.html # Grafico per la letalità
      - mappaDeceduti.html # Mappa per i deceduti
      - mappaIntensiva.html # Mappa per le intensive
      - mappaNonIntensiva.html # Mappa per i ricoveri ordinari
      - mappaRapportoTamponiMolecolari.html # Mappa per il tasso di positività ai molecolari
      - mappaRapportoTamponiTotali.html # Mappa per il tasso di positività a tutti i tamponi
      - nonIntensiva.html # Grafico per i ricoveri ordinari giornalieri
      - nonIntensivaSettimanale.html # Grafico per i ricoveri ordinari settimanali
      - positiviSuMolecolari.html # Grafico per il tasso di positività giornaliero ai tamponi molecolari
      - positiviSuTotali.html # Grafico per il tasso di positività giornaliero a tutti i tamponi
      - positiviSuTotaliSettimanali.html # Grafico per il tasso di positività giornaliero ai tamponi molecolari
      - positiviSuMolecolariSettimanali.html # Grafico per il tasso di positività settimanale ai tamponi molecolari
    - README.md #Il file che state leggendo
    - italy_shape.geojson # File contenente le coordinate per disegnare la mappa dell'Italia suddivisa per regioni
    
## OpenData utilizzati 
I grafici sono stati realizzati tramite un'elaborazione degli open data pubblicati ogni pomeriggio dalla Protezione Civile e reperibili al seguente link github: https://github.com/pcm-dpc/COVID-19.

In particolare giorno per giorno utilizziamo il file denominato "dpc-covid19-ita-regioni.csv "  che si trova nella  sottocartella  "dati-regioni".

Abbiamo utilizzato anche il dataset "popolazione-istat-regione-range.csv" che si trova nella sottocartella "dati-statistici-riferimento". In quest'ultimo file abbiamo trovato il numero di abitanti regione per regione e abbiamo potuto calcolare il rapporto tra gli abitanti italiani e gli abitanti di ciascuna regione. In questo modo abbiamo potuto confrontare in maniera più significativa i dati regionali e quelli italiani relativi agli ingressi in terapia intensiva, agli ingressi nei reparti ordinari e al numero di deceduti. Infatti, abbiamo moltiplicato i dati della regione considerata per il rapporto tra la popolazione italiana e la popolazione della regione ottenendo una stima dei numeri che avrebbe avuto la regione in esame se fosse popolosa quanto l'Italia. (Senza tale calcolo il confronto non sarebbe significativo in quanto la popolazione di una singola regione è nettamente inferiore a quella italiana)

## Funzionamento della webapp
#### Cartella CovidDaInizioPandemia
In questa cartella è presente il codice che legge i csv caricati dalla Protezione Civile, ne elabora i dati, genera dei nuovi csv in cui ci sono i dati da inizio pandemia fino all'ultimo giorno che vengono utilizzati dai grafici presenti nel sito. Questi csv vengono salvati su una repository pubblica di GitHub (https://github.com/DigitalChriAri/Covid). 
I codici contenuti in questa cartella vengono eseguiti lanciando il file application.py dal terminale.

**NOTA**: Questo è già stato eseguito da noi manualmente per avere i dati completi da inizio pandemia e non necessita di essere rieseguito a meno che che non ci siano problemi o si perda qualche dato. (Per esempio se la Protezione Civile aggiorna i csv dopo le 19:00)

#### Cartella CovidUltimoGiorno
In questa cartella è presente il codice che legge i csv caricati dalla Protezione Civile, ne elabora i dati, genera un csv per la mappa relativo all'ultimo giorno e aggiorna i csv contenenti i dati settimanali e giornalieri aggiungendo una riga relativa all'ultimo giorno/settimana (la riga nel csv settimanale viene aggiunta solo di domenica).
 
La lettura e l'elaborazione dei dati deve avvenire quotidianamente dopo la pubblicazione dei dati da parte della Protezione Civile. A tal fine una cartella zip contenente i file della cartella 'FileAWS' viene caricata su AWS (Amazon Web Server, https://aws.amazon.com/console) e un chron-job (https://cron-job.org/en/) esegue il file application.py ogni giorno alle ore 19:00.

#### GoogleSite
Il sito web è stato sviluppato utilizzando la piattaforma GoogleSite. Ogni volta che è presente un grafico, questo è stato realizzato incorporando un codice html  (che si trova nella cartella templatesGoogleSite) che utilizza la libreria ChartJS di JavaScript. Questo codice legge dalla nostra repository Github il csv che si trova all'url indicato nel file html ed elabora il grafico. In questo modo, ogni volta che i csv vengono aggiornati tramite il chron-job, in automatico si aggiornano anche i grafici.


## Hardware e software necessari

    

