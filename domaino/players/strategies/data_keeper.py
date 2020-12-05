from ..player import BasePlayer

class DataKeeper(BasePlayer):
    '''
    Player who keeps his most repeated pieces.
    '''
    def __init__(self, name):
        super().__init__(f"DataKeeper::{name}")

    def filter(self, valids=None):
        valids = super().filter(valids)

        datas = {}
        for p1, p2 in self.pieces:
            if p1 != p2:
                datas[p2] = datas.get(p2, 0) + 1
            datas[p1] = datas.get(p1, 0) + 1
        
        pieces = {x for p, h in valids for x in p}
        temp = [(c, v) for v, c in datas.items() if v in pieces]
        temp.sort(reverse=True)
        
        best, selected = temp[0][0], set()
        for piece, head in valids:
            value = [datas.get(piece[0], 0), datas.get(piece[1], 0)]

            for i in range(2):
                if datas.get(piece[i], 0) < best:
                    best = value[i]
                    selected.clear()
                    selected.add((piece, head))
                else:
                    selected.add((piece, head))

        return list(selected)
        