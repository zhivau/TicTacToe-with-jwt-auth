from datasource.models.game_orm import GameORM
from domain.game_domain import GameDomain


class DataMapper:
    @staticmethod
    def to_game_table(game: GameDomain) -> GameORM:
        return GameORM(
            game_board=game.game_board,
            game_id=game.game_id,
            active_turn=game.active_turn,
            player1_id=game.player1_id,
            player2_id=game.player2_id,
            player1_sign=game.player1_sign,
            player2_sign=game.player2_sign,
            state=game.state,
            created_at=game.created_at
        )

    @staticmethod
    def to_game_domain(game_table: GameORM) -> GameDomain:
        return GameDomain(
            game_board=game_table.game_board,
            game_id=game_table.game_id,
            active_turn=game_table.active_turn,
            player1_id=game_table.player1_id,
            player2_id=game_table.player2_id,
            player1_sign=game_table.player1_sign,
            player2_sign=game_table.player2_sign,
            state=game_table.state,
            created_at=game_table.created_at
        )
