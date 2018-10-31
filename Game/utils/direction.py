from itertools import product


class Direction:
    def __init__(self):
        self._direction = tuple(product((-1, 0, 1), repeat=2))

    def __iter__(self):
        return iter(self._direction)

    def __getitem__(self, item):
        return self._direction[item]

    def __len__(self):
        return len(self._direction)
