from flask_smorest import Blueprint, abort

blp = Blueprint(
    "users",
    __name__,
    url_prefix="/user",
    description="""
                user management end point
                """,
)
