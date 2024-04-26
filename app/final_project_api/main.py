from flask import Flask, jsonify
from flask_smorest import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin
from app.database_connector import getSqliteConnector
from app.model_base_service import db

from .views import UserBluePrint
from .model.user import UserTypeModel


def create_app(db_url=None):
    app = Flask(__name__)
    # app = Flask(__name__,static_url_path="/",static_folder="../frontend/dist")
    app.config["API_TITLE"] = "Final Project Api"
    app.config["API_VERSION"] = "v0"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or getSqliteConnector()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["JWT_SECRET_KEY"] = "WkmpquACbmiuS7gd"
    app.config["CORS_HEADERS"] = "Content-Type"
    jwt = JWTManager(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)
    cors = CORS(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        # Look in the database and see whether the user is an admin
        return {"current_id": identity, "is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    with app.app_context():
        db.create_all()
        if len(UserTypeModel.query.all()) == 0:
            UserTypeModel.add_all_model(
                [
                    UserTypeModel("user"),
                    UserTypeModel("admin"),
                ]
            )
            # TransactionTypeModel.add_all_model(
            #     [
            #         TransactionTypeModel("groceries"),
            #         TransactionTypeModel("rent"),
            #         TransactionTypeModel("entertainment"),
            #         TransactionTypeModel("deposit"),
            #         TransactionTypeModel("withdrawal"),
            #         TransactionTypeModel("transfer"),
            #         TransactionTypeModel("receive"),
            #     ]
            # )
            # AccountTypeModel.add_all_model(
            #     [
            #         AccountTypeModel("checking"),
            #         AccountTypeModel("saving"),
            #     ]
            # )
        # DataStore.store_account_type(AccountTypeModel.query.all())
        # DataStore.store_transaction_type(TransactionTypeModel.query.all())
    api.register_blueprint(UserBluePrint)
    # api.register_blueprint(AccountBluePrint)
    # api.register_blueprint(BillsBluePrint)
    # api.register_blueprint(TransactionBluePrint)
    # api.register_blueprint(BudgetsBluePrint)
    return app
