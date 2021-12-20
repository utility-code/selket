#!/bin/bash
black "."
pdoc --force --html -o docs selket
python ../pyGroff/runner.py -f "syntax.txt" -o "syntax.pdf" -c -n "Subhaditya Mukherjee" -t "Selket documentation" -e "False"
mv docs/selket/index.html docs/index.md
mv docs/selket/* docs/
if [[ ! -z $1 ]]; then
        git add . && git commit -m $1 && git push
fi
