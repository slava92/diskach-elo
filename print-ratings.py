"""Calculate ELO standings."""

import argparse
import json

MIN_GAMES = 10


def main():
    """Calculate ELO standings after one round."""
    parser = argparse.ArgumentParser(
        description="Print ratings.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        conflict_handler='resolve')
    parser.add_argument('standings',
                        help='Current standings')
    options = parser.parse_args()

    with open(options.standings) as sf:
        standings = json.load(sf)

    # new_standings = {'elo': new_elos, 'matches': new_counters}
    elos = standings['elo']
    matches = standings['matches']
    ranks = sorted(elos.items(), key=lambda m: m[1], reverse=True)
    print("%-13s\t%s%s\t%s" % ('Name', 'Rank', ' ', 'Rounds'))
    for name, rank in ranks:
        count = matches[name]
        provisional = '*' if count < MIN_GAMES else ' '
        print("%-13s\t%d%s\t%3d" % (name, rank, provisional, count))


if __name__ == '__main__':
    main()
