from flask import Blueprint, render_template
from . import db

bp = Blueprint('genero', __name__, url_prefix='/genero')


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