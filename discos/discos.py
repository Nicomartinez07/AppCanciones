from flask import Blueprint, render_template
from . import db

bp = Blueprint('discos', __name__, url_prefix='/discos')

#Creo lista de disocs
@bp.route('/')
def discos():
    #nombre artista y cant de canciones
    base_de_datos = db.get_db()
    consulta = """
        SELECT a.title AS Album, ar.name AS Artista, COUNT(t.name) AS cantCanciones FROM albums a
        JOIN artists ar ON a.ArtistId = ar.ArtistId
        JOIN tracks t ON a.AlbumId = t.AlbumId
        GROUP BY a.AlbumId
        ORDER BY Album;
    """

    resultado = base_de_datos.execute(consulta)
    lista_de_resultados = resultado.fetchall()
    return render_template("discos.html", discos=lista_de_resultados)
