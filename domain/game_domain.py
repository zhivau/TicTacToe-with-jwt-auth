from uuid import uuid4
from enum import Enum
from datetime import datetime


class GameState(Enum):
    WAITING = "waiting"
    DRAW = "draw"
    WIN_PLAYER1 = "win_player1"
    WIN_PLAYER2 = "win_player2"
    PLAYER1_TURN = "player1_turn"
    PLAYER2_TURN = "player2_turn"


class GameDomain:
    def __init__(
        self,
        game_board=None,
        game_id=None,
        active_turn=None,
        player1_id=None,
        player2_id=None,
        player1_sign=None,
        player2_sign=None,
        state=None,
        created_at=None
    ):
        self.game_board = game_board or [[0 for _ in range(3)] for _ in range(3)]

        self.game_id = game_id or uuid4()

        self.player1_id = player1_id
        self.player2_id = player2_id

        self.state = state or GameState.WAITING

        self.player1_sign = player1_sign or "X"
        self.player2_sign = player2_sign or "O"

        self.active_turn = active_turn or 1
        self.created_at = created_at or datetime.utcnow()

    def __str__(self):
        return f"game_domain: {self.game_board} | {self.game_id} | {self.active_turn}"

    def is_win(self, value):
        board = self.game_board
        for i in range(3):
            if (
                board[i][0] == board[i][1] == board[i][2] == value
                or board[0][i] == board[1][i] == board[2][i] == value
            ):
                return True
        if (
            board[0][0] == board[1][1] == board[2][2] == value
            or board[0][2] == board[1][1] == board[2][0] == value
        ):
            return True
        return False

    def is_draw(self):
        for line in self.game_board:
            if 0 in line:
                return False
        return True

    def update_state(self):
        if self.is_win(1):
            self.state = GameState.WIN_PLAYER1
        elif self.is_win(2):
            self.state = GameState.WIN_PLAYER2
        elif self.is_draw():
            self.state = GameState.DRAW
        else:
            if self.active_turn == 1:
                self.state = GameState.PLAYER1_TURN
            elif self.active_turn == 2:
                self.state = GameState.PLAYER2_TURN

    def get_score(self):
        if self.is_win(1):
            return 10
        elif self.is_win(2):
            return -10
        else:
            return 0

    def get_available_moves(self):
        moves = []
        for i in range(3):
            for j in range(3):
                if self.game_board[i][j] == 0:
                    moves.append((i, j))
        return moves

    def print_board(self):
        num_ceil = []

        for i in range(3):
            num_ceil.append([])
            for j in range(3):
                num_ceil[i].append((i, j))

        for line, line_num in zip(self.game_board, num_ceil):
            print(*line, " ", *line_num)
        print()
