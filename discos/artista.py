from flask import Blueprint, render_template
from . import db

bp = Blueprint('artista', __name__, url_prefix='/artista')

#CORREGIR PORQ MUESTRA LOS 2 NUMEROS IGUALES

@bp.route('/')
def artistas():
    #genero disco artista duracion 
    base_de_datos = db.get_db()
    consulta = """
        SELECT a.Name AS Artista, 
               a.ArtistId AS aId, 
               COUNT(al.AlbumId) AS cantAlbums, 
               COUNT(t.TrackId) AS cantCanciones 
        FROM artists a
        JOIN albums al ON a.ArtistId = al.ArtistId
        JOIN tracks t ON al.AlbumId = t.AlbumId
        GROUP BY al.AlbumId
        ORDER BY Artista
    """

    resultado = base_de_datos.execute(consulta)
    lista_de_resultados = resultado.fetchall()
    return render_template("artista/artista.html", artistas=lista_de_resultados)


#Artista
@bp.route('/detalle/<int:id>')
def detalle(id):
    base_de_datos = db.get_db()
    consulta1 = """
        SELECT ar.name AS Artista,
        ar.ArtistId AS idA
        FROM artists ar
        WHERE ar.ArtistId = ?;
    """

    consulta2 = """
        SELECT ar.name AS Artista, a.Title AS "Disco", ar.ArtistId AS idA, a.AlbumId AS idAl
        FROM artists ar
        JOIN albums a ON ar.ArtistId = a.ArtistId
        WHERE ar.ArtistId = ?;
    """
  
    resultado = base_de_datos.execute(consulta1, (id,))
    artista = resultado.fetchone()
    resultado = base_de_datos.execute(consulta2, (id,))
    lista_discos = resultado.fetchall()
    

    pagina = render_template("/artista/detalleArtista.html", 
                           artist=artista,
                           listaDiscos=lista_discos)
    return pagina
