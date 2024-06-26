"""_summary_

Returns:
    _type_: _description_
"""

from http import HTTPStatus
from dotenv import load_dotenv

from flask import Flask, jsonify, redirect
from flask_smorest import Api, Blueprint
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin
from flask_marshmallow import Marshmallow

# from flask_caching import Cache

from .user_module.views import blp as UserBluePrint
from .product_module.views import blp as ProductBluePrint
from .business_module.views import blp as BusinessBluePrint

from .user_module.type_model import UserTypeModel
from .business_module.type_model import BusinessTypeModel

from app.model_base_service import db
from app.jwt_service import JWTData
from app.message_service import MessageService


def create_app():
    app = Flask(__name__, static_url_path="/", static_folder="../../templates")
    load_dotenv(".env")
    app.config.from_object("config_default")
    app.config.from_envvar("APPLICATION_SETTINGS", silent=True)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)
    api = Api(app)
    cors = CORS(app)
    ma = Marshmallow(app)
    db.init_app(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(jwt_data: JWTData):
        return jwt_data.to_json()

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(MessageService.get_message(key_name="expired_token_callback")),
            HTTPStatus.UNAUTHORIZED,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(MessageService.get_message(key_name="invalid_token_callback")),
            HTTPStatus.UNAUTHORIZED,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(MessageService.get_message(key_name="missing_token")),
            HTTPStatus.UNAUTHORIZED,
        )

    with app.app_context():
        db.create_all()
        if len((UserTypeModel.get_all_model())) == 0:
            UserTypeModel.add_model(name="user")
            UserTypeModel.add_model(name="admin")
        if len(BusinessTypeModel.get_all_model()) == 0:
            BusinessTypeModel.add_model(name="food_and_beverage")
            BusinessTypeModel.add_model(name="fashion")
            BusinessTypeModel.add_model(name="education")
            BusinessTypeModel.add_model(name="health_care")
            BusinessTypeModel.add_model(name="finance")
            BusinessTypeModel.add_model(name="entertainment")
            BusinessTypeModel.add_model(name="advertising_and_media")
            BusinessTypeModel.add_model(name="construction")
            BusinessTypeModel.add_model(name="manufacturing")
            BusinessTypeModel.add_model(name="hospitality_and_tourism")

    # api.register_blueprint(mainApp)
    api.register_blueprint(UserBluePrint)
    api.register_blueprint(BusinessBluePrint)
    api.register_blueprint(ProductBluePrint)

    @app.route("/")
    def index():
        # return app.send_static_file("index.html")
        return redirect("api/redoc")

    return app
