from .data import Color


class Rule:
    BoardSize = 8
    StartPlayer = Color.Black
    StartPosition = ((3, 3), (3, 4), (4, 4), (4, 3))
    White = ((3, 3), (4, 4))
    Black = ((3, 4), (4, 3))
