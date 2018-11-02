import random as rd
from .player import Player


class RandomPlayer(Player):

    def action(self, board):
        movable = board.get_movable(self.color)
        pos = rd.choice(tuple(filter(lambda x: x is not None, movable)))
        return pos
