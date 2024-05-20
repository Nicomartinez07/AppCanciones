from flask import Blueprint, render_template
from . import db

bp = Blueprint('artista', __name__, url_prefix='/artista')



#Artista
@bp.route('/detalleArtista/<int:id>')
def detalleArtista(id):
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
