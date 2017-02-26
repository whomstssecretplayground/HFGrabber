import time
import os
import sys
import multiprocessing
import threading

WISHLIST_FILE = os.getcwd() + "/wishlist.txt"

def create_wishlist():
    os.chdir(os.getcwd())
    if not os.path.exists(WISHLIST_FILE) or os.stat(WISHLIST_FILE).st_size == 0:
        open(WISHLIST_FILE, "a+").close()
        os.chmod(WISHLIST_FILE, 0o666)
        print("Please enter the Names of the Artists you would like to grapple.")
        print("Will now exit!")
        time.sleep(5)
        exit(0)
    return

def init():
    with open(WISHLIST_FILE, "r") as wishlist:
        for line in wishlist:
            if not line.startswith("#") and not line == "\n" and not line == "":
                line = line.replace('\n', '')
                artistdir = os.getcwd + "/" + line
                if not os.path.exists(artistdir):
                    os.mkdir(artistdir)
                    os.chmod(artistdir, 0o775)
                

def main():
    pass

main()