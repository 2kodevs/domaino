from .hand_out import hand_out
from .data import data

HANDS = [
    hand_out,
    data,
]

def get_hand(value):
    value = value.lower()
    for obj in HANDS:
        if obj.__name__.lower() == value:
            return obj
    raise ValueError(f"{value} not found in {[r.__name__ for r in HANDS]}")
