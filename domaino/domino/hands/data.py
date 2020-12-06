from ..player_view import PlayerView
from random import sample, choice

def data(max_number, pieces_per_player, high=True):
    """
    Force player 0 to have 5 or more pieces of the same number.
    Randomly distribute pieces among the other players.
    Valid pieces are all integer tuples of the form:
        (i, j) 0 <= i <= j <= max_number
    Each player will have `pieces_per_player`.
    """

    mid = (max_number + 1) // 2 + 1
    data_number = choice(list(range(0 + mid * high, mid + (max_number + 1 - mid) * high)))
    hand = [(min(data_number, i), max(data_number, i)) for i in sample(list(range(max_number + 1)), 5)]

    pieces = [(i, j) for i in range(max_number + 1) for j in range(max_number + 1) if i <= j and (i, j) not in hand]
    assert 4 * pieces_per_player <= len(pieces) + len(hand)
    
    hand.extend(sample(pieces, 4 * pieces_per_player - len(hand)))
    hands = [hand[i:i+pieces_per_player] for i in range(0, 4 * pieces_per_player, pieces_per_player)]
    print(hands)
    return [PlayerView(h) for h in hands]
