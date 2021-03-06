#!/usr/bin/python3
import argparse
from domaino.domino import get_hand
from domaino import get_player, get_rule, get_hand, PLAYERS, RULES, BEHAVIORS, HANDS


def info(args):
    information = \
            'Players:\n' + \
            ''.join([f'+ {player.__name__.lower()}\n' for player in PLAYERS]) + \
            '\n' + \
            'Rules:\n' + \
            ''.join([f'+ {rule.__name__.lower()}\n' for rule in RULES]) + \
            '\nOptionally you can merge some players into one passing any amount of them\n' + \
            'separated by a dash(-). Example: BigDrop-Repeater\n' + \
            'Also you can use some extra behaviors in your player mesures.\n' + \
            '\nAvailable behaviors:\n' + \
            ''.join([f'+ {rule.__name__.lower()}\n' for rule in BEHAVIORS]) + \
            '\n' + \
            'Hands:\n' + \
            ''.join([f'+ {hand.__name__.lower()}\n' for hand in HANDS])
    print(information)


def play(args):
    player0 = get_player(args.player0)
    player1 = get_player(args.player1)
    rule = get_rule(args.rule)
    hand = get_hand(args.hand)

    wins = {-1:0, 0:0, 1:0}
    for _ in range(args.rep):
        game = rule()
        wins[game.start(player0, player1, hand, *args.pieces)] += 1
    print(wins)

def main():
    parser = argparse.ArgumentParser("DomAIno")
    parser.add_argument

    subparsers = parser.add_subparsers()
    info_parser = subparsers.add_parser('info', help="Show available Players and Rules")
    info_parser.set_defaults(command=info)

    play_parser = subparsers.add_parser('play', help="Run a dominoe game")
    play_parser.add_argument('-p0',  '--player0',     dest='player0', default='random')
    play_parser.add_argument('-p1',  '--player1',     dest='player1', default='random')
    play_parser.add_argument('-r',   '--rule',        dest='rule',    default='onegame')
    play_parser.add_argument('-n',   '--nine',        dest='pieces',  action='store_const', const=[9,10], default=[])
    play_parser.add_argument('-rep', '--repetitions', dest='rep',     type=int, default=1)
    play_parser.add_argument('-H',   '--hand',        dest='hand',    default='hand_out')

    # play_parser.add_argument('-c', '--count', type=int, dest='count', default=1, help="Number of games to play")
    play_parser.set_defaults(command=play)

    args = parser.parse_args()

    if not hasattr(args, 'command'):
        parser.print_help()
    else:
        args.command(args)

if __name__ == '__main__':
    main()