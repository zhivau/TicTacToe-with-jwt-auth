from domain.game_domain import GameState
from abc import ABC, abstractmethod
from domain.game_domain import GameDomain


class ServiceInterface(ABC):
    @staticmethod
    @abstractmethod
    def next_move_computer(game: GameDomain):
        pass

    @staticmethod
    @abstractmethod
    def validate_board(game: GameDomain, new_game: GameDomain) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def is_game_over(game: GameDomain) -> bool:
        pass


class GameService(ServiceInterface):
    @staticmethod
    def next_move_computer(game: GameDomain):
        if not GameService.is_game_over(game):
            ceil, _ = GameService.minimax(game)
            game.game_board[ceil[0]][ceil[1]] = 2
            game.active_turn = 1
        game.update_state()

    @staticmethod
    def validate_board(game: GameDomain, new_game: GameDomain) -> bool:
        diff = 0
        board = game.game_board
        new_board = new_game.game_board

        for i in range(3):
            for j in range(3):
                if board[i][j] != new_board[i][j]:
                    if (
                        board[i][j] == 0
                        and new_board[i][j] == 1
                        or board[i][j] == 0
                        and new_board[i][j] == 2
                    ):
                        diff += 1
                    else:
                        return False
        return diff == 1

    @staticmethod
    def is_game_over(game: GameDomain) -> bool:
        if game.state not in [
            GameState.PLAYER1_TURN,
            GameState.PLAYER2_TURN,
            GameState.WAITING,
        ]:
            return True
        return False

    @staticmethod
    def get_new_state(game: GameDomain, move):
        new_game = GameDomain()

        current_board = game.game_board
        new_board = new_game.game_board
        for i in range(3):
            for j in range(3):
                if move == (i, j):
                    new_board[i][j] = game.active_turn
                else:
                    new_board[i][j] = current_board[i][j]

        new_game.active_turn = 1 if game.active_turn == 2 else 2
        new_game.update_state()

        return new_game

    @staticmethod
    def minimax(game: GameDomain):
        if GameService.is_game_over(game):
            return None, game.get_score()

        moves_scores = []

        for move in game.get_available_moves():
            possible_game = GameService.get_new_state(game, move)
            _, score = GameService.minimax(possible_game)
            moves_scores.append((move, score))

        if game.active_turn == 1:
            best_move_score = max(moves_scores, key=lambda ms: ms[1])
            return best_move_score
        else:
            best_move_score = min(moves_scores, key=lambda ms: ms[1])
            return best_move_score
