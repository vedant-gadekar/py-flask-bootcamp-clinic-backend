import datetime
from flask_jwt_extended import create_access_token, create_refresh_token

def generate_token(identity, role):
    access_token = create_access_token(
        identity=str(identity), additional_claims={"role": role}, expires_delta=datetime.timedelta(hours=1)
    )

    refresh_token = create_refresh_token(
        identity=str(identity), additional_claims={"role": role}, expires_delta=datetime.timedelta(days=30)
    )

    return access_token, refresh_token
