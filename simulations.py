from domaino.players import strategies
from domaino import RULES, PLAYERS, BEHAVIORS, get_player
from main import play
import json

class Arguments: pass
non_valid = ['SimpleHybrid', 'MonteCarlo', 'Supportive', 'Casino']

prefix = ["", "Supportive-"]
non_valid = ['SimpleHybrid', 'MonteCarlo', 'Supportive', 'Casino']
random = get_player('random')

interesting_data = [
    [False, 'data_zero', ('Casino', 'Casino-Supportive-DataDropper'), ('BigDrop', 'Supportive-BigDrop')],
    [True,  'data_opponent', ('DataDropper', 'Supportive-DataDropper'), ('DataKeeper', 'Supportive-DataKeeper')],
    [False, 'data_partner', ('DataDropper', 'Supportive-DataDropper')],
    [False, 'doubles', ('AlwaysDouble', 'AlwaysDouble-Supportive')]
]

def all(args):
    data = {}
    for g in [('9x9', [9,10]), ('6x6', [])]:
        d0 = data[g[0]] = {}
        for r in RULES:
            d1 = d0[r.__name__] = {}
            for b in [random, *BEHAVIORS]:
                if b.__name__ in non_valid:
                    continue
                d2 = d1[b.__name__] = {}
                for idx, t in enumerate(['Normal', 'Supportive']):
                    d3 = d2[t] = {}
                    for p0 in PLAYERS:
                        if p0.__name__ in non_valid:
                            continue
                        d4 = d3[p0.__name__] = {}
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
                            d4[p1.__name__] = play(args)[0] / 5
    json.dump(data, open('json_data/data.json', 'w'), indent=4)

def sim(swap, hand, *players):
    data = {}
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
            args.hand    = hand
            if swap: 
                args.player0, args.player1 = args.player1, args.player0
            d1[p2.__name__] = play(args)[0] / 5
    json.dump(data, open(f'json_data/{hand}.json', 'w'), indent=4)

def custom(args):
    if 0 <= args.number < len(interesting_data):
        sim(*interesting_data[args.number])
    else:
        for test in interesting_data:
            sim(*test)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("DomAIno-simulations")

    subparsers = parser.add_subparsers()
    all_parser = subparsers.add_parser('all', help="Run a big suite of cases using different domino sizes, rules, player startegies and behaviors")
    all_parser.set_defaults(command=all)

    custom_parser = subparsers.add_parser('custom', help="Run a suite of interesting cases, listed in the array `interesting-data`")
    custom_parser.add_argument('-n',  '--number', type=int, default=-1, help='Test number in range [0, 4]')
    custom_parser.set_defaults(command=custom)

    args = parser.parse_args()

    if not hasattr(args, 'command'):
        parser.print_help()
    else:
        args.command(args)
