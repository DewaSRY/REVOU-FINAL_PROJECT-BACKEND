"""_summary_
"""

from flask_smorest import Blueprint, abort

blp = Blueprint(
    "business",
    __name__,
    description="""
                user management end point
                """,
)
