from datasource.database import db
from datasource.models.game_orm import GameORM
from datasource.mapper_db import DataMapper
from domain.game_domain import GameDomain, GameState
from sqlalchemy import or_


class GameRepository:
    @staticmethod
    def add_game(game: GameDomain):
        game_table = DataMapper.to_game_table(game)
        db.session.add(game_table)
        db.session.commit()

    @staticmethod
    def get_game(game_id) -> GameDomain:
        game_table = db.session.query(GameORM).filter_by(game_id=game_id).first()
        return DataMapper.to_game_domain(game_table) if game_table else None

    @staticmethod
    def update_game(game: GameDomain):
        game_table = db.session.query(GameORM).filter_by(game_id=game.game_id).first()

        if game_table:
            game_table.game_board = game.game_board
            game_table.active_turn = game.active_turn
            game_table.state = game.state
            game_table.player2_id = game.player2_id
            db.session.commit()
        else:
            raise ValueError(f"Game with ID {game.game_id} not found.")

    @staticmethod
    def get_available_games() -> list[GameDomain]:
        available_games = db.session.query(GameORM).filter_by(state=GameState.WAITING).limit(5).all()
        return [DataMapper.to_game_domain(game) for game in available_games]

    @staticmethod
    def get_completed_games_by_user(user_uuid: str):
        completed_games = db.session.query(GameORM).filter(
            or_(
                GameORM.player1_id == user_uuid,
                GameORM.player2_id == user_uuid
            ),
            GameORM.state.in_([GameState.WIN_PLAYER1, GameState.WIN_PLAYER2, GameState.DRAW])
        ).order_by(GameORM.created_at.desc()).limit(5).all()
        return [DataMapper.to_game_domain(game) for game in completed_games]

