#! /bin/bash

set -euo pipefail
export PYTHONPATH=~/src/dg/Multiplayer-ELO/python

# cp empty.json standings.json
# for round in ../cards/20*.csv; do
#     python add-round.py standings.json "$round" > standings-new.json
#     mv standings-new.json standings.json
# done

# data='../cards/UDisc Scorecards.csv'
data='../cards/UDisc Scorecards_1622132448.csv'
python multiple-rounds.py empty.json "$data" > standings.json

# cat standings.json
