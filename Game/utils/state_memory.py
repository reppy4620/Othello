from collections import deque
from config import CFG
from .helper import field_to_black, field_to_white
from ..data.color import Color
from ..rule import Rule

import numpy as np


class StateMemory:

    def __init__(self, clone=False, old=None):
        if clone:
            self._black_memory = deque(old._black_memory, maxlen=CFG.MemoryLength*2)
            self._white_memory = deque(old._white_memory, maxlen=CFG.MemoryLength*2)
        else:
            self._black_memory = deque([np.zeros((Rule.BoardSize, Rule.BoardSize)) for _ in range(CFG.MemoryLength*2)],
                                       maxlen=CFG.MemoryLength*2)
            self._white_memory = deque([np.zeros((Rule.BoardSize, Rule.BoardSize)) for _ in range(CFG.MemoryLength*2)],
                                       maxlen=CFG.MemoryLength*2)

    def clone(self):
        return StateMemory(clone=True, old=self)

    def push(self, field):
        self._black_memory.appendleft(field_to_white(field))
        self._black_memory.appendleft(field_to_black(field))
        self._white_memory.appendleft(field_to_black(field))
        self._white_memory.appendleft(field_to_white(field))

    def _get_memory(self, color):
        memory = self._black_memory if color == Color.Black else self._white_memory
        return np.array(memory)

    @property
    def black_memory(self):
        return self._get_memory(Color.Black)

    @property
    def white_memory(self):
        return self._get_memory(Color.White)

    def get_state(self, field, color):
        now_black = field_to_black(field)
        now_white = field_to_white(field)
        if color == Color.Black:
            state = np.array([now_black, now_white,
                              *self._black_memory, np.ones((Rule.BoardSize, Rule.BoardSize))],
                             dtype=np.float32)
        else:
            assert color == Color.White
            state = np.array([now_white, now_black,
                              *self._white_memory, np.zeros((Rule.BoardSize, Rule.BoardSize))],
                             dtype=np.float32)
        self.push(field)
        return state

    def __iter__(self):
        return iter(self._black_memory)

    def __getitem__(self, item):
        return self._black_memory[item]

    def __len__(self):
        return len(self._black_memory)
