from flask_smorest import Blueprint, abort

blp = Blueprint(
    "image",
    __name__,
    description="""
                user management end point
                """,
)
