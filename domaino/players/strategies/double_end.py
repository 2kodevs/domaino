from ..player import BasePlayer

class DoubleEnd(BasePlayer):
    ''' 
    This player always selects a double piece if possible to make a move at the end of the game.
    '''
    def __init__(self, name):
         super().__init__(f"AlwaysDouble::{name}")

    def filter(self, valids=None):
        valids = super().filter(valids)

        data = []
        for piece, head in valids:
            if piece[0] == piece[1]:
                data.append((piece, head))

        if data:
            heads = []
            player_pieces = {}
            first_move = True
            for e, *d in self.history:
                if e.name == 'MOVE':
                    player, piece, head = d
                    if first_move:
                        heads = list(piece)
                        first_move = False
                    else:
                        heads[head] = piece[piece[0] == heads[head]]
                    player_pieces[player] = player_pieces.get(player, 0) + 1

            if not any([self.pieces_per_player - x <= 2 for x in player_pieces.values()]):
                data.clear()

        return data if data else valids
                
                    
