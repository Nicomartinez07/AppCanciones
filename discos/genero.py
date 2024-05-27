from flask import Blueprint, render_template
from . import db

bp = Blueprint('genero', __name__, url_prefix='/genero')


@bp.route('/')
def generos():
    #genero disco artista duracion 
    base_de_datos = db.get_db()
    consulta = """
        SELECT g.Name AS Genero,
		        count(t.TrackId) AS cantCanciones,
                g.GenreId AS idG
        FROM genres g
        JOIN tracks t ON g.GenreId = t.GenreId
        GROUP BY g.GenreId
    """

    resultado = base_de_datos.execute(consulta)
    lista_de_resultados = resultado.fetchall()
    return render_template("genero/genero.html", generos=lista_de_resultados)



#Genero
@bp.route('/detalle/<int:id>')
def detalle(id):
    base_de_datos = db.get_db()
    consulta1 = """
        SELECT Name AS Nombre, 
        GenreId AS idG 
        FROM genres
        WHERE GenreId = ?;
    """

    consulta2 = """
        SELECT t.name AS Cancion , t.TrackId AS tId FROM tracks t
        JOIN genres g ON t.GenreId = g.GenreId
        WHERE g.GenreId = ?;
    """
  
    resultado = base_de_datos.execute(consulta1, (id,))
    genero = resultado.fetchone()
    resultado = base_de_datos.execute(consulta2, (id,))
    lista_Canciones = resultado.fetchall()
    
    
    pagina = render_template("/genero/detalleGenero.html", 
                           genero=genero,
                           listaCanciones=lista_Canciones)
    return pagina
