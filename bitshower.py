# Copyright James Flanagan 2014.
# Provided under the MIT license (see the LICENSE file).

# TODO: add some more comments!


# * pyaudio is used for playing the background music.
# * wave is used for reading the wav file that contains the background music.
# * threading is used to run the program on multiple threads at once, so the audio can be played while the animation is displayed.
import pyaudio, wave, threading

from random import randint, randrange


# console_size is used to find out the size of the window the program is running in.
import console_size

# Get the size of the console.
(CONSOLE_WIDTH, CONSOLE_HEIGHT) = console_size.getTerminalSize()


# CONFIGURATION FOR ANIMATION #
# =========================== #

MAX_LENGTH = 10

MAX_CHANGE_EACH_TIME = int(CONSOLE_WIDTH / 5)

#    END OF CONFIGURATION     #
#    --------------------     #


# Used for sound generation.
CHUNK = 1024

# Used to generate a random bit to display on the screen in the animation.
randbit = lambda: randint(0, 1)

def generateLines():
    """Generate a random set of column numbers of random length, each of which respresents a line going down the screen. This can be used to create a list of lines to remove from, or add to the screen."""
    lines = set()

    # Generate the number of lines to be chosen, which must be between 1 and MAX_CHANGE_EACH_TIME.
    numToChange = randint(1, MAX_CHANGE_EACH_TIME)

    # Generate the column numbers for the lines.
    for i in range(numToChange):
        lines.add(randrange(CONSOLE_WIDTH))

    return lines

def displayAnimation():
    """Displays the actual animation."""

    lines = set()

    # Loop forever.
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

def playMusic():
    """Loops a sound widget"""

    def readSoundFile():
        """Gets sound from the file."""

        # Use wave module to open the wav file.
        return wave.open('sound.wav', 'rb')

    sounds = readSoundFile()

    # Initialise pyaudio instance.
    pa = pyaudio.PyAudio()

    # Open output stream.
    stream = pa.open(format=pa.get_format_from_width(sounds.getsampwidth()),
                   channels=sounds.getnchannels(),
                       rate=sounds.getframerate(),
                     output=True)

    # Play the sound effect forever.
    while True:
        # Read the next chunk of data from the wav file.
        data = sounds.readframes(CHUNK)

        # While data is being read.
        while data != '':
            # Write data onto the stream to play it.
            stream.write(data)

            # Read the next chunk of data from the wav file.
            data = sounds.readframes(CHUNK)

        # Rewind the track to the beginning.
        sounds.rewind()


# Create and run a second thread which plays the sound.
threading.Thread(target = playMusic).start()

# Begin your hacking adventure!
displayAnimation()
