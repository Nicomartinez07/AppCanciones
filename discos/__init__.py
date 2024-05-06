import os 
from flask import Flask, send_file, render_template

app = Flask(__name__)

#importa el db.py
with app.app_context():
    from . import db
    db.init_app(app)

@app.route('/')
def hello():
    return 'Que, tal!'

#Creo lista de disocs
@app.route('/discos')
def discos():
    base_de_datos = db.get_db()
    consulta = """
        SELECT title FROM albums
        ORDER BY title;
    """

    resultado = base_de_datos.execute(consulta)
    lista_de_resultados = resultado.fetchall()
    return render_template("discos.html", discos=lista_de_resultados)

#Creo lista de disocs
@app.route('/canciones')
def canciones():
    base_de_datos = db.get_db()
    consulta = """
        SELECT name FROM tracks
        ORDER BY name;
    """

    resultado = base_de_datos.execute(consulta)
    lista_de_resultados = resultado.fetchall()
    return render_template("canciones.html", canciones=lista_de_resultados)

#Creo lista de artistas
@app.route('/artistas')
def artistas():
    base_de_datos = db.get_db()
    consulta = """
        SELECT name FROM artists
        ORDER BY name;
    """

    resultado = base_de_datos.execute(consulta)
    lista_de_resultados = resultado.fetchall()
    return render_template("artistas.html", artistas=lista_de_resultados)

#Creo lista de generos
@app.route('/generos')
def generos():
    base_de_datos = db.get_db()
    consulta = """
        SELECT name FROM genres
        ORDER BY name;
    """

    resultado = base_de_datos.execute(consulta)
    lista_de_resultados = resultado.fetchall()
    return render_template("genero.html", generos=lista_de_resultados)


#Icono de la pagina 
@app.route('/favicon.ico')
def favicon():
    return send_file('static/flavicon.ico')

