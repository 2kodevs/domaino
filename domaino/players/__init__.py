from .strategies import PLAYERS, MergeFactory
from .behaviors import BEHAVIORS
from .player import BasePlayer

ALL = [*PLAYERS, *BEHAVIORS]

def get_player(value, merge=True, elements=PLAYERS):
    value = value.lower()
    for obj in elements:
        if obj.__name__.lower() == value:
            return obj
    try:
        assert merge
        names = value.split('-')
        return MergeFactory([get_player(name, False, ALL) for name in names])
    except AssertionError: pass
    except ValueError: pass
        
    raise ValueError(f"{value} not found in {[e.__name__ for e in elements]}")
