#! /bin/bash

set -euo pipefail

# Join array of strings into a string using a separator.
# NOTE: the array to be joined is passed to the function by name (not by value)
# Usage: a=(1 2 3); run.join_array '|' a  # <- 'a' is a name, not value of 'a'
# Result: 1|2|3
join_array() {
    local IFS="$1"; shift
    local arg1="$1[@]"
    local -a list=("${!arg1}")
    echo "${list[*]}"
}

# data_file='../cards/UDisc Scorecards.csv'
data_file='../cards/UDisc Scorecards_1622132448.csv'

output=${data_file##*/}
output=${output%.csv}
mkdir -p "${output:?}"
rm -fr "${output:?}"/*

cat "$data_file" | {
    read -r header
    echo "$header" >&2
    IFS=','
    while read -ra data; do
        save_to="$output/${data[3]}.csv"
        echo "$save_to" >&2
        if [[ ! -f "$save_to" ]]; then
            echo "$header" > "$save_to"
        fi
        join_array ',' data >> "$save_to"
    done
}

# PlayerName,CourseName,LayoutName,Date,Total,+/-,Hole1,Hole2,Hole3,Hole4,Hole5,Hole6,Hole7,Hole8,Hole9,Hole10,Hole11,Hole12,Hole13,Hole14,Hole15,Hole16,Hole17,Hole18
