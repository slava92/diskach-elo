#! /bin/bash

set -euo pipefail
export PYTHONPATH=~/src/dg/Multiplayer-ELO/python
data_dir=CombinedScorecards

cp empty.json standings.json
for round in "$data_dir"/*.csv; do
    if (( $(wc -l "$round") > 3 )); then
        python add-round.py standings.json "$round" > standings-new.json
        mv standings-new.json standings.json
    fi
done

cat standings.json
