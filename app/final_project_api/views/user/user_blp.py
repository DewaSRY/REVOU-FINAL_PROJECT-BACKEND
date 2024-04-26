from flask_smorest import Blueprint, abort

blp = Blueprint(
    "users",
    __name__,
    description="""
                user management end point
                """,
)
