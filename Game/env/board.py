from ..utils import Direction, CellState, Position, Color, Result
from ..rule import Rule


class Board:

    def __init__(self):
        self._field = [[0] * 8 for _ in range(8)]
        self._direction = Direction()
        self.disks = DiskMemory()
        self._initialize()

    def reset(self):
        self._field = [[0] * 8 for _ in range(8)]
        self.disks.reset()
        self._initialize()

    def _initialize(self):
        color = Color.White
        for x, y in Rule.StartPosition:
            self._field[y][x] = color
            color *= -1

    def put(self, pos, color):
        if self._field[pos.y][pos.x] != CellState.empty:
            return False
        flippable = self._get_flippable(pos.x, pos.y, color)
        if len(flippable) == 0:
            return False

        self._field[pos.y][pos.x] = color
        self.disks.count(color)
        for x, y in flippable:
            self._field[y][x] = color
            self.disks.discount(color*-1)

    def _get_flippable(self, x, y, color):
        flippable = list()
        for dx, dy in self._direction:
            if dx == dy == 0:
                continue
            tmp = list()
            depth = 0
            while True:
                depth += 1
                rx = x + (dx * depth)
                ry = y + (dy * depth)

                if 0 <= rx < Rule.BoardSize and 0 <= ry < Rule.BoardSize:
                    req = self._field[ry][rx]
                    if req == CellState.empty:
                        break
                    if req == color:
                        if len(tmp) != 0:
                            flippable.extend(tmp)
                    else:
                        tmp.append((rx, ry))
                else:
                    break
        return flippable

    def get_movable(self, color):
        possible = list()
        for x in range(Rule.BoardSize):
            for y in range(Rule.BoardSize):
                if self._field[y][x] != CellState.empty:
                    continue
                elif len(self._get_flippable(x, y, color)) == 0:
                    continue
                else:
                    possible.append(Position(x, y))
        return possible

    def check_game_state(self):
        is_over = self.is_game_over()
        if is_over:
            return is_over, self.disks.compare()
        return is_over, None

    def is_game_over(self):
        for row in self._field:
            for cell_state in row:
                if cell_state == CellState.empty:
                    return False
        return True

    def display(self):
        self._separate()
        for row in self._field:
            for cell_state in row:
                if cell_state == Color.Black:
                    print('| ● ', end='')
                elif cell_state == Color.White:
                    print('| ○ ', end='')
                else:
                    print('|   ', end='')
            print('|')
            self._separate()
        print()

    @staticmethod
    def _separate():
        print('-' * (Rule.BoardSize * 4 + 1))

    @property
    def size(self):
        return Rule.BoardSize, Rule.BoardSize

    @property
    def width(self):
        return Rule.BoardSize

    @property
    def height(self):
        return Rule.BoardSize


class DiskMemory:
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
