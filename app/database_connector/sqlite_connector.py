from os import getcwd, path


def getSqliteConnector():
    """alternative db for db in locale"""
    basedir = path.join(getcwd(), "app", "database_connector")
    dbPhat = "sqlite:///" + path.join(basedir, "data.db")
    return dbPhat
