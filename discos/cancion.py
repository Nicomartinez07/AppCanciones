from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db


bp = Blueprint('cancion', __name__, url_prefix='/cancion')

#Creo lista de cancniones
@bp.route('/')
def canciones():
    #genero disco artista duracion 
    base_de_datos = db.get_db()
    consulta = """
        SELECT t.name AS Nombre, 
            t.TrackId AS idC, 
	        ar.name AS Artista,
	        a.Title AS Album, 
	        g.name AS Genero,
            ar.ArtistId AS idA,
            g.GenreId AS idG,
            a.AlbumId AS idD
        FROM tracks t
        JOIN artists ar ON a.ArtistId = ar.ArtistId
        JOIN albums a ON t.AlbumId = a.AlbumId
        LEFT JOIN genres g ON t.GenreId = g.GenreId
        ORDER BY Nombre DESC;
    """

    resultado = base_de_datos.execute(consulta)
    lista_de_resultados = resultado.fetchall()
    return render_template("cancion/cancion.html", canciones=lista_de_resultados)


 
#Detalle cancion 
@bp.route('/detalle/<int:id>')
def detalle(id):
    base_de_datos = db.get_db()
    consulta1 = """
        SELECT t.name AS Nombre,
	        ar.name AS Artista,
	        a.Title AS Album, 
	        g.name AS Genero,
	        strftime('%M:%S', t.Milliseconds / 1000, 'unixepoch') AS duracion,
            t.Bytes AS byte,
            ar.ArtistId AS idA,
            g.GenreId AS idG,
            a.AlbumId AS idD
        FROM tracks t
        JOIN artists ar ON a.ArtistId = ar.ArtistId
        JOIN albums a ON t.AlbumId = a.AlbumId
        JOIN genres g ON t.GenreId = g.GenreId
        WHERE t.TrackId = ?;
    """

  
    resultado = base_de_datos.execute(consulta1, (id,))
    cancion = resultado.fetchone()
    
    
    pagina = render_template("/cancion/detalleCancion.html", 
                           track=cancion)
    return pagina


@bp.route('/<int:albumid>/nueva', methods=('GET', 'POST'))
def nueva(albumid):
    if request.method == 'POST':
        name = request.form['name']
        artist = request.form['artist']
        genre = request.form['genre']
        error = None

        if not name:
            error = 'Se requiere el nombre.'

        if error is not None:
            flash(error)
        else:
            base = db.get_db()
            base.execute(
                'INSERT INTO tracks (Name, Composer, albumid)'
                'VALUES (?, ?, ?)',
                (name, artist, albumid) # genre)
            )
            base.commit()
            return redirect(url_for('disco.detalle', id=albumid))
    #SELECT DE GENEROS ID Y NOMBRE Y PASAR EN EL RENDER TEMPLATE

    return render_template('cancion/nueva_cancion.html')