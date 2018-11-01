from .board import Board
from ..rule import Rule


class OthelloEnv:

    def __init__(self, clone=False, old=None):
        if clone:
            self._board = old._board.clone()
            self.current_player = old.current_player
        else:
            self._board = Board()
            self.current_player = Rule.StartPlayer

    @property
    def board(self):
        return self._board

    def reset(self):
        self._board.reset()
        self.current_player = Rule.StartPlayer

    def clone(self):
        c = OthelloEnv(clone=True, old=self)

    def step(self, action):
        self._board.put(action, self.current_player)
        game_over, value = self.is_game_over()
        self.current_player *= -1
        return self.board, None, game_over, value

    def is_game_over(self):
        return self._board.check_game_state()

    def display(self):
        self._board.display()
