from collections import deque
from config import CFG
from .helper import field_to_black, field_to_white
from ..data.color import Color
from ..rule import Rule

import numpy as np


class StateMemory:

    def __init__(self):
        self._black_memory = deque([np.zeros((Rule.BoardSize, Rule.BoardSize)) for _ in range(CFG.MemoryLength)],
                                   maxlen=CFG.MemoryLength)
        self._white_memory = deque([np.zeros((Rule.BoardSize, Rule.BoardSize)) for _ in range(CFG.MemoryLength)],
                                   maxlen=CFG.MemoryLength)
        self._idx = 0
        self._current_player = Rule.StartPlayer

    def push(self, field):
        self._black_memory.append(field_to_black(field))
        self._white_memory.append(field_to_white(field))
        self._idx += 1

    def _get_memory(self, color):
        memory = self._black_memory if color == Color.Black else self._white_memory
        return np.array(list(reversed(memory)))

    @property
    def black_memory(self):
        return self._get_memory(Color.Black)

    @property
    def white_memory(self):
        return self._get_memory(Color.White)

    def get_state(self, field):
        now_black = field_to_black(field)
        now_white = field_to_white(field)
        color_state = np.ones((Rule.BoardSize, Rule.BoardSize)) if self._current_player == Color.Black else\
            np.zeros((Rule.BoardSize, Rule.BoardSize))
        self._current_player *= -1
        return np.array([now_black, now_white,
                         *self.black_memory, *self.white_memory,
                         color_state], dtype=np.float32)

    def __iter__(self):
        return iter(self._black_memory)

    def __getitem__(self, item):
        return self._black_memory[item]

    def __len__(self):
        return len(self._black_memory)
