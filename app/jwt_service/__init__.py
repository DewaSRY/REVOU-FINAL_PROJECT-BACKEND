from datetime import timedelta
from .jwt_data import JWTData

# from .jwt_service import JWSService
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)


def getCurrentAuthId():
    jwt = get_jwt()
    return jwt.get("current_id")


def getIsUserAdmin():
    jwt = get_jwt()
    return jwt.get("is_admin")


def createAccessToken(user_id: str, user_type: str):
    return create_access_token(
        identity=JWTData(user_id=user_id, user_type=user_type),
        expires_delta=timedelta(days=7),
    )
