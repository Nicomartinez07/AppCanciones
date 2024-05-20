import os 
import sqlite3

import click
from flask import current_app, g

#Define constantes con nombres y locaciones de las constantes----------------------------------------
db_folder = current_app.instance_path
db_name = 'discos.sqlite'
db_file = os.path.join(db_folder,db_name)


def dict_factory(cursor, row):
    """Arma un diccionario con los valores de la fila."""
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

#Conecta-Cierra base de datos -----------------------------------------------------------------------
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            db_file,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = dict_factory

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
#--------------------------------------------------------------------------------------------

#Abre el archivo sql y le manda todo lo q tiene adentro
def init_db():
    
    try:
        os.makedirs(current_app.instance_path)
    except OSError:
        pass

    db = get_db()

    with current_app.open_resource('discos.sql') as f:
        db.executescript(f.read().decode('utf8'))

#Inicializa la base de datos 
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

#--------------------------------------------------------------------------------------------

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)