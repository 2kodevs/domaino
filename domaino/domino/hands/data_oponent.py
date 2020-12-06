from ..player_view import PlayerView
from random import sample, randint, shuffle

def data_opponent(max_number, pieces_per_player, high=True):
    """
    Share a high data or a low data with a oponent
    Randomly distribute pieces among other player.
    Valid pieces are all integer tuples of the form:
        (i, j) 0 <= i <= j <= max_number
    Each player will have `pieces_per_player`.
    """
    if high:
        data_num = randint(max_number // 2 + 1, max_number)
    else:
        data_num = randint(0, max_number // 2)
    data = [(min(data_num, i), max(data_num, i)) for i in sample(list(range(max_number + 1)), min(randint(max_number - 1, max_number + 1), pieces_per_player)]
    shuffle(data)

    all_pieces = {(i, j) for i in range(max_number + 1) for j in range(max_number + 1) if i <= j}

    data0 = data[:randint(1, len(data))]
    pieces0 = all_pieces - set(data0)
    hand0 = sample(pieces0, pieces_per_player - len(data0))
    hand0 += data0

    dataO = set(data) - set(data0)
    piecesO = pieces0 - set(dataO)
    handO = sample(piecesO, pieces_per_player - len(dataO))
    handO += dataO

    assert 4 * pieces_per_player <= len(piecesO) + len(handO) + len(hand0)
    hand = sample(piecesO, 2 * pieces_per_player)
    temp_hands = [hand[i:i+pieces_per_player] for i in range(0, 2 * pieces_per_player, pieces_per_player)]
    oponent_hands = [handO, temp_hands[0]]
    shuffle(oponent_hands)

    hands = [hand0, oponent_hands[0], temp_hands[1], oponent_hands[1]]

    for h in hands:
        print(h)
    return [PlayerView(h) for h in hands]

def data_opponent_low(max_number, pieces_per_player):
    return data_opponent(max_number, pieces_per_player, high=False)
    
