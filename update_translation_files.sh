#!/usr/bin/env bash

cd "$(dirname "$0")"

echo "Preparing template..."
xgettext --output=po/pigment.pot --files-from=po/POTFILES.in

declare -A languages=(
    [es]="Spanish"
    [te]="Telugu"
    [de]="German"
    [nl]="Dutch"
)

for code in "${!languages[@]}"; do
    echo "Updating ${languages[$code]}..."
    msgmerge --no-fuzzy-matching -U "po/$code.po" po/pigment.pot
done
