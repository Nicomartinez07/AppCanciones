from flask import Blueprint, render_template
from . import db

bp = Blueprint('disco', __name__, url_prefix='/disco')

#Creo lista de disocs
@bp.route('/')
def discos():
    #nombre artista y cant de canciones
    base_de_datos = db.get_db()
    consulta = """
        SELECT a.title AS Album,
            a.AlbumId AS Id,
            ar.name AS Artista,
            ar.ArtistId AS idA,
            COUNT(t.name) AS cantCanciones 
            FROM albums a
        JOIN artists ar ON a.ArtistId = ar.ArtistId
        JOIN tracks t ON a.AlbumId = t.AlbumId
        GROUP BY a.AlbumId
        ORDER BY Album;
    """

    resultado = base_de_datos.execute(consulta)
    lista_de_resultados = resultado.fetchall()
    return render_template("disco/disco.html", discos=lista_de_resultados)


@bp.route('/detalle/<int:id>')
def detalle(id):
    base_de_datos = db.get_db()
    consulta1 = """
        SELECT a.Title AS Titulo, 
                ar.name AS Artista,
                a.AlbumId,
                ar.ArtistId AS idA
        FROM albums a
        JOIN artists ar ON a.ArtistId = ar.ArtistId
        WHERE a.AlbumId = ?;
    """
    consulta2 = """
        SELECT t.name AS Cancion ,
                t.TrackId AS tId
        FROM tracks t
        JOIN albums a ON t.AlbumId = a.AlbumId
        WHERE a.AlbumId  = ?;
    """

  
    resultado = base_de_datos.execute(consulta1, (id,)).fetchone()
    artista = { "nombre" : resultado["Artista"], "id": resultado["idA"]}
    disco = { "titulo" :  resultado["Titulo"], "id": resultado["AlbumId"]}
    resultado = base_de_datos.execute(consulta2, (id,))
    lista_canciones = resultado.fetchall()
    
    
    pagina = render_template("/disco/detalleDisco.html", 
                           disco=disco,
                           artista=artista,
                           listaCanciones=lista_canciones)
    return pagina


