from libreria.graficiCovidSettimanali import *
from libreria.graficiCovid import *
from libreria.numeroDiAbitanti import *

from libreria.mappaCovid import *
from flask import Flask, jsonify, render_template


application = Flask(__name__)

@application.route("/")
def index():
    return "405 Method Not Allowed"

@application.route("/update")
def update():
    mappa()
    graficiGiornalieri()
    graficiSettimanali()
    return render_template("updateFlourish.html")

mappa()
graficiGiornalieri()
graficiSettimanali()

if __name__ == '__main__':
    application.run(debug=True, port=80)