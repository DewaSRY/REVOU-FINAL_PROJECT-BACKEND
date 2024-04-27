"""_summary_
"""

from flask_smorest import Blueprint, abort

blp = Blueprint(
    "product",
    __name__,
    description="""
                user management end point
                """,
)
