from os import environ


def getMysqlConnector():
    """my sql connector"""
    USER_NAME = environ.get("USER_NAME")
    PASSWORD = environ.get("PASSWORD")
    DB_NAME = environ.get("DB_NAME")
    SERVER = environ.get("SERVER")
    if USER_NAME == None or PASSWORD == None or DB_NAME == None or SERVER == None:
        raise Exception(
            "mysql environment not found,  please make sure the environment is define"
        )

    return f"mysql+mysqlconnector://{USER_NAME}:{PASSWORD}@{SERVER}/{DB_NAME}"
