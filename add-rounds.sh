#! /bin/bash

set -euo pipefail
export PYTHONPATH=~/src/dg/Multiplayer-ELO/python
data_dir=CombinedScorecards

cp empty.json standings.json
for round in "$data_dir"/20*.csv; do
    python add-round.py standings.json "$round" standings-new.json
    mv standings-new.json standings.json
done

python print-ratings.py standings.json --markdown > standings.md
python print-ratings.py standings.json
