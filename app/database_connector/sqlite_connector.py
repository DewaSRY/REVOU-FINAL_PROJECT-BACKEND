

from os import  getcwd,path


def get_sqlite_connector():
    """alternative db for db in locale"""
    basedir = path.join(getcwd(), "app", "database_connector")
    dbPhat='sqlite:///' + path.join(basedir, 'data.db')
    return dbPhat