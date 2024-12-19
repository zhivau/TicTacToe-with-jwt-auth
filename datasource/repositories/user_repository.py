from datasource.models.game_orm import GameORM
from datasource.models.user_orm import UserORM
from datasource.database import db
from sqlalchemy import func, case


class UserRepository:
    @staticmethod
    def add_user(login: str, password: str):
        if db.session.query(UserORM).filter_by(login=login).first():
            raise ValueError("User with this login already exists")

        user = UserORM(login=login, password=password)
        db.session.add(user)
        db.session.commit()
        return {"success": True, "user_id": str(user.user_id)}

    @staticmethod
    def get_user_by_login(login):
        return db.session.query(UserORM).filter_by(login=login).first()

    @staticmethod
    def get_user_by_id(user_id):
        return db.session.query(UserORM).filter_by(user_id=user_id).first()

    @staticmethod
    def get_user_game_stats(number_users):
        win_case = case(
            ((GameORM.player1_id == UserORM.user_id) & (GameORM.state == 'WIN_PLAYER1'), 1),
            ((GameORM.player2_id == UserORM.user_id) & (GameORM.state == 'WIN_PLAYER2'), 1),
            else_=0
        )

        lose_draw_case = case(
            ((GameORM.player1_id == UserORM.user_id) & (GameORM.state.in_(['WIN_PLAYER2', 'DRAW'])), 1),
            ((GameORM.player2_id == UserORM.user_id) & (GameORM.state.in_(['WIN_PLAYER1', 'DRAW'])), 1),
            else_=0
        )

        query = (
            db.session.query(
                UserORM.login,
                UserORM.user_id,
                func.sum(win_case).label("win"),
                func.sum(lose_draw_case).label("lose_draw")
            )
            .outerjoin(
                GameORM,
                (GameORM.player1_id == UserORM.user_id) | (GameORM.player2_id == UserORM.user_id)
            )
            .group_by(UserORM.user_id, UserORM.login)
            .order_by(
                func.sum(win_case).desc(),
                func.sum(lose_draw_case).asc()
            )
        )

        return query.limit(number_users).all()
