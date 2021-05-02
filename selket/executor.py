from selket.backbone import *
from selket.sitegen import *


def main(ag):
    """
    Because I like minimalism xD
    Just calls everything and is in a different file to keep things separated and to make my life easier
    """
    from pathlib import Path

    print(markToHTML(Path.joinpath(Path.cwd(), "index.md")))
    #  initializeSite(ag)
    #  if ag.p == True:
    #      newPost()
