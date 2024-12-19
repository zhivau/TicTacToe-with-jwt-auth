from domain.game_service import GameService
from datasource.repositories.game_repository import GameRepository
from datasource.repositories.user_repository import UserRepository


class Container:
    def __init__(self):
        self.game_service = GameService
        self.game_repository = GameRepository
        self.user_repository = UserRepository
