from web.models.game_web import GameWeb
from domain.game_domain import GameDomain
from web.models.user_web import UserWeb
from datasource.models.user_orm import UserORM
from web.models.user_leaderboard import UserLeaderboard


class WebMapper:
    @staticmethod
    def to_game_web(game: GameDomain):
        return GameWeb(
            game_board=game.game_board,
            game_id=game.game_id,
            active_turn=game.active_turn,
            player2_id=game.player2_id,
            player1_id=game.player1_id,
            state=game.state,
            created_at=game.created_at
        )

    @staticmethod
    def to_game_domain(game_json):
        game_board_web = game_json["game_board"]
        game_board_domain = [[0 for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                if game_board_web[i][j] == "X":
                    game_board_domain[i][j] = 1
                elif game_board_web[i][j] == "O":
                    game_board_domain[i][j] = 2

        return GameDomain(
            game_board=game_board_domain, game_id=game_json.get("game_id")
        )

    @staticmethod
    def to_user_web(user: UserORM):
        return UserWeb(login=user.login, user_id=user.user_id)

    @staticmethod
    def to_user_leaderboard(user_row):
        return UserLeaderboard(uuid=str(user_row.user_id), win=user_row.win, lose_draw=user_row.lose_draw)

