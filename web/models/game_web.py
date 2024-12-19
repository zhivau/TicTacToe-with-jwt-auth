class GameWeb:
    def __init__(self, game_board, game_id, active_turn, player1_id, player2_id, state, created_at):
        self.game_board = [[" " for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                if game_board[i][j] == 1:
                    self.game_board[i][j] = "X"
                elif game_board[i][j] == 2:
                    self.game_board[i][j] = "O"

        self.game_id = game_id
        self.active_turn = active_turn

        self.player1_id = player1_id
        self.player2_id = player2_id

        self.state = state

        self.player1_sign = "X"
        self.player2_sign = "O"
        self.created_at = created_at

    def __str__(self):
        return f"game_web: {self.game_board} | {self.game_id} | {self.active_turn}"

    def to_dict(self):
        return {
            "game_board": self.game_board,
            "game_id": self.game_id,
            "player1_id": self.player2_id,
            "player2_id": self.player2_id,
            "state": self.state.value,
            "player1_sign": self.player1_sign,
            "player2_sign": self.player2_sign,
            "active_turn": self.active_turn,
            "created_at": self.created_at
        }
