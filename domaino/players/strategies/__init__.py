from .simple import BigDrop, Frequent, Random
from .repeater import Repeater
from .table_counter import TableCounter
from .passer import Passer
from .supportive import Supportive
from .player_merge import MergeFactory
from .simpleh import SimpleHybrid
from .mc import MonteCarlo
from .less_played import LessPlayed
from .data_keeper import DataKeeper
from .small_drop import SmallDrop
from .agachao import Agachao
from .always_double import AlwaysDouble

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
    LessPlayed,
    DataKeeper,
    SmallDrop,
    Agachao,
    AlwaysDouble
]
