from pathlib import Path
import os
import shutil
import json
from datetime import datetime

list_to_init = [
    "_layouts",
    "assets",
    "assets/js",
    "assets/css",
    "_posts",
    "_compiled",
    ".nojekyll",
]


def joinAndMake(p1, p2):
    """
    Returns the directory after joining a parent and a directory name, then makes it if it does not exist
    """
    toMake = Path.joinpath(p1, p2)
    if Path.is_dir(toMake) == False:
        Path.mkdir(toMake)


def createConfig(ag, fp):
    """
    Create the config file, json object. Pretty formatted because why not.
    """
    d_config = {
        "name": ag.n,
        "math": True,
        "toc": True,
        "author": "",
        "title": "",
        "description": "",
    }
    cpath = Path.joinpath(fp, "config.json")
    if Path.is_file(cpath) == False:
        with open(cpath, "w+") as f:
            json.dump(d_config, f, indent=4)


def inits(ag, fpath, newfp):
    """
    Create the required directories
    """
    joinAndMake(fpath, ag.n)
    if len(os.listdir(newfp)) == 0 and ag.p == False:
        for i in list_to_init:
            joinAndMake(newfp, i)

        Path.touch(Path.joinpath(newfp, "index.md"))
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
    createConfig(ag, newfp)


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


def createPost(fpath, fname, ptags):
    """
    Adds default tags and creates
    """
    fname = Path.joinpath(fpath, fname)
    if Path.is_file(fname) == True:
        print("This already exists. Try again?")
    else:
        print(fname)
        with open(fname.with_suffix(".md"), "w+") as f:
            f.write(
                f"---\nlayout : default\ndate: {datetime.now().strftime('%Y-%m-%d')}\ntags: {formatTags(ptags)}\n---\n"
            )


def newPost():
    """
    User input with name and tags
    Calls create function
    """
    fpath = Path.joinpath(Path.cwd(), "_posts")
    print(fpath)
    pname = input("Post name : ")
    ptags = input("Comma separated tags : ")
    createPost(fpath, pname, ptags)
