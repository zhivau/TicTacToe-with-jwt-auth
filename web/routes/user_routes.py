from flask import Blueprint, request, jsonify, current_app, g
from pydantic import ValidationError
from web.models.signup_request import SignUpRequest
from web.models.jwt_models import JwtRequest, RefreshJwtRequest
from web.modules.auth_service import AuthService
from web.models.user_web import UserWeb
from web.mapper_web import WebMapper


user_blueprint = Blueprint("user_routes", __name__)


@user_blueprint.route("/signup", methods=["POST"])
def signup():
    try:
        signup_request = SignUpRequest(**request.json)
        response = AuthService.register_user(signup_request)
        return jsonify(response), 200
    except ValidationError as e:
        return jsonify(e.errors()), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@user_blueprint.route("/login", methods=["POST"])
def login():
    try:
        jwt_request = JwtRequest(**request.json)
        response = AuthService.authenticate(jwt_request)
        return jsonify(response.dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401


@user_blueprint.route("/refresh/access-token", methods=["POST"])
def refresh_access_token():
    try:
        refresh_request = RefreshJwtRequest(**request.json)
        response = AuthService.refresh_access_token(refresh_request)
        return jsonify(response.dict()), 200
    except ValidationError as e:
        return jsonify(e.errors()), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 401


@user_blueprint.route("/refresh/refresh-token", methods=["POST"])
def refresh_refresh_token():
    try:
        refresh_request = RefreshJwtRequest(**request.json)
        response = AuthService.refresh_refresh_token(refresh_request)
        return jsonify(response.dict()), 200
    except ValidationError as e:
        return jsonify(e.errors()), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 401


@user_blueprint.route("/user", methods=["GET"])
@AuthService.login_required
def get_user_info():
    user_repository = current_app.config["container"].user_repository
    user = user_repository.get_user_by_id(g.user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(UserWeb(user.login, user.user_id).to_dict()), 200


@user_blueprint.route("/leaderboard/<int:number_users>")
@AuthService.login_required
def get_leaderboard_users(number_users):
    user_repository = current_app.config["container"].user_repository
    try:
        users = user_repository.get_user_game_stats(number_users)
        result = {i: WebMapper.to_user_leaderboard(user).dict() for i, user in enumerate(users)}
    except Exception as e:
        result = {"error": str(e)}
    return jsonify(result)