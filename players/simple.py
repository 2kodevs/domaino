from player import BasePlayer
import random

class BigDrop(BasePlayer):
    """ Always drop piece with highest score
    """
    def __init__(self, name):
        super().__init__(f"BigDrop::{name}")

    def choice(self, valids=None):
        if valids is None:
            valids = self.valid_moves()

        max_weight = 0
        fat = []

        for piece, head in valids:
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


class TableCounter(BigDrop):
    ''' 
    Select the pice with higher score from the pices with most frequent played values
    '''
    def __init__(self, *args):
        super().__init__(*args)


    def count_table(self):
        cant = {}
        pieces = [d[1] for e, *d in self.history if e.name == 'MOVE']
        for p in pieces:
            cant[p[0]] = cant.get(p[0], 0) + 1
            if p[0] != p[1]:
                cant[p[1]] = cant.get(p[1], 0) + 1
        return cant

    
    def choice(self, valids=None):
        if valids is None:
            valids = self.valid_moves()

        best, data = -1, []
        cant = self.count_table()
        for piece, head in valids:
            value = cant.get(piece[piece[0] == self.heads[head]], 0)
            if value > best:
                best, data = value, []
            if value == best:
                data.append((piece, head))
               
        return super().choice(data)


class Supportive(BasePlayer):
    '''
    When the other player of the team is the hand, plays for him.
    '''
    def __init__(self, name):
        super().__init__(f"Supportive::{name}")

    def filter(self, valids=None):
        if valids is None:
            valids = self.valid_moves()
        
        heads = []
        passed = {}
        partner_pieces = {}
        my_pieces = 0
        first_move = True
        for e, *d in self.history:
            if e.name == 'MOVE':
                player, piece, head = d
                if first_move:
                    heads = piece
                    first_move = False
                else:
                    heads[head] = piece[0] if piece[1] == heads[head] else piece[1]
                    if player == self.partner:
                        partner_pieces[heads[head]] = partner_pieces.get(heads[head], 0) + 1
                    elif player == self.me:
                        my_pieces += 1
            elif e.name =='PASS' and d[0] == self.partner:
                h0, h1 = heads
                passed[h0] = True
                passed[h1] = True

        #True if current_player is the hand
        if sum(partner_pieces.values()) < my_pieces:
            return valids

        top = []
        medium = []
        low = []
        for piece, head in valids:
            if passed.get(self.heads[head]):
                top.append((piece, head))
            elif partner_pieces.get(self.heads[head]):
                low.append((piece, head))
            elif (partner_pieces.get(piece[0]) and piece[0] != self.heads[head]) or \
                (partner_pieces.get(piece[1]) and piece[1] != self.heads[head]):
                top.append((piece, head))
            else:
                medium.append((piece, head))

        if top != []:
            return top
        return medium if medium != [] else low
