#!/usr/bin/env bash
cd "$(dirname "$0")"
echo "Preparing template..."
xgettext --output=po/pigment.pot --files-from=po/POTFILES.in
echo "Updating Spanish..."
msgmerge --no-fuzzy-matching -U po/es.po po/pigment.pot
echo "Updating Telugu..."
msgmerge --no-fuzzy-matching -U po/te.po po/pigment.pot
echo "Updating German..."
msgmerge --no-fuzzy-matching -U po/de.po po/pigment.pot
echo "Updating Dutch..."
msgmerge --no-fuzzy-matching -U po/nl.po po/pigment.pot