from sqlalchemy import UUID, DateTime
from sqlalchemy.sql import func
from uuid import uuid4
from datasource.database import db
from domain.game_domain import GameState


class GameORM(db.Model):
    __tablename__ = "games"

    game_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    game_board = db.Column(db.PickleType, nullable=False)
    active_turn = db.Column(db.Integer, nullable=False, default=1)

    player1_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.user_id"), nullable=True
    )
    player2_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.user_id"), nullable=True
    )
    state = db.Column(db.Enum(GameState), nullable=False, default=GameState.WAITING)

    player1_sign = db.Column(db.String(1), nullable=False)
    player2_sign = db.Column(db.String(1), nullable=False)

    player1 = db.relationship("UserORM", foreign_keys=[player1_id])
    player2 = db.relationship("UserORM", foreign_keys=[player2_id])

    created_at = db.Column(DateTime, server_default=func.now())

    def __init__(
        self,
        game_board,
        game_id,
        active_turn,
        player1_id,
        player2_id,
        player1_sign,
        player2_sign,
        state,
        created_at
    ):
        self.game_board = game_board
        self.game_id = game_id
        self.active_turn = active_turn
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.player1_sign = player1_sign
        self.player2_sign = player2_sign
        self.state = state
        self.created_at = created_at
