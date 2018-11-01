from ..data import Color

import numpy as np


def _field_to_color(field, color):
    field = np.array(field)
    return np.where(field == color, 1, 0)


def field_to_black(field):
    return _field_to_color(field, Color.Black)


def field_to_white(field):
    return _field_to_color(field, Color.White)


def field_to_black_and_white(field):
    return _field_to_color(field, Color.Black), _field_to_color(field, Color.White)
