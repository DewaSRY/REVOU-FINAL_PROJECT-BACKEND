"""Default application settings"""

from app.database_connector import getSqliteConnector


API_TITLE = "Final Project Api"
API_VERSION = "v0"
OPENAPI_VERSION = "3.0.3"
OPENAPI_URL_PREFIX = "/"

API_DOC_HTML = "custom_swagger_ui.html"
OPENAPI_REDOC_PATH = "api/redoc"
OPENAPI_REDOC_URL = (
    "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
)


OPENAPI_SWAGGER_UI_PATH = "api/swagger-ui"
OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

OPENAPI_RAPIDOC_PATH = "api/rapidoc"
OPENAPI_RAPIDOC_URL = "https://unpkg.com/rapidoc/dist/rapidoc-min.js"
OPENAPI_RAPIDOC_CONFIG = {"theme": "dark"}


SQLALCHEMY_DATABASE_URI = getSqliteConnector()
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
JWT_SECRET_KEY = "WkmpquACbmiuS7gd"
CORS_HEADERS = "Content-Type"
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 mb
ALLOWED_EXTENSIONS = [".jpeg", ".png", ".gif", ".jpg"]
UPLOAD_FOLDER = "upload"
