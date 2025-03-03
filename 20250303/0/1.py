import shlex
import readline

while line := input():
    print(shlex.join(shlex.split(line)))
