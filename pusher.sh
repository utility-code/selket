black "."
pdoc --force --html -o docs pygroff
mv docs/selket/index.html docs/index.md
mv docs/selket/* docs/
if [[ ! -z $1 ]]; then
        git add . && git commit -m $1 && git push
fi
