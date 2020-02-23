# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 01:11:40 2020

@author: josep
"""

# CodeSkulptor runs Python programs in your browser.
# Click the upper left button to run this simple demo.

# CodeSkulptor is tested to run in recent versions of
# Chrome, Firefox, and Safari.

import simplegui
import user303_ivqx1IgHh2_7 as notePackage


# Mario 
import user303_lGD8HmtyMf_2 as midiFileP0
import user303_7iDJpaPrij_1 as midiFileP1
import user303_Qisy2AlNe0_1 as midiFileP2
import user303_OWcl650jBp_1 as midiFileP3
import user303_stFd3nfU7t_1 as midiFileP4
import user303_ELYDyvXUt5_1 as midiFileP5
import user303_gJe4SMZ325_1 as midiFileP6
import user303_nB8nlrS9Tw_2 as midiFileP7

'''
# Nier Automata Copied City
import user303_KOSiuK6Vn3_0 as midiFileP0
import user303_jfkRFCeFsD_0 as midiFileP1
import user303_goylVcxbLE_0 as midiFileP2
import user303_HJsmZn1M2B_1 as midiFileP3
'''
'''
# Waltz by Shastakovich
import user303_CXe9YqKk9k_0 as midiFileP0
import user303_VXOreGhwCU_0 as midiFileP1
import user303_fYb1uSHAOM_0 as midiFileP2
import user303_Y5B62KkPFR_0 as midiFileP3
'''

'''
Note: Only handles flats!

'''

class Key:
    def __init__(self, pos, sound, width, height, color):
        self._pos = pos
        self._sound = sound
        self._width = width
        self._height = height
        self._color = color
        self._playColor = 'green'
        self._repr = sound
        
        self._curColor = self._color
    def __repr__(self):
        return self._repr
    
    def __eq__(self, other):
        return self._repr == other._repr
            
    def draw(self, canvas):
        pos, w,h = self._pos, self._width, self._height
        
        canvas.draw_polygon([pos[:], (pos[0] + w, pos[1]),(pos[0]+w,pos[1]+h),
                (pos[0],pos[1]+h)], 1, 'black', self._curColor)

        
    def playSound(self):
        print('Playing: ' + self._repr)
        self._curColor = self._playColor
        notePackage.play(self._repr)
    
    def stopSound(self):
        notePackage.pause(self._repr)
        self._curColor = self._color
        self.__rewind()
    
    def __rewind(self):
        notePackage.rewind(self._repr)
    
    def changeVolume(self, level):
        if level == 'fff':        
            self._volume = 1
        elif level == 'ff':
            self._volume = .8
        elif level == 'f':
            self._volume = .6
        elif level == 'mf':
            self._volume = .4
        elif level == 'mp':
            self._volume = .2
        elif level == 'pp':
            self._volume = .1
        else:
            raise ValueError('Ivalid Level: ' + level + '. Levels must be from [fff,ff,f,mf,mp,pp]')
            
    def isClicked(self, pos):
        return self._pos[0] < pos[0] < self._pos[0] + self._width and self._pos[1] < pos[1] < self._pos[1] + self._height
class WhiteKey(Key):
    WIDTH = 25;HEIGHT=100
    def __init__(self, pos, note, octave):
        Key.__init__(self, pos, note+str(octave), WhiteKey.WIDTH, WhiteKey.HEIGHT,
                     'white')
        
class BlackKey(Key):
    WIDTH = 15; HEIGHT=50
    def __init__(self, pos, note, octave):
        Key.__init__(self, pos, note+str(octave), BlackKey.WIDTH, BlackKey.HEIGHT,
                     'black')
    
class Octave(Key):
    OCTWIDTH = WhiteKey.WIDTH*7
    def __init__(self, pos, number):
        self._whiteKeys = [WhiteKey((pos[0]+i*WhiteKey.WIDTH, pos[1]), 'CDEFGAB'[i],
                               number) for i in range(7)]
        self._blackKeys = []#[Key((pos[0]+i*BlackKey.WIDTH, pos[1]), 'FGA'[i]+'#',
                          #     number) for i in range(8)]
        
        self._blackKeys = [BlackKey((pos[0] + WhiteKey.WIDTH*(i+1)-BlackKey.WIDTH//2, pos[1]),
                              'DEFGAB'[i]+'b', number) for i in range(6) if i != 2]
        
        self._number = number

    def draw(self, canvas):
        for key in self._whiteKeys + self._blackKeys:
            key.draw(canvas)
        
    def isClicked(self, pos):
        '''
        For now, returns repr of key that is clicked
        '''
        for key in self._blackKeys + self._whiteKeys:
            if key.isClicked(pos):
                return str(key)
        return False
    def pressKey(self, keyRepr):
        print('pressed! : ' + keyRepr + ' on octave: ' + str(self._number))
        'key in form (Note)(Sharp if Sharp)(nUmber)'
        for key in self._blackKeys + self._whiteKeys:
            if str(key) == keyRepr:
                key.playSound()

    def releaseKey(self, keyRepr):
        for key in self._whiteKeys + self._blackKeys:
            if str(key) == keyRepr:
                key.stopSound()
                
class FingerBot:
    WIDTH = BlackKey.WIDTH-2; HEIGHT=2*WIDTH
    botNum = 0
    def __init__(self, pos, keyPos):
        self._pos = list(pos)
        
        self._width = FingerBot.WIDTH
        self._height = FingerBot.HEIGHT
        
        self._keyPossibilities = ['C','Db','D','Eb','E',
                                  'F','Gb','G','Ab', 'A', 'Bb','B']
        self._curKey = self._keyPossibilities.index(keyPos[:-1])
        print(self._curKey)
        self._curOct = int(keyPos[-1])
        
        self._botNum = FingerBot.botNum
        FingerBot.botNum += 1
        
        self._pressing = False
    
    def get_num(self):
        return self._botNum
    
    def centerPos(self):
        return (self._pos[0] + FingerBot.WIDTH//2, self._pos[1] + FingerBot.HEIGHT//2)
    
    def moveRight(self):
        # Returns 0 for failed, 1 for succeeded
        if False: #If at the end of the keyboard
            return 0
        if (self._curKey == 11 or self._curKey == 4): # Should be and not at the end of the keyboard
            self._pos[0] += WhiteKey.WIDTH
        else:
            self._pos[0] += WhiteKey.WIDTH/2
            
        if self._curKey == len(self._keyPossibilities) - 1:
            self._curOct += 1
        self._curKey = (self._curKey + 1)%len(self._keyPossibilities)    
        print(self._curKey)

        return 1
    def moveLeft(self):
        # Returns 0 for failed, 1 for succeeded
        if False: #If at the end of the keyboard
            return 0
        
        if (self._curKey == 0 or self._curKey == 5): # Should be and not at the end of the keyboard
            self._pos[0] -= WhiteKey.WIDTH
        else:
            self._pos[0] -= WhiteKey.WIDTH/2
        if self._curKey == 0:
            self._curOct -= 1
        
        self._curKey = (self._curKey - 1)%len(self._keyPossibilities)        
        print(self._curKey)
        return 1
    
    def pressKey(self, octaves): # Passing the piano to press the key on lol
        self._pressing = True
        octaves[self._curOct-1].pressKey(self._keyPossibilities[self._curKey]+
                                       str(self._curOct))
        
    def releaseKey(self, octaves):
        self._pressing = False
        octaves[self._curOct-1].releaseKey(self._keyPossibilities[self._curKey]+
                                       str(self._curOct))
    
    def togglePress(self, octaves):
        if self._pressing:
            self.releaseKey(octaves)
        else:
            self.pressKey(octaves)
    
    def draw(self, canvas):
        p, w, h = self._pos, self._width, self._height
        canvas.draw_polygon([p, (p[0] + w, p[1]),(p[0] + w, p[1] + h),
                             (p[0], p[1] + h)], 1,'black', 'pink')
        
        canvas.draw_text(str(self._botNum), (p[0], p[1] + 120), 20, 'black')


# Midi files should be handled as follows:
# A parser should figure out if the command is a note on or not off
# The parser should return True of False if the note is an on or off note
# The parser should have a function that returns the note 
# The parser should have a function that returns the volume of the note
# The parser should have a hasNextLine function
# The parser should have a proceed function
# The parser should have a timing function that returns
#   The ms the command should be fired at
class MidiParser:
    NOTES = [None]*21+['A0','Bb0','B0']+[note + str(octave) 
                                   for octave in range(1, 8) 
                                   for note in ['C','Db','D',
                                                'Eb','E','F',
                                                'Gb','G','Ab',
                                                'A','Bb','B']]+[
        'C8']
    def __init__(self, midiFile):
        '''
        Constructor for Parser
        Takes in preprocessed midi file in format
            [layer, time(ms), command, channel, note, vel]
        and sets the file up for parsing
        ---
        The parser tells user if there are commands left
        in the midi file, proceeds between commands,
        and returns volume, note, timing, and c_type information
        '''
        
        assert type(midiFile) == list, "midiFile Must be list in format [Channel, time(ms), command, channel??, note, velocity]"
        self._midiFile = iter(midiFile)
        self._curCommand = next(self._midiFile)
        self._nextCommand = next(self._midiFile)
        
    def has_more_commands(self):
        return self._nextCommand[0] != 'EOF'
    
    def proceed(self):
        assert self.has_more_commands(), "Error: No remaining commands"
        self._curCommand = self._nextCommand
        self._nextCommand = next(self._midiFile)
    
    def volume(self):
        return self._curCommand[-1]
    
    def note(self):
        return MidiParser.NOTES[self._curCommand[-2]]
    
    def time(self):
        return self._curCommand[1]
    
    def c_type(self):
        return self._curCommand[2] == 'Note_on_c' and self.volume() != 0
    
# Handler for mouse click
def click(pos):
    for octave in octaves:
        clicked = octave.isClicked(pos)
        if clicked:
            octave.pressKey(clicked)

# Handler to draw on canvas
def draw(canvas):
    for oct in octaves:
        oct.draw(canvas)
    for bot in bots:
        bot.draw(canvas)
    
def right():
    for bot in bots:
        bot.moveRight()

def left():
    for bot in bots:
        bot.moveLeft()
    
def tick():
    #global elapsedNotePrecisions
    #elapsedNotePrecisions+=1
    global time_ms, ticktime
    timingCommands()
    time_ms += timestep

def timingCommands():
    global time_ms, ticktime, timestep, midiParser#elapsedNotePrecisions, octaves
    # Volume currently unsupported
    while time_ms == midiParser.time()//(timestep)*(timestep):
        octave = octaves[int(midiParser.note()[-1]) - 1]
        if midiParser.c_type():
            octave.pressKey(midiParser.note())
        else:
            octave.releaseKey(midiParser.note())
        if midiParser.has_more_commands():
            midiParser.proceed()
        else:
            try:
                midiParser = next(midiParsers)
            except:
                timer.stop()
                
octStart = 10
octaves = [Octave((octStart + Octave.OCTWIDTH*(i-1), octStart), i) for i in range(1, 9)]

bots = []
#					Position on the octave we're starting onq		 Vert pos on oct					
bot0 = FingerBot([octStart + Octave.OCTWIDTH*(5-1) + WhiteKey.WIDTH//2 - FingerBot.WIDTH//2, octStart],'C5') 
bot1 = FingerBot([octStart + Octave.OCTWIDTH*(5-1) + 5*WhiteKey.WIDTH//2 - FingerBot.WIDTH//2, octStart],'E5') 
bot2 = FingerBot([octStart + Octave.OCTWIDTH*(5-1) + 9*WhiteKey.WIDTH//2 - FingerBot.WIDTH//2, octStart],'G5') 
bots += [bot0, bot1, bot2]

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", 1200, 200)
ticktime = 13
timestep = 30

miliInAMin = 60000
bpm = 150
handledNotePrecision = 8 # = notes up to eighth notes are handled by simulator
timer = simplegui.create_timer(ticktime, tick)#miliInAMin/(bpm*handledNotePrecision), tick)
elapsedNotePrecisions = 0

time_ms = 0

midiParsers = iter((MidiParser(midiFileP0.midiFile),
MidiParser(midiFileP1.midiFile),
MidiParser(midiFileP2.midiFile),
MidiParser(midiFileP3.midiFile),))
#MidiParser(midiFileP4.midiFile),
#MidiParser(midiFileP5.midiFile),
#MidiParser(midiFileP6.midiFile),
#MidiParser(midiFileP7.midiFile)))

midiParser = next(midiParsers)

frame.add_button('left', left)
frame.add_button('right', right)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)
frame.set_canvas_background('orange')

# Start the frame animation
frame.start()
timer.start()

print(midiParser.has_more_commands())
print(midiParser.c_type())
print(midiParser.note())      
print(midiParser.time())
      