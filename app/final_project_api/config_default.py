"""Default application settings"""

from app.database_connector import getSqliteConnector


class ConfigDefault:
    API_TITLE = "Final Project Api"
    API_VERSION = "v0"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    SQLALCHEMY_DATABASE_URI = getSqliteConnector()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    JWT_SECRET_KEY = "WkmpquACbmiuS7gd"
    CORS_HEADERS = "Content-Type"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 mb
    ALLOWED_EXTENSIONS = [".jpeg", ".png", ".gif", ".jpg"]
