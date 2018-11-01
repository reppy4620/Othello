from .player import Player
from NeuralNetwork import NNetWrapper
from Game.rule import Rule
from Game.data import Position


class NNetPlayer(Player):

    def __init__(self, color):
        super().__init__(color)
        self.net = NNetWrapper()

    def action(self, board):
        pi, v = self.net.predict(board)
        idx = pi.argmax()
        y = pi % Rule.BoardSize
        x = idx - y*Rule.BoardSize
        return Position(x, y)
