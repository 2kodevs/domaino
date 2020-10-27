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

        for piece in self.pieces:
            for head in range(2):
                if self.valid(piece, head):
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
        valids = []

        for piece in self.pieces:
            for head in range(2):
                if self.valid(piece, head):
                    valids.append((piece, head))

        return random.choice(valids)


class Frequent(BasePlayer):
    """ Find piece most frequent in its hand. It tries to avoid passing.
    """
    def __init__(self, name):
        super().__init__(f"Frequent::{name}")

    def choice(self):
        # List all valid moves in the form (piece, head).
        # This is put piece on head.
        valids = []

        for piece in self.pieces:
            for head in range(2):
                if self.valid(piece, head):
                    valids.append((piece, head))

        # One piece A is neighbor of B if have at least one common number
        # Find pieces with largest number of neighbors
        pieces = []
        best_freq = -1

        for (cur_piece, head) in valids:
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


    def times_played(self, numbers):
        ''' Given a list of numbers return the amount of repetions per each one
        '''
        times = []
        all_moves = [d for e, *d in self.history if e.name == 'MOVE']
        if not all_moves:
            return [0] * len(numbers)
        first, *moves = all_moves
        for num in numbers:
            times.append(0)
            heads = list(first[1])
            for data in moves:
                player, piece, head = data
                heads[head] = piece[piece[0] == heads[head]]
                times[-1] += (num in heads) * (player == self.position)
            times[-1] += (num in first[1]) * (first[0] == self.position)
        return times


    def choice(self):
        # List all valid moves in the form (piece, head).
        # This is put piece on head.
        valids = []

        for piece in self.pieces:
            for head in range(2):
                if self.valid(piece, head):
                    valids.append((piece, head))

        # Select the movement that generate the maximun repetion
        best, selected = [-1, -1], None
        for piece, head in valids:
            heads = self.heads[:]
            heads[head] = piece[piece[0] == heads[head]]
            times = self.times_played(heads)
            times.sort(reverse=True)
            if times > best:
                best, selected = times, (piece, head)

        return selected



        
