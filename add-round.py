"""Calculate ELO standings."""

import argparse
import collections
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
    parser.add_argument('new_standings',
                        help='New standings')
    options = parser.parse_args()

    with open(options.standings) as sf:
        standings = json.load(sf)

    match = elo.ELOMatch()
    players = []
    ignore = standings['ignore']

    with open(options.round) as rf:
        reader = csv.DictReader(rf)
        for row in reader:
            if row['PlayerName'] not in ignore:
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

    if len(players) < 3:
        # print(players, file=sys.stderr)
        new_standings = standings
    else:
        match.calculateELOs()
        new_elos = dict(standings['elo'])
        new_counters = collections.defaultdict(int, standings['matches'])
        for name, total in players:
            new_elos[name] = match.getELO(name)
            new_counters[name] += 1

        new_standings = {'elo': new_elos,
                         'ignore': ignore,
                         'matches': new_counters}

    with open(options.new_standings, "w") as nf:
        json.dump(new_standings, nf, sort_keys=True, indent=2)


if __name__ == '__main__':
    main()
