#!/usr/bin/env bash
cd "$(dirname "$0")"
echo "Preparing template..."
xgettext --output=po/pigment.pot --files-from=po/POTFILES.in
echo "Updating Spanish..."
msgmerge --no-fuzzy-matching -U po/es.po po/pigment.pot