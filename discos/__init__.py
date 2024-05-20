import os 
from flask import Flask, send_file, render_template

app = Flask(__name__)

#importa el db.py
with app.app_context():
    from . import db
    db.init_app(app)

#Icono de la pagina 
@app.route('/favicon.ico')
def favicon():
    return send_file('static/flavicon.ico')

from . import cancion, disco
app.register_blueprint(cancion.bp)
app.register_blueprint(disco.bp)

app.add_url_rule('/', endpoint='cancion.canciones')