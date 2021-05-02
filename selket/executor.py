from selket.backbone import *
from selket.sitegen import *
from pathlib import Path

"""
Because I like minimalism xD
Just calls everything and is in a different file to keep things separated and to make my life easier
"""


def main(ag):
    """
    Just calls everything else
    """
    print(listmd(Path.cwd()))
    initializeSite(ag)
    if ag.p == True:
        newPost()
