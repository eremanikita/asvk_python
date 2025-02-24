import sys
import cowsay
import glob

files = glob.glob("*.cow")
for i in files:
    tmp = input()
    with open(i, "r") as f:
        the_cow = cowsay.read_dot_cow(f)

    print(cowsay.cowsay("QQ", cowfile=the_cow))