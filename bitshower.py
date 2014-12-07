# Copyright James Flanagan 2014.
# Provided under the MIT license (see the LICENSE file).

# TODO: add some more comments!

from random import randint, randrange
import console_size

(CONSOLE_WIDTH, CONSOLE_HEIGHT) = console_size.getTerminalSize()

MAX_LENGTH = 10

MAX_CHANGE_EACH_TIME = int(CONSOLE_WIDTH / 5)


randbit = lambda: randint(0, 1)

def generateLines():
    lines = set()

    numToChange = randint(1, MAX_CHANGE_EACH_TIME)

    for i in range(numToChange):
        lines.add(randrange(CONSOLE_WIDTH))
    
    return lines


lines = set()

while True:
    if len(lines) > 0 + MAX_CHANGE_EACH_TIME:
        lines -= generateLines()
    
    if len(lines) < CONSOLE_WIDTH - MAX_CHANGE_EACH_TIME:
        lines |= generateLines()

    linesList = list(lines)

    linesList.sort()

    for i, l in enumerate(linesList):
        if i == 0:
            numSpacesToAdd = l
        else:
            # Have to -1 since one of the columns will have already been used up
            # by the previous line.
            numSpacesToAdd = l - linesList[i-1] - 1

        print(" " * numSpacesToAdd + str(randbit()), end='')

    print()
