from .hand_out import hand_out
from .no_doubles import no_doubles
from .data_partner import data_partner, data_partner_low
from .data_opponent import data_opponent, data_opponent_low

HANDS = [
    hand_out,
    no_doubles,
    data_partner,
    data_partner_low,
    data_opponent,
    data_opponent_low,
]

def get_hand(value):
    value = value.lower()
    for obj in HANDS:
        if obj.__name__.lower() == value:
            return obj
    raise ValueError(f"{value} not found in {[r.__name__ for r in HANDS]}")
