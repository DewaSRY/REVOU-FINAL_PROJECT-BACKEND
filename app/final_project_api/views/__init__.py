"""_summary_
"""

# from flask_smorest import Api, Blueprint
from .user.user_views import blp as UserBluePrint
from .business.business_views import blp as BusinessBluePrint
from .product.product_views import blp as ProductBluePrint

# mainApp = Blueprint(
#     "main_api_rout",
#     __name__,
#     url_prefix="/api",
#     description="user rout end point, most of it is user account setting from the personal data to the list of personal ownership",
# )
# mainApp.register_blueprint(UserBluePrint)
# mainApp.register_blueprint(BusinessBluePrint)
# mainApp.register_blueprint(ProductBluePrint)
