from flask import Blueprint, render_template
from . import db

bp = Blueprint('discos', __name__, url_prefix='/discos')

#Creo lista de disocs
@bp.route('/')
def discos():
    #nombre artista y cant de canciones
    base_de_datos = db.get_db()
    consulta = """
        SELECT a.title AS Album,
            a.AlbumId AS Id,
            ar.name AS Artista,
            COUNT(t.name) AS cantCanciones 
            FROM albums a
        JOIN artists ar ON a.ArtistId = ar.ArtistId
        JOIN tracks t ON a.AlbumId = t.AlbumId
        GROUP BY a.AlbumId
        ORDER BY Album;
    """

    resultado = base_de_datos.execute(consulta)
    lista_de_resultados = resultado.fetchall()
    return render_template("disco/discos.html", discos=lista_de_resultados)


@bp.route('/detalle/<int:id>')
def detalle(id):
    base_de_datos = db.get_db()
    consulta = """
        SELECT a.Title AS Titulo, 
                ar.name AS Nombre
        FROM albums a
        JOIN artists ar ON a.ArtistId = ar.ArtistId
        WHERE a.AlbumId = ?;
    """

  
    resultado = base_de_datos.execute(consulta, (id,))
    discos = resultado.fetchone()
    
    
    pagina = render_template("/discos/detalleDisco.html", 
                           track=discos)
    return pagina