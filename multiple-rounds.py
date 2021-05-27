"""Calculate ELO standings."""

import argparse
import csv
import itertools
import json

import elo


def main():
    """Calculate ELO standings after one round."""
    parser = argparse.ArgumentParser(
        description="Calculate ELO based on previous standings and one round.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        conflict_handler='resolve')
    parser.add_argument('standings',
                        help='Current standings')
    parser.add_argument('rounds',
                        help='Results for multiple rounds of play')
    options = parser.parse_args()

    standings = dict()
    with open(options.standings) as sf:
        standings = json.load(sf)

    plays = []
    with open(options.rounds) as rf:
        reader = csv.DictReader(rf)
        for row in reader:
            plays.append([row['PlayerName'], row['Total'], row['Date']])
    plays = sorted(plays, key=lambda r: r[2])

    for k, g in itertools.groupby(plays, key=lambda r: r[2]):
        players = sorted(list(g), key=lambda r: r[1])
        prev_total = 0
        prev_place = 0
        match = elo.ELOMatch()
        for place, (name, total, _) in enumerate(players, start=1):
            if name == 'Par':
                continue
            prev_elo = standings[name] if name in standings else 1500
            if total == prev_total:
                place = prev_place
            match.addPlayer(name, place, prev_elo)
            prev_total, prev_place = total, place

        try:
            match.calculateELOs()
        except ZeroDivisionError:
            pass
        else:
            for name, total, _ in players:
                if name != 'Par':
                    standings[name] = match.getELO(name)

    print(json.dumps(standings, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
