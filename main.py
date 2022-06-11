from flask import Flask, render_template, request
import sys
import requests

sys.path.append('./Data/data_elecciones')
from read import Indice_invertido

app = Flask(__name__)
nuevo_indice=Indice_invertido()
nuevo_indice.construct_indice()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/indice")
def load_indice():
    nuevo_indice=Indice_invertido()
    nuevo_indice.construct_indice()
    return nuevo_indice.Indice

@app.route("/query", methods=['POST'])
def query():
    texto = request.form['texto_query']
    document_query=nuevo_indice.query(texto)
    return nuevo_indice.compare_total(document_query)






if __name__ == '__main__':
    app.run(debug=True)


