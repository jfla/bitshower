# Copyright James Flanagan 2014.
# Provided under the MIT license (see the LICENSE file).

# TODO: add some more comments!

#import audio module, 'wave' sound file module, and multiple thread module
import pyaudio, wave, threading
#import some stuff from the random module
from random import randint, randrange
#import module to find console size
import console_size
#the consol_size and pyaudio modules can be accessed from the files above.

#globalise constants
#used for matrix generator (main)
global CONSOLE_WIDTH
global CONSOLE_HEIGHT
(CONSOLE_WIDTH, CONSOLE_HEIGHT) = console_size.getTerminalSize()

global MAX_LENGTH
MAX_LENGTH = 10

global MAX_CHANGE_EACH_TIME
MAX_CHANGE_EACH_TIME = int(CONSOLE_WIDTH / 5)

#used for sound
global CHUNK
CHUNK = 1024

#random bit lambda function
randbit = lambda: randint(0, 1)


def generateLines():
    """generates something that's used in procedure main
    jfla can explain it"""
    lines = set()

    numToChange = randint(1, MAX_CHANGE_EACH_TIME)

    for i in range(numToChange):
        lines.add(randrange(CONSOLE_WIDTH))
    
    return lines
    
    
class Application():
    """a class with most of the stuff for running the program in it"""
    
    def __init__(self):
        """runs when an application object is created"""
        # instantiate PyAudio
        self.p = pyaudio.PyAudio()
        """get sound from file and
        create a stream to stream it on"""
        self.sound()
        #something to do with matrix generator
        self.lines = set()
        #begin program
        self.begin()

    def sound(self):
        """gets sound from a file"""
        #use wave module to open a wav file
        self.sounds = wave.open('/Users/glenmcconkey/Documents/Almanzos_folder/Python_music/matrix.wav', 'rb')
        # open stream
        self.stream = self.p.open(format=self.p.get_format_from_width(self.sounds.getsampwidth()),
                channels=self.sounds.getnchannels(),
                rate=self.sounds.getframerate(),
                output=True)


    def playMusic(self): 
        """loops a sound widget"""
        #loop forever
        while True:
            # read the next chunk of data from the wav file
            self.data = self.sounds.readframes(CHUNK)
            #while data is being read
            while self.data != '':
                #write data onto the stream to play it
                self.stream.write(self.data)
                #read the next chunk of data from the wav file
                self.data = self.sounds.readframes(CHUNK)
            #rewind the track to the beginning
            self.sounds.rewind()
        
        
    def main(self):
        """runs the matrix generator part of the program"""
        #loops forever
        while True:
            #ask jfla how this bit works
            if len(self.lines) > 0 + MAX_CHANGE_EACH_TIME:
                self.lines -= generateLines()
        
            if len(self.lines) < CONSOLE_WIDTH - MAX_CHANGE_EACH_TIME:
                self.lines |= generateLines()

            linesList = list(self.lines)

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
    
    def begin(self):
        """runs the whole program"""
        #create and run a second thread which plays the sound
        threading.Thread(target = self.playMusic).start()
        #run the matrix generator part of the program
        self.main()

#create an object to start the program
Application()

