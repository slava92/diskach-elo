"""Calculate ELO standings."""

import argparse
import json

MIN_GAMES = 10


def print_markdown(ranks, matches, alias):
    """Print ratings in markdown format."""
    print('Name|Rank|Rounds')
    print(':---|---:|-----:')
    for name, rank in ranks:
        count = matches[name]
        if count < MIN_GAMES:
            rank2 = f"*{rank}\\**"
        else:
            rank2 = rank
        if name in alias:
            name = alias[name]
        print("%s|%s|%d" % (name, rank2, count))
    print()
    print(f'*\\**: The rank is provisional if less than {MIN_GAMES} cards registered')


def print_text(ranks, matches, alias):
    """Print ratings in plain text format."""
    print("%-13s\t%s%s\t%s" % ('Name', 'Rank', ' ', 'Rounds'))
    for name, rank in ranks:
        count = matches[name]
        provisional = '*' if count < MIN_GAMES else ' '
        if name in alias:
            name = alias[name]
        print("%-13s\t%d%s\t%3d" % (name, rank, provisional, count))


def main():
    """Calculate ELO standings after one round."""
    parser = argparse.ArgumentParser(
        description="Print ratings.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        conflict_handler='resolve')
    parser.add_argument('standings',
                        help='Current standings')
    parser.add_argument('--markdown', action='store_true')
    options = parser.parse_args()

    with open(options.standings) as sf:
        standings = json.load(sf)

    # new_standings = {'elo': new_elos, 'matches': new_counters}
    alias = standings['alias']
    elos = standings['elo']
    matches = standings['matches']
    ranks = sorted(elos.items(), key=lambda m: m[1], reverse=True)
    if options.markdown:
        print_markdown(ranks, matches, alias)
    else:
        print_text(ranks, matches, alias)


if __name__ == '__main__':
    main()
