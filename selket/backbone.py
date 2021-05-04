from pathlib import Path
import os
import shutil
import json
from datetime import datetime

"""
Module to set up the folder, create the needed files etc. Also ability to create new post
"""

list_to_init = [
    "_layouts",
    "assets",
    "assets/js",
    "assets/css",
    "assets/img",
    "_posts",
    "_compiled",
]


def joinAndMake(p1, p2):
    """
    Returns the directory after joining a parent and a directory name, then makes it if it does not exist
    """
    toMake = Path.joinpath(p1, p2)
    if Path.is_dir(toMake) == False and toMake.name != Path.cwd().name:
        Path.mkdir(toMake)
    else:
        return 0


def createConfig(ag, fp):
    """
    Create the config file, json object. Pretty formatted because why not."""
    d_config = {
        "name": ag.n,
        "math": True,
        "toc": True,
        "author": "",
        "title": "",
        "description": "",
        "fenced_code": True,
        "sane_lists": True,
        "wikilinks": True,
        "codehilite": True,
        "date_format": "%Y %B",
        "index_format": '<li><a href = "{link}">{title}: {date}</a><br>{summary}</li>',
    }
    cpath = Path.joinpath(fp, "config.json")
    if Path.is_file(cpath) == False:
        with open(cpath, "w+") as f:
            json.dump(d_config, f, indent=4)


def inits(ag, fpath, newfp):
    """
    Create the required directories
    """
    flag = joinAndMake(fpath, ag.n)
    if flag != 0:
        if len(os.listdir(newfp)) == 0 and ag.p == False:
            for i in list_to_init:
                joinAndMake(newfp, i)

            Path.touch(Path.joinpath(newfp, "index.md"))
            Path.touch(Path.joinpath(newfp / "_layouts", "default.html"))
            Path.touch(Path.joinpath(newfp / "_assets", "style.css"))
            Path.touch(Path.joinpath(newfp, ".nojekyll"))
            Path.touch(Path.joinpath(newfp, "CNAME"))
    print(f"Your site is at : {str(newfp)}")


def initializeSite(ag):
    """
    Create the directories, create config file.
    Also option to delete and recreate everything from scratch (debug lol)
    """
    fpath = Path.cwd()
    newfp = Path.joinpath(fpath, ag.n)
    if ag.f == True:  # clean up
        if input("Are you sure you want to delete everything? y/n/Y/N ") in list("yY"):
            shutil.rmtree(newfp)

    inits(ag, fpath, newfp)
    try:
        createConfig(ag, newfp)
    except FileNotFoundError:
        pass


def postName(name):
    """
    Post name format
    """
    dt = datetime.now().strftime("%Y-%m-%d")
    return f"{dt}-{name.replace(' ', '-')}"


def formatTags(ptags):
    """
    Lowercase tags, strip extra spaces
    """
    t = [x.lower().strip() for x in ptags.split(",")]
    return ",".join(t)


def createPost(fpath, fname, ptags, summary):
    """
    Adds default tags and creates
    """
    fname = Path.joinpath(fpath, fname)
    if Path.is_file(fname) == True:
        print("This already exists. Try again?")
    else:
        print(f"Your post is at : ", fname.with_suffix(".md"))
        with open(fname.with_suffix(".md"), "w+") as f:
            f.write(
                f"---\nlayout: default\ntitle: {fname.name}\ncategories: post\ndate: {datetime.now().strftime('%Y-%m-%d')}\ntags: {formatTags(ptags)}\nsummary: {summary}\n---\n[title]\n\n"
            )


def newPost():
    """
    User input with name and tags
    Calls create function
    """
    fpath = Path.joinpath(Path.cwd(), "_posts")
    pname = input("Post name : ")
    ptags = input("Comma separated tags : ")
    summary = input("One line description : ")
    createPost(fpath, pname, ptags, summary)
