from domaino.players import strategies
from domaino import RULES, PLAYERS, BEHAVIORS, get_player
from main import play
import json
import argparse

class Arguments: pass
non_valid = ['SimpleHybrid', 'MonteCarlo', 'Supportive', 'Casino']

prefix = ["", "Supportive-"]
non_valid = ['SimpleHybrid', 'MonteCarlo', 'Supportive', 'Casino']
random = get_player('random')

def all(args):
    data = {}
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
                            args.player1 = f'{b.__name__}-{prefix[idx]}{p1.__name__}'
                            args.rule    = r.__name__
                            args.rep     = 500
                            args.pieces  = g[1]
                            args.hand    = 'hand_out'
                            d3[p1.__name__] = play(args)[0] / 5
    json.dump(data, open('data.json', 'w'), indent=4)

def casino_vs_bota():
    data = {}
    players = [('Casino', 'Casino-Supportive-DataDropper'), ('BigDrop', 'Supportive-BigDrop')]
    for p1 in players:
        d1 = data[p1[0]] = {}
        for p2 in PLAYERS:
            if p2.__name__ in non_valid:
                continue
            args = Arguments()
            args.player0 = p1[1]
            args.player1 = f'Supportive-{p2.__name__}'
            args.rule    = "OneGame"
            args.rep     = 500
            args.pieces  = [9, 10]
            args.hand    = 'data_zero'
            d1[p2.__name__] = play(args)[0] / 5
    json.dump(data, open('data_casino.json', 'w'), indent=4)

    
def sim_data_opponent(args):
    data = {}

    d0 = {}
    for b in [random, *BEHAVIORS]:
        if b.__name__ in non_valid:
            continue
        d1 = d0[b.__name__] = {}
        for idx, t in enumerate(['Normal', 'Supportive']):
            d2 = d1[t] = {}
            for p0 in ['DataDropper', 'DataKeeper']:
                d3 = d2[p0] = {}
                for p1 in PLAYERS:
                    if p1.__name__ in non_valid:
                        continue
                    args = Arguments()
                    args.player0 = f'{b.__name__}-{prefix[idx]}{p0}'
                    args.player1 = f'{b.__name__}-{prefix[idx]}{p1.__name__}'
                    args.rule    = 'OneGame'
                    args.rep     = 500
                    args.pieces  = ('9x9', [9,10])
                    args.hand    = 'data_opponent'
                    d3[p1.__name__] = play(args)[0] / 5
    json.dump(data, open('data.json', 'w'), indent=4)

def sim_data_partner(args):
    data = {}

    d0 = {}
    for b in [random, *BEHAVIORS]:
        if b.__name__ in non_valid:
            continue
        d1 = d0[b.__name__] = {}
        for idx, t in enumerate(['Normal', 'Supportive']):
            d2 = d1[t] = {}
            for p1 in PLAYERS:
                if p1.__name__ in non_valid:
                    continue
                args = Arguments()
                args.player0 = f'best-Supportive-DataDropper'
                args.player1 = f'{b.__name__}-{prefix[idx]}{p1.__name__}'
                args.rule    = 'OneGame'
                args.rep     = 500
                args.pieces  = ('9x9', [9,10])
                args.hand    = 'data_partner'
                d2[p1.__name__] = play(args)[0] / 5
        
    json.dump(data, open('data.json', 'w'), indent=4)

def sim_doubles(args):
    data = {}

    d0 = {}
    for b in [random, *BEHAVIORS]:
        if b.__name__ in non_valid:
            continue
        d1 = d0[b.__name__] = {}
        for idx, t in enumerate(['Normal', 'Supportive']):
            d2 = d1[t] = {}
            for p1 in PLAYERS:
                if p1.__name__ in non_valid:
                    continue
                args = Arguments()
                args.player0 = f'BestAccompanied-AlwaysDouble'
                args.player1 = f'{b.__name__}-{prefix[idx]}{p1.__name__}'
                args.rule    = 'OneGame'
                args.rep     = 500
                args.pieces  = ('9x9', [9,10])
                args.hand    = 'doubles'
                d2[p1.__name__] = play(args)[0] / 5
        
    json.dump(data, open('data.json', 'w'), indent=4)

def sim_data_opponent(args):
    data = {}
    players = ['Casino-DataDropper', 'BigDrop']

    d0 = {}
    for b in [random, *BEHAVIORS]:
        if b.__name__ in non_valid:
            continue
        d1 = d0[b.__name__] = {}
        for idx, t in enumerate(['Normal', 'Supportive']):
            d2 = d1[t] = {}
            for i, p0 in enumerate(['DataDropper', 'BigDrop']):
                d3 = d2[p0] = {}
                for p1 in PLAYERS:
                    if p1.__name__ in non_valid:
                        continue
                    args = Arguments()
                    args.player0 = players[i]
                    args.player1 = f'{b.__name__}-{prefix[idx]}{p1.__name__}'
                    args.rule    = 'OneGame'
                    args.rep     = 500
                    args.pieces  = ('9x9', [9,10])
                    args.hand    = 'data_zero'
                    d3[p1.__name__] = play(args)[0] / 5
    json.dump(data, open('data.json', 'w'), indent=4)

def main():
    parser = argparse.ArgumentParser("DomAIno-Simulations")
    parser.add_argument

    subparsers = parser.add_subparsers()
    all_parser = subparsers.add_parser('all_vs_all', help="Play every posible combination of a strategies against" + \
                                        "all strategies")
    all_parser.set_defaults(command=all)

if __name__ == "__main__":
    casino_vs_bota()
