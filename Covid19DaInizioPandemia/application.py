#File che chiama le tre funzioni principali: mappa (in file mappaCovid.py), graficiGiornalieri (in file graficiCovid.py) e graficiSettimanali (in file graficiCovidSettimanali.py)
from libreria.graficiCovidSettimanali import *
from libreria.graficiCovid import *
from libreria.numeroDiAbitanti import *
from libreria.mappaCovid import *
from flask import Flask, jsonify, render_template

application = Flask(__name__)

#Per vedere se è tutto ok quando facciamo carica e distribuisci su AWS (sulla pagina html deve comparire la scritta "405 Method Not Allowed")
@application.route("/")
def index():
    return "405 Method Not Allowed"

#funzione chiamata dal cron-job (aggiungendo "/update" all'url dell'applicazione caricata su AWS) 
@application.route("/update")
def update():
    mappa()
    graficiGiornalieri()
    graficiSettimanali()
    return render_template("update.html")

mappa()
graficiGiornalieri()
graficiSettimanali()

if __name__ == '__main__':
    application.run(debug=True, port=80)
