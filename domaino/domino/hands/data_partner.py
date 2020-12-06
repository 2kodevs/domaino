from ..player_view import PlayerView
from random import sample, randint, shuffle

def data_partner(max_number, pieces_per_player, high=True):
    """
    Randomly distribute pieces among every player.
    Share a high data or a low data with partner
    Valid pieces are all integer tuples of the form:
        (i, j) 0 <= i <= j <= max_number
    Each player will have `pieces_per_player`.
    """
    if high:
        data_num = randint(max_number // 2 + 1, max_number)
    else:
        data_num = randint(0, max_number // 2)
    data = [(min(data_num, i), max(data_num, i)) for i in sample(list(range(pieces_per_player)), randint(max_number - 1, max_number + 1) )]
    shuffle(data)

    all_pieces = {(i, j) for i in range(max_number + 1) for j in range(max_number + 1) if i <= j}

    data0 = data[:randint(1, len(data))]
    pieces0 = all_pieces - set(data0)
    hand0 = sample(pieces0, pieces_per_player - len(data0))
    hand0 += data0

    data2 = set(data) - set(data0)
    pieces2 = pieces0 - set(data2)
    hand2 = sample(pieces2, pieces_per_player - len(data2))
    hand2 += data2

    assert 4 * pieces_per_player <= len(pieces2) + len(hand2) + len(hand0)
    hand = sample(pieces2, 2 * pieces_per_player)
    temp_hands = [hand[i:i+pieces_per_player] for i in range(0, 2 * pieces_per_player, pieces_per_player)]
    hands = [hand0]
    hands += [temp_hands[0]]
    hands += [hand2]
    hands += [temp_hands[1]]

    return [PlayerView(h) for h in hands]

def data_partner_low(max_number, pieces_per_player):
    return data_partner(max_number, pieces_per_player, high=False)
