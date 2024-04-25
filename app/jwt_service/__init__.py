
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)


def getCurrentAuthId():
    jwt=get_jwt()
    return jwt.get('current_id')