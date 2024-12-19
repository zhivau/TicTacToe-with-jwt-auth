from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token
)
from datetime import timedelta
import json


class JwtProvider:
    @staticmethod
    def generate_access_token(user):
        res = create_access_token(identity=str({"uuid": str(user.user_id)}), expires_delta=timedelta(hours=1))
        return res

    @staticmethod
    def generate_refresh_token(user):
        return create_refresh_token(identity=str({"uuid": str(user.user_id)}), expires_delta=timedelta(days=30))

    @staticmethod
    def validate_access_token(token):
        try:
            decode_token(token, allow_expired=False)
            return True
        except Exception as e:
            return False

    @staticmethod
    def validate_refresh_token(token):
        try:
            decode_token(token, allow_expired=False)
            return True
        except Exception as e:
            return False

    @staticmethod
    def get_uuid_from_token(token):
        decoded = decode_token(token, allow_expired=False)
        uuid_dict = json.loads(decoded["sub"].replace("'", '"'))
        return uuid_dict["uuid"]
