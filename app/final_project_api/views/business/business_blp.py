"""_summary_
"""

from flask_smorest import Blueprint, abort

blp = Blueprint(
    "business",
    __name__,
    url_prefix="/business",
    description="""
                business management end point
                """,
)
