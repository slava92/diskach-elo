"""Calculate ELO standings."""

import argparse
import csv
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
    parser.add_argument('round',
                        help='Results for one round of play')
    options = parser.parse_args()

    with open(options.standings) as sf:
        standings = json.load(sf)

    match = elo.ELOMatch()
    players = []

    with open(options.round) as rf:
        reader = csv.DictReader(rf)
        for row in reader:
            players.append((row['PlayerName'], row['Total']))

    players = sorted(players, key=lambda r: r[1])
    prev_total = 0
    prev_place = 0
    for place, (name, total) in enumerate(players, start=1):
        prev_elo = standings[name] if name in standings else 1500
        if total == prev_total:
            place = prev_place
        match.addPlayer(name, place, prev_elo)
        prev_total, prev_place = total, place

    match.calculateELOs()

    new_standins = dict(standings)
    for name, total in players:
        if name != 'Par':
            new_standins[name] = match.getELO(name)

    print(json.dumps(new_standins, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
