#! /bin/bash

set -euo pipefail

IFS=','
grep ':' "${1:?}" | sed 's/^ *//; s/"//g; s/: */,/; s/,$//' | sort -rn -k 2 -t ',' | while read -r name rate; do
    printf "%12s\t%d\n" $name $rate
done

