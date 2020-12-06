from .simple import BigDrop, Frequent, Random
from .repeater import Repeater
from .table_counter import TableCounter
from .passer import Passer
from .supportive import Supportive
from .player_merge import MergeFactory
from .simpleh import SimpleHybrid
from .mc import MonteCarlo
from .small_drop import SmallDrop
from .agachao import Agachao

# Add players to this list
PLAYERS = [
    BigDrop,
    Frequent,
    Random,
    SimpleHybrid,
    MonteCarlo,
    Repeater,
    TableCounter,
    Passer,
    Supportive,
    SmallDrop,
    Agachao,
]

def get_player(value, merge=True):
    value = value.lower()
    for obj in PLAYERS:
        if obj.__name__.lower() == value:
            return obj
    try:
        assert merge
        names = value.split('-')
        return MergeFactory([get_player(name, False) for name in names])
    except AssertionError: pass
    except ValueError: pass
        
    raise ValueError(f"{value} not found in {[p.__name__ for p in PLAYERS]}")
