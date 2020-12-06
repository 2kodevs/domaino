from ..player import BasePlayer

class Agachao(BasePlayer):
    ''' 
    This player doesn't want to pass, 
    so if there is a number that appears in only one piece, 
    this piece will not be used until there's no other choice.
    '''
    def __init__(self, name):
         super().__init__(f"Agachao::{name}")

    def filter(self, valids=None):
        valids = super().filter(valids)

        def count(piece):
            cant = [0, 0]
            for item in self.pieces:
                cant[0] += (piece[0] in item)
                cant[1] += (piece[1] in item)
            val = min(cant)
            return val, cant.index(val)

        heads = []
        first_move = True
        lru = {}

        for e, *d in self.history:
            if e.name == 'MOVE':
                player, piece, head = d
                if player == self.me:
                    lru[piece[0]] = lru.get(piece[0], 0) + 1
                    lru[piece[1]] = lru.get(piece[1], 0) + 1
                if first_move:
                    heads = list(piece)
                    first_move = False
                else:
                    heads[head] = piece[piece[0] == heads[head]]

        best, data = (-1, -1), []
        for piece, head in valids:
            mn, i = count(piece)
            value = (mn, lru.get(piece[i], 0))
            if value > best:
                best = value
                data.clear()
            if value == best:
                data.append((piece, head))

        return data
                
                    
