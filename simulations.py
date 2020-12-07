from domaino import RULES, PLAYERS, BEHAVIORS, get_player
from main import play
import json

class Arguments: pass

if __name__ == "__main__":
    data = {}
    prefix = ["", "Supportive-"]
    non_valid = ['SimpleHybrid', 'MonteCarlo', 'Supportive', 'Casino']
    random = get_player('random')


    for g in [('9x9', [9,10]), ('6x6', [])]:
        d0 = data[g[0]] = {}
        for r in RULES:
            d1 = d0[r.__name__] = {}
            for b in [random, *BEHAVIORS]:
                if b.__name__ in non_valid:
                    continue
                d4 = d1[b.__name__] = {}
                for idx, t in enumerate(['Normal', 'Supportive']):
                    d2 = d4[t] = {}
                    for p0 in PLAYERS:
                        if p0.__name__ in non_valid:
                            continue
                        d3 = d2[p0.__name__] = {}
                        for p1 in PLAYERS:
                            if p1.__name__ in non_valid:
                                continue
                            args = Arguments()
                            args.player0 = f'{b.__name__}-{prefix[idx]}{p0.__name__}'
                            args.player1 = f'{prefix[idx]}{p1.__name__}'
                            args.rule    = r.__name__
                            args.rep     = 100
                            args.pieces  = g[1]
                            args.hand    = 'hand_out'
                            d3[p1.__name__] = play(args)[0]
    json.dump(data, open('data.json', 'w'), indent=4)
