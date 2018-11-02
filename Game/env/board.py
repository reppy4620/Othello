from ..data import Direction, CellState, Position, Color
from ..utils import DiskCounter, StateMemory
from ..rule import Rule

import numpy as np


class Board:

    def __init__(self, clone=False, old=None):
        if clone:
            self._field = np.array(old._field)
            self._direction = old._direction
            self._disk_counter = old._disk_counter.clone()
            self._state_memory = old._state_memory.clone()
        else:
            self._field = np.array([[0] * 8 for _ in range(8)])
            self._direction = Direction()
            self._disk_counter = DiskCounter()
            self._state_memory = StateMemory()
            self._initialize()

    @property
    def state(self):
        return self._state_memory.get_state(self._field)

    def clone(self):
        return Board(clone=True, old=self)

    def reset(self):
        self._field = np.array([[0] * 8 for _ in range(8)])
        self._disk_counter.reset()
        self._initialize()

    def _initialize(self):
        color = Color.White
        for x, y in Rule.StartPosition:
            self._field[y][x] = color
            color *= -1

    def put(self, pos, color):
        if self._field[pos.y, pos.x] != CellState.empty or pos is None:
            return
        flippable = self._get_flippable(pos.x, pos.y, color)
        if len(flippable) == 0:
            return

        self._field[pos.y, pos.x] = color
        self._disk_counter.count(color)
        for x, y in flippable:
            self._field[y, x] = color
            self._disk_counter.count(color)
            self._disk_counter.discount(color * -1)

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
                    req = self._field[ry, rx]
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
                if self._field[y, x] != CellState.empty:
                    possible.append(None)
                    continue
                elif len(self._get_flippable(x, y, color)) == 0:
                    possible.append(None)
                    continue
                else:
                    possible.append(Position(x, y))
        return possible

    def check_game_state(self):
        is_over = self.is_game_over()
        if is_over:
            return is_over, self._disk_counter.compare()
        return is_over, 0

    def is_game_over(self):
        for row in self._field:
            for cell_state in row:
                if cell_state == CellState.empty:
                    return False
        return True

    def display(self):
        def separate():
            print('-' * (Rule.BoardSize * 4 + 1))
        separate()
        for row in self._field:
            for cell_state in row:
                if cell_state == Color.Black:
                    print('| ● ', end='')
                elif cell_state == Color.White:
                    print('| ○ ', end='')
                else:
                    print('|   ', end='')
            print('|')
            separate()
        print()

    @property
    def field(self):
        return self._field

    @property
    def size(self):
        return Rule.BoardSize, Rule.BoardSize

    @property
    def width(self):
        return Rule.BoardSize

    @property
    def height(self):
        return Rule.BoardSize
