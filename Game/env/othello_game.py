from .board import Board
from ..rule import Rule
from ..utils import StateMemory


class OthelloEnv:

    def __init__(self):
        self._board = Board()
        self.current_player = Rule.StartPlayer
        self.memory = StateMemory()

    @property
    def board(self):
        return self._board

    def reset(self):
        self._board.reset()
        self.current_player = Rule.StartPlayer

    def step(self, action):
        self._board.put(action, self.current_player)
        game_over, value = self.is_game_over()
        self.current_player *= -1
        self.memory.push(self._board.field)
        return self.board, None, game_over, value

    def is_game_over(self):
        return self._board.check_game_state()

    def display(self):
        self._board.display()
