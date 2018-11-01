from Game.data.color import Color
from Game.data.result import Result


class DiskCounter:
    def __init__(self):
        self._black = 0
        self._white = 0

    def reset(self):
        self._black = 0
        self._white = 0

    def _count(self, color, sign):
        if color == Color.Black:
            self._black += sign
        elif color == Color.White:
            self._white += sign
        else:
            assert color != Color.Empty

    def count(self, color):
        self._count(color, 1)

    def discount(self, color):
        self._count(color, -1)

    def compare(self):
        if self.black > self.white:
            return Result.BlackWin
        elif self.black < self.white:
            return Result.WhiteWin
        else:
            return Result.Draw

    @property
    def black(self):
        return self._black

    @property
    def white(self):
        return self._white
