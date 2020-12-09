from ..player import BasePlayer

class NonDouble(BasePlayer):
    ''' This player prefer to play non-double pieces
    '''
    def __init__(self, name):
        super().__init__(f'NonDouble::{name}')

    def filter(self, valids=None):
        valids = super().filter(valids)

        data = []
        for piece, head in valids:
            if piece[0] != piece[1]:
                data.append((piece, head))
        return data if data else valids
        