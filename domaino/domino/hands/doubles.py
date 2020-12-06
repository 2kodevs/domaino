from ..player_view import PlayerView
from random import sample, randint

def doubles(max_number, pieces_per_player):
    """
    Randomly distribute pieces among every player.
    Valid pieces are all integer tuples of the form:
        (i, j) 0 <= i <= j <= max_number
    Each player will have `pieces_per_player`.

    Player0 always gets at least half of doubles.
    """
    pieces = [(i, j) for i in range(max_number + 1) for j in range(max_number + 1) if i <= j]
    assert 4 * pieces_per_player <= len(pieces)

    selected_doubles = sample(list(range(max_number + 1)), randint((max_number + 1) // 2, max_number - 1))
    selected_doubles = [(x, x) for x in selected_doubles]
    for x in selected_doubles:
        pieces.remove(x)
    hand = sample(pieces, 4 * pieces_per_player - len(selected_doubles))
    hand = [*selected_doubles, *hand]
    hands = [hand[i:i+pieces_per_player] for i in range(0, 4 * pieces_per_player, pieces_per_player)]
    return [PlayerView(h) for h in hands]
