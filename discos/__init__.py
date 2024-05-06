import os 
from flask import Flask, send_file

app = Flask(__name__)

#importa el db.py
with app.app_context():
    from . import db
    db.init_app(app)

@app.route('/')
def hello():
    return 'Que, tal!'

#Icono de la pagina 
@app.route('/favicon.ico')
def favicon():
    return send_file('static/flavicon.ico')

