from ..player import BasePlayer
from random import choice

class Higher(BasePlayer):
    ''' Play higher if possible as the first move of the game
    '''
    def __init__(self, name):
        super().__init__(f'Higher::{name}')

    def filter(self, valids=None):
        valids = super().filter(valids)

        if self.heads != [-1, -1]:
            return valids
        
        cant = {}
        for p0, p1 in self.pieces:
            if p0 != p1:
                cant[p1] = cant.get(p1, 0) + 1
            cant[p0] = cant.get(p0, 0) + 1

        filtered = [(num, c) for num, c in cant.items()]

        best = max(filtered)[0]
        pieces = [p for p in self.pieces if best in p]

        if (best, best) in pieces:
            return [((best, best), 0)]
        return [(p, 0) for p in pieces]
    
