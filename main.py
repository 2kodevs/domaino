#!/usr/bin/python3
import argparse
from domaino import get_player, get_rule


def info(args):
    information = \
            'Players:\n' + \
            ''.join([f'+ {player.__name__.lower()}\n' for player in PLAYERS]) + \
            '\n' + \
            'Rules:\n' +\
            ''.join([f'+ {rule.__name__.lower()}\n' for rule in RULES])
    print(information)


def play(args):
    player0 = get_player(args.player0)
    player1 = get_player(args.player1)
    rule = get_rule(args.rule)

    game = rule()
    game.start(player0, player1, *args.pieces)


def main():
    parser = argparse.ArgumentParser("DomAIno")
    parser.add_argument

    subparsers = parser.add_subparsers()
    info_parser = subparsers.add_parser('info', help="Show available Players and Rules")
    info_parser.set_defaults(command=info)

    play_parser = subparsers.add_parser('play', help="Run a dominoe game")
    play_parser.add_argument('-p0', '--player0', dest='player0', default='random')
    play_parser.add_argument('-p1', '--player1', dest='player1', default='random')
    play_parser.add_argument('-r', '--rule', dest='rule', default='onegame')
    play_parser.add_argument('-n', '--nine', dest='pieces', action='store_const', const=[9,10], default=[])
    # play_parser.add_argument('-c', '--count', type=int, dest='count', default=1, help="Number of games to play")
    play_parser.set_defaults(command=play)

    args = parser.parse_args()

    if not hasattr(args, 'command'):
        parser.print_help()
    else:
        args.command(args)

if __name__ == '__main__':
    main()