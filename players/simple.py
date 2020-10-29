from player import BasePlayer
import random

class BigDrop(BasePlayer):
    """ Always drop piece with highest score
    """
    def __init__(self, name):
        super().__init__(f"BigDrop::{name}")

    def choice(self):
        heads = self.heads
        max_weight = 0
        fat = []

        for piece, head in self.valid_moves():
            weight = piece[0] + piece[1]

            if weight > max_weight:
                fat.clear()
                max_weight = weight

            if weight == max_weight:
                fat.append((piece, head))

        assert len(fat) > 0

        move = random.choice(fat)

        return move


class Random(BasePlayer):
    """ Make a random move at each step
    """
    def __init__(self, name):
        super().__init__(f"Random::{name}")

    def choice(self):
        heads = self.heads

        return random.choice(self.valid_moves())


class Frequent(BasePlayer):
    """ Find piece most frequent in its hand. It tries to avoid passing.
    """
    def __init__(self, name):
        super().__init__(f"Frequent::{name}")

    def choice(self):
        # One piece A is neighbor of B if have at least one common number
        # Find pieces with largest number of neighbors
        pieces = []
        best_freq = -1

        for (cur_piece, head) in self.valid_moves():
            freq = 0

            for piece in self.pieces:
                if piece[0] in cur_piece or piece[1] in cur_piece:
                    freq += 1

            if freq > best_freq:
                best_freq = freq
                pieces = []

            if freq == best_freq:
                pieces.append((cur_piece, head))

        # Return one piece with largest number of neighbors randomly
        return random.choice(pieces)


class Repeater(BasePlayer):
    """ Find the piece with the number more used by himself. It tries to avoid passing.
    """
    def __init__(self, name):
        super().__init__(f"Repeater::{name}")


    def times_played(self):
        ''' Given a list of numbers return the amount of repetions per each one
        '''

        def update(d, player, heads):
            if player == self.position:
                for num in heads:
                    d[num] = d.get(num, 0) + 1
        
        times = {}
        all_moves = [d for e, *d in self.history if e.name == 'MOVE']
        if all_moves:
            first, *moves = all_moves
            heads = list(first[1])
            update(times, first[0], heads)
            for data in moves:
                player, piece, head = data
                heads[head] = piece[piece[0] == heads[head]]
                update(times, player, heads)    
        return times


    def choice(self):
        # Select the movement that generate the maximun repetion
        best, selected = [-1, -1], None
        times = self.times_played()
        for piece, head in self.valid_moves():
            heads = self.heads[:]
            heads[head] = piece[piece[0] == heads[head]]
            heads_value = [times.get(num, 0) for num in heads]
            heads_value.sort(reverse=True)
            if heads_value > best:
                best, selected = heads_value, (piece, head)

        return selected



        
