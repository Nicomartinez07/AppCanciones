from flask import Blueprint, render_template
from . import db

bp = Blueprint('genero', __name__, url_prefix='/genero')


#Genero
@bp.route('/detalleGenero/<int:id>')
def detalleGenero(id):
    base_de_datos = db.get_db()
    consulta3 = """
        SELECT Name AS Nombre, 
        GenreId AS idG 
        FROM genres
        WHERE GenreId = ?;
    """

  
    resultado = base_de_datos.execute(consulta3, (id,))
    genero = resultado.fetchone()
    
    
    pagina = render_template("/genero/detalleGenero.html", 
                           genre=genero)
    return pagina