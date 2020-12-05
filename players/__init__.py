from .simple import BigDrop, Frequent, Random, Repeater, TableCounter, Passer
from .simpleh import SimpleHybrid
from .mc import MonteCarlo

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
]