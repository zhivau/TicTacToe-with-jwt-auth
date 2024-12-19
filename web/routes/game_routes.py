from flask import Blueprint, request, current_app, jsonify, send_from_directory, g
from domain.game_domain import GameDomain, GameState
from web.mapper_web import WebMapper
from web.modules.auth_service import AuthService


game_blueprint = Blueprint("game_routes", __name__)


@game_blueprint.route("/")
def index():
    return send_from_directory("static", "index.html")


@game_blueprint.route("/new_game/<int:type_game>")
@AuthService.login_required
def new_game(type_game):
    user_repository = current_app.config["container"].user_repository
    user = user_repository.get_user_by_id(g.user_id)

    game = GameDomain()
    if type_game == 1:
        computer = user_repository.get_user_by_login("admin")
        game.player2_id = computer.user_id
        game.state = GameState.PLAYER1_TURN

    game.player1_id = user.user_id

    game_repository = current_app.config["container"].game_repository
    game_repository.add_game(game)

    return jsonify(WebMapper.to_game_web(game).to_dict()), 200


@game_blueprint.route("/game/<uuid:game_id>", methods=["POST"])
@AuthService.login_required
def update_game(game_id):
    game_repository = current_app.config["container"].game_repository
    user_repository = current_app.config["container"].user_repository
    game_service = current_app.config["container"].game_service

    game_data = request.get_json()
    user = user_repository.get_user_by_id(g.user_id)

    if not game_data:
        return {"error": "Invalid JSON"}, 400

    try:
        new_game_domain = WebMapper.to_game_domain(game_data)

        current_game_domain = game_repository.get_game(game_id)
        if not game_service.validate_board(current_game_domain, new_game_domain):
            return {"error": "invalid game"}, 400

        player2 = user_repository.get_user_by_id(current_game_domain.player2_id)
        if player2 and player2.login == "admin":
            current_game_domain.game_board = new_game_domain.game_board
            current_game_domain.active_turn = 2
            current_game_domain.update_state()
            game_service.next_move_computer(current_game_domain)
        elif player2:
            if (
                user.user_id == current_game_domain.player1_id
                and current_game_domain.active_turn == 1
                and current_game_domain.state == GameState.PLAYER1_TURN
            ) or (
                user.user_id == current_game_domain.player2_id
                and current_game_domain.active_turn == 2
                and current_game_domain.state == GameState.PLAYER2_TURN
            ):
                current_game_domain.game_board = new_game_domain.game_board
                current_game_domain.active_turn = (
                    1 if current_game_domain.active_turn == 2 else 2
                )
                current_game_domain.update_state()

    except KeyError as e:
        return {"error": f"Missing key: {str(e)}"}, 400

    game_repository.update_game(current_game_domain)
    game_web = WebMapper.to_game_web(current_game_domain)

    return jsonify(game_web.to_dict()), 200


@game_blueprint.route("/game_state/<uuid:game_id>")
@AuthService.login_required
def get_game_state(game_id):
    game_repository = current_app.config["container"].game_repository
    game_domain = game_repository.get_game(game_id)
    game_web = WebMapper.to_game_web(game_domain)
    return jsonify(game_web.to_dict()), 200


@game_blueprint.route("/available_games")
@AuthService.login_required
def get_available_games():
    game_repository = current_app.config["container"].game_repository
    available_games = game_repository.get_available_games()
    return jsonify(
        {
            i: WebMapper.to_game_web(game).to_dict()
            for i, game in enumerate(available_games)
        }
    )


@game_blueprint.route("/join_game/<uuid:game_id>", methods=["POST"])
@AuthService.login_required
def join_game(game_id):
    game_repository = current_app.config["container"].game_repository
    current_game = game_repository.get_game(game_id)

    user_repository = current_app.config["container"].user_repository
    user = user_repository.get_user_by_id(g.user_id)

    if user.user_id != current_game.player1_id:
        current_game.player2_id = user.user_id
        current_game.state = GameState.PLAYER1_TURN

        game_web = WebMapper.to_game_web(current_game)
        game_web.player_sign = "O"

        game_repository.update_game(current_game)
    else:
        return {"error": "player1 and player2 must be different"}, 400
    return jsonify(game_web.to_dict()), 200


@game_blueprint.route("/completed_games")
@AuthService.login_required
def get_completed_games():
    game_repository = current_app.config["container"].game_repository
    try:
        completed_games = game_repository.get_completed_games_by_user(g.user_id)
    except Exception as e:
        return {"error": str(e)}, 400

    return jsonify(
        {
            i: WebMapper.to_game_web(game).to_dict()
            for i, game in enumerate(completed_games)
        }
    )

