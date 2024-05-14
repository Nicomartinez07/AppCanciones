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

from . import discos
app.register_blueprint(discos.bp)

from . import canciones
app.register_blueprint(canciones.bp)

app.add_url_rule('/', endpoint='canciones.canciones')