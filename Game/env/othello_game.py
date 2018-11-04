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
        return c

    def step(self, action):
        pos, flippable = self._board.put(action, self.current_player)
        self.current_player *= -1
        return pos, flippable

    def is_game_over(self):
        return self._board.check_game_state()

    def is_valid(self, action):
        flippable = self._board.get_movable(self.current_player)
        for act in flippable:
            if act is None:
                continue
            if (act.x, act.y) == (action.x, action.y):
                print('valid')
                return True
        print('invalid')
        return False

    def display(self):
        self._board.display()
