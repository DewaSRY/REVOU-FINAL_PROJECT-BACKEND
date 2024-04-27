"""_summary_

Returns:
    _type_: _description_
"""

from flask import Flask, jsonify
from flask_smorest import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin
from http import HTTPStatus

from dotenv import load_dotenv

from .views import UserBluePrint, BusinessBluePrint, ProductBluePrint
from .model.user import UserTypeModel
from .model.business import BusinessTypeModel

from app.model_base_service import db
from app.jwt_service import JWTData
from app.message_service import MassageService


def create_app():
    app = Flask(__name__)
    load_dotenv(".env")
    app.config.from_object("config_default")
    app.config.from_envvar("APPLICATION_SETTINGS", silent=True)

    jwt = JWTManager(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)
    cors = CORS(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(jwt_data: JWTData):
        return jwt_data.to_json()

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(MassageService.get_message(key_name="expired_token_callback")),
            HTTPStatus.UNAUTHORIZED,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(MassageService.get_message(key_name="invalid_token_callback")),
            HTTPStatus.UNAUTHORIZED,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(MassageService.get_message(key_name="missing_token")),
            HTTPStatus.UNAUTHORIZED,
        )

    with app.app_context():
        db.create_all()
        if len((UserTypeModel.get_all_model())) == 0:
            UserTypeModel.add_model(name="user")
            UserTypeModel.add_model(name="admin")
        if len(BusinessTypeModel.get_all_model()) == 0:
            BusinessTypeModel.add_model(name="food")
            BusinessTypeModel.add_model(name="book")

    api.register_blueprint(UserBluePrint)
    api.register_blueprint(BusinessBluePrint)
    api.register_blueprint(ProductBluePrint)

    return app
