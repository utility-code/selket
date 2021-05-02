import markdown
import json
from pathlib import Path
from selket.backbone import joinAndMake
from tqdm import tqdm

"""
This module takes care of Markdown -> HTML and generating the site
"""


def markToHTML(fpath):
    with open(fpath, "r") as f:
        f = f.read()
        md = markdown.Markdown(
            extensions=["meta", "fenced_code", "sane_lists", "toc", "wikilinks"]
        )
    conv = md.convert(f)
    layout = md.Meta["layout"][0] + ".html"
    with open(Path.joinpath(Path.cwd() / "_layouts/", layout), "r") as f2:
        f2 = f2.read()
        return f2.replace("{{ content }}", conv)


def listmd(fpath):
    mdLi = [x for x in Path.glob(fpath, "*.md")]
    for fil in mdLi:
        nm = fil.name
        with open(Path.joinpath(Path.cwd(), nm).with_suffix(".html"), "w+") as f:
            f.write(markToHTML(fil))
    mdLi = [x for x in Path.glob(fpath, "*/*.md")]
    for fil in tqdm(mdLi, total=len(mdLi)):
        nm = fil.name
        with open(
            Path.joinpath(Path.cwd() / "_compiled", nm).with_suffix(".html"), "w+"
        ) as f:
            f.write(markToHTML(fil))
