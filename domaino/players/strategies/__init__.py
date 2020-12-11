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
from .data_dropper import DataDropper
from .always_double import AlwaysDouble
from .double_end import DoubleEnd
from .non_double import NonDouble

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
    DataDropper,
    AlwaysDouble,
    DoubleEnd,
    NonDouble,
]
