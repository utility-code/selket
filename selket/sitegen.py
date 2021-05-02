import markdown
import json
from pathlib import Path
from selket.backbone import joinAndMake

"""
This module takes care of Markdown -> HTML and generating the site
"""


def addCSS(md, cssname):
    return f"<!DOCTYPE html>\n<html lang='en'>\n<head>\n<meta charset='utf-8'>\n<link rel='stylesheet' href= './assets/css/{cssname}.html'>\n</head>\n<body>\n{md}\n</body>"


def markToHTML(fpath):
    with open(fpath, "r") as f:
        f = f.read()
        md = markdown.Markdown(
            extensions=["meta", "fenced_code", "sane_lists", "toc", "wikilinks"]
        )
        conv = md.convert(f)
        return addCSS(conv, md.Meta["layout"][0])
