from .board import Board
from ..rule import Rule


class OthelloEnv:

    def __init__(self):
        self._board = Board()
        self.current_player = Rule.StartPlayer

    @property
    def state(self):
        return self._board

    def reset(self):
        self._board.reset()
        self.current_player = Rule.StartPlayer

    def step(self, action):
        self._board.put(action, self.current_player)
        game_over, value = self.is_game_over()
        self.current_player *= -1
        return self.state, None, game_over, value

    def is_game_over(self):
        return self._board.check_game_state()

    def display(self):
        self._board.display()
