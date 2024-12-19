from flask import current_app, request, jsonify, g
from web.models.signup_request import SignUpRequest
from web.models.jwt_models import JwtRequest, JwtResponse, RefreshJwtRequest
from web.modules.jwt_provider import JwtProvider
from functools import wraps


class AuthService:
    @staticmethod
    def register_user(signup_request: SignUpRequest):
        user_repository = current_app.config["container"].user_repository
        response = user_repository.add_user(signup_request.login, signup_request.password)
        return response

    @staticmethod
    def authenticate(jwt_request: JwtRequest):
        try:
            user_repository = current_app.config["container"].user_repository
            user = user_repository.get_user_by_login(jwt_request.login)

            if user and user.check_password(jwt_request.password):
                access_token = JwtProvider.generate_access_token(user)
                refresh_token = JwtProvider.generate_refresh_token(user)
                return JwtResponse(accessToken=access_token, refreshToken=refresh_token)
            else:
                raise ValueError("Invalid login or password")

        except (ValueError, TypeError, UnicodeDecodeError):
            raise ValueError("Invalid authorization header")

    @staticmethod
    def refresh_access_token(refresh_request: RefreshJwtRequest):
        if not JwtProvider.validate_refresh_token(refresh_request.refreshToken):
            raise ValueError("Invalid refresh token")
        user_uuid = JwtProvider.get_uuid_from_token(refresh_request.refreshToken)
        user_repository = current_app.config["container"].user_repository
        user = user_repository.get_user_by_id(user_uuid)
        if not user:
            raise ValueError("User not found")
        access_token = JwtProvider.generate_access_token(user)
        return JwtResponse(accessToken=access_token, refreshToken=refresh_request.refreshToken)

    @staticmethod
    def refresh_refresh_token(refresh_request: RefreshJwtRequest):
        if not JwtProvider.validate_refresh_token(refresh_request.refreshToken):
            raise ValueError("Invalid refresh token")
        user_uuid = JwtProvider.get_uuid_from_token(refresh_request.refreshToken)
        user_repository = current_app.config["container"].user_repository
        user = user_repository.get_user_by_id(user_uuid)
        if not user:
            raise ValueError("User not found")
        refresh_token = JwtProvider.generate_refresh_token(user)
        access_token = JwtProvider.generate_access_token(user)
        return JwtResponse(accessToken=access_token, refreshToken=refresh_token)

    @staticmethod
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": f"Missing or invalid Authorization header"}), 401

            token = auth_header.split(" ")[1]

            if not JwtProvider.validate_access_token(token):
                return jsonify({"error": "Invalid or expired access token, validate"}), 401

            try:
                g.user_id = JwtProvider.get_uuid_from_token(token)
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({"error": str(e)}), 401

        return decorated_function
