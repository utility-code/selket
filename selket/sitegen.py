import markdown
import json
from pathlib import Path
from tqdm import tqdm
import http.server
import socketserver
from datetime import datetime

"""
This module takes care of Markdown -> HTML and generating the site
"""


def serve():
    """
    Local server creation on given port
    """
    handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", 0), handler) as httpd:
        print(
            "Server started at localhost:"
            + " http://0.0.0.0:"
            + str(httpd.server_address[1])
        )
        httpd.serve_forever()


def count_from_json(js, index, hashed=True):
    """
    Since the json for every post is in order, this just returns the element at the position supplied and its count. In most cases, this would be a unique list of elements
    """
    counter = []
    for i in js:
        counter.append(js[i][index])
    counter = [x for x in counter if len(x) > 0]
    if hashed == True:
        counter = set(counter)
    return counter, len(counter)


def state_vars():
    """
    Read the config, add some extra essentials from the indexed documents
    """
    with open(Path.joinpath(Path.cwd(), "config.json"), "r") as f:
        d_vars = json.load(f)
        indexPath = Path.joinpath(Path.cwd(), "indexed.json")
        d_vars["index_path"] = indexPath
        try:
            with open(indexPath, "r") as f2:
                indexed = json.load(f2)
                d_vars["total_posts"] = len(indexed.keys())
                d_vars["categories"] = count_from_json(indexed, 1)[0]
        except FileNotFoundError:
            pass

    return d_vars


def returnIndex(statev):
    strsend = "<ul>\n"
    with open(statev["index_path"], "r") as f:
        all_files = json.load(f)

    for i in all_files.keys():
        temp = all_files[i]
        strsend += f"""<li>
        <a href = ./_compiled/{i.split('.')[0]+'.html'}>{temp[3]}</li>"""

    return strsend + "\n<ul>\n"


def replacerHTML(fil, statev, conv, meta_lis):
    """
    Takes the file, replaces whatever is needed to compile in the html
    """
    dict_replacer = {
        "[content]": conv,
        "[index]": returnIndex(statev),
        "[total_posts]": str(statev["total_posts"]),
        "[title]": f"<h1>{str(meta_lis[3])}</h1>\n\n",
    }

    for i in dict_replacer.keys():
        fil = fil.replace(i, dict_replacer[i])
    return fil


def markToHTML(fpath, statev):
    """
    Converts from markdown to HTML given some addons (user can add)
    """
    with open(fpath, "r") as f:
        f = f.read()
        extensions = ["meta"]
        for i in ["fenced_code", "sane_lists", "wikilinks", "toc"]:
            if statev[i] == True:
                extensions.append(i)
        md = markdown.Markdown(extensions=extensions)
        conv = md.convert(f)
        layout = md.Meta["layout"][0] + ".html"
        with open(Path.joinpath(Path.cwd() / "_layouts/", layout), "r") as f2:
            f2 = f2.read()
            meta_lis = []
            for metas in ["layout", "categories", "tags", "title", "date"]:
                try:
                    if metas == "tags":
                        meta_lis.append(md.Meta[metas][0].split(" "))
                    else:
                        meta_lis.append(md.Meta[metas][0])
                except KeyError:
                    meta_lis.append("")
            layout = md.Meta["layout"]
            return replacerHTML(f2, statev, conv, meta_lis), meta_lis


def mdtoIndex(fpath):
    with open(fpath, "r") as f:
        f = f.read()
        md = markdown.Markdown(extensions=["meta"])
        md.convert(f)
        meta_lis = []
        for metas in ["layout", "categories", "tags", "title"]:
            try:
                if metas == "tags":
                    meta_lis.append(md.Meta[metas][0].split(" "))
                else:
                    meta_lis.append(md.Meta[metas][0])
            except KeyError:
                meta_lis.append("")
        return meta_lis


def create_index(fpath):
    mdLi = [x for x in Path.glob(fpath, "*/*.md")]
    indexed = {}
    for fil in tqdm(mdLi, total=len(mdLi)):
        mfile = mdtoIndex(fil)
        nm = fil.name
        indexed[nm] = mfile

    with open(Path.cwd() / "indexed.json", "w+") as f:
        json.dump(indexed, f, indent=4, sort_keys=True)


def compilemd(fpath, statev):
    """
    Goes through all markdown documents. One for the root and the other for the posts directory, converts and compiles them to html with add ons specified and substitues whatever is in the state variables.
    Also indexes the files for access to information
    """
    # root directory
    mdLi = [x for x in Path.glob(fpath, "*.md")]
    for fil in mdLi:
        nm = fil.name
        with open(Path.joinpath(Path.cwd(), nm).with_suffix(".html"), "w+") as f:
            f.write(markToHTML(fil, statev)[0])

    # posts directory
    mdLi = [x for x in Path.glob(fpath, "*/*.md")]
    for fil in tqdm(mdLi, total=len(mdLi)):
        mfile = markToHTML(fil, statev)
        nm = fil.name
        with open(
            Path.joinpath(Path.cwd() / "_compiled", nm).with_suffix(".html"), "w+"
        ) as f:
            f.write(mfile[0])
