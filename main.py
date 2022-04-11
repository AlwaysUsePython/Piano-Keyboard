"""
IDEAS

 - chord database
 build chord functions using half steps
 manually overriding 1-9
"""
import pygame
import numpy as np
import time
import math

notesList = ['C0', 'C#0', 'D0', 'D#0', 'E0', 'F0', 'F#0', 'G0', 'G#0', 'A0', 'A#0', 'B0', 'C1', 'C#1', 'D1', 'D#1', 'E1', 'F1', 'F#1', 'G1', 'G#1', 'A1', 'A#1', 'B1', 'C2', 'C#2', 'D2', 'D#2', 'E2', 'F2', 'F#2', 'G2', 'G#2', 'A2', 'A#2', 'B2', 'C3', 'C#3', 'D3', 'D#3', 'E3', 'F3', 'F#3', 'G3', 'G#3', 'A3', 'A#3', 'B3', 'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4', 'C5', 'C#5', 'D5', 'D#5', 'E5', 'F5', 'F#5', 'G5', 'G#5', 'A5', 'A#5', 'B5', 'C6', 'C#6', 'D6', 'D#6', 'E6', 'F6', 'F#6', 'G6', 'G#6', 'A6', 'A#6', 'B6', 'C7', 'C#7', 'D7', 'D#7', 'E7', 'F7', 'F#7', 'G7', 'G#7', 'A7', 'A#7', 'B7', 'C8', 'C#8', 'D8', 'D#8', 'E8', 'F8', 'F#8', 'G8', 'G#8', 'A8', 'A#8', "B8", "C9"]


pygame.init()
pygame.mixer.init()

pygame.mixer.set_num_channels(50)

played = False

screen = pygame.display.set_mode((1000, 600))

def makeNote(frequency, duration =15, samplingRate = 44100):
    frames = int(duration * samplingRate)

    # Divide the duration into frames and make an array with the appropriate cos value in each
    waveTable = np.sin(2 * np.pi * frequency * np.linspace(0, duration, frames))
    waveTable = waveTable + np.sin(4 * np.pi * frequency * np.linspace(0, duration, frames))
    waveTable = waveTable + np.sin(6 * np.pi * frequency * np.linspace(0, duration, frames))
    """for i in range(len(waveTable)):
        waveTable[i] /= 2+(i**(1/2))/5"""
    waveTable /= 9

    #waveTable = waveTable + np.sin(8 * np.pi * frequency * np.linspace(0, duration, frames))/8
    #waveTable = waveTable + np.sin(10 * np.pi * frequency * np.linspace(0, duration, frames))/16


    # transform it into a 16 bit wave file that pygame can mix
    sound = np.asarray([32767 * waveTable, 32767 * waveTable]).T.astype(np.int16)
    sound = pygame.sndarray.make_sound(sound.copy())

    return sound

def playNote(note):
    notes[note][0].play()
    notes[note][3] = 1
    if note[0] == "k":
        notes["a" + str(int(note[1])+1)][3] = 1

def releaseNote(note):
    notes[note][0].fadeout(100)
    notes[note][3] = 0
    if note[0] == "k":
        notes["a" + str(int(note[1])+1)][3] = 0

print(len(notesList))

firstFreq = 16.3516

notes = {}


def drawKeyboard(notes):
    whiteKeys = 0
    octave = 0
    keylist = "awsedftgyhuj"
    for key in range(len(notesList)):
        note = keylist[key % 12] + str(octave)
        otherNote = ""
        if note[0] == "a":
            otherNote = "k" + note[1]
        if notesList[key][1] in "012345678":
            pygame.draw.rect(screen, (0, 0, 0),
                         pygame.Rect(whiteKeys * 15.87, 440, 20, 150))
            try:
                if notes[note][3] == 0:
                    pygame.draw.rect(screen, (255, 255, 255),
                                 pygame.Rect(whiteKeys * 15.87 + 1, 441, 13.87, 148))
                else:
                    #print(notes[note][1])
                    pygame.draw.rect(screen, (0, 255, 0),
                                     pygame.Rect(whiteKeys * 15.87 + 1, 441, 13.87, 148))

            except:
                pygame.draw.rect(screen, (255, 255, 255),
                                 pygame.Rect(whiteKeys * 15.87 + 1, 441, 13.87, 148))

            if otherNote != "":
                """try:
                    print(notes[otherNote][3])
                    print("k4 -", notes["k4"][3])
                    print()
                except:
                    pass"""
                    #print(otherNote)
                try:
                    if notes[otherNote][3] != 0:
                        pygame.draw.rect(screen, (0, 255, 0),
                                         pygame.Rect((whiteKeys+8) * 15.87 + 1, 441, 13.87, 148))
                except:
                    pass

            whiteKeys += 1
            if whiteKeys % 7 == 0:
                octave += 1
    whiteKeys = -1
    octave = 0
    for key in range(len(notesList)):
        if notesList[key][1] in "012345678":
            whiteKeys += 1
            if whiteKeys % 7 == 0:
                octave += 1
        else:
            note = keylist[key % 12] + str(octave-1)
            """try:
                print(notes[note][1])
            except:
                print(note)"""
            try:
                if notes[note][3] == 0:
                    pygame.draw.rect(screen, (0, 0, 0),
                             pygame.Rect(whiteKeys * 15.87 + 10.58, 440, 10.58, 100))
                else:
                    #print(notes[note][1])
                    pygame.draw.rect(screen, (0, 255, 0),
                             pygame.Rect(whiteKeys * 15.87 + 10.58, 440, 10.58, 100))
            except:
                pygame.draw.rect(screen, (0, 0, 0),
                                 pygame.Rect(whiteKeys * 15.87 + 10.58, 440, 10.58, 100))
    #ready = input()
def playChord(chordArr):
    for note in range(len(chordArr)-2):
        #notes[note][0].play()
        playNote(chordArr[note])
def releaseChord(chordArr):
    for note in range(len(chordArr)-2):
        #notes[note][0].fadeout(100)
        releaseNote(chordArr[note])

font = pygame.font.Font('freesansbold.ttf', 50)
font2 = pygame.font.Font('freesansbold.ttf', 30)

def drawChordList(chordList, octaveNum):
    coords = [50, 100]
    for key in [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]:
        text = font.render(str(key), True, (0, 0, 255))
        textRect = text.get_rect()
        textRect.center = (coords[0], coords[1])
        #print(chordList[str(key) + str(octaveNum)])

        if chordList[str(key) + str(octaveNum)][-2] == 0:
            text2 = font2.render(chordList[str(key)+str(octaveNum)][-1], True, (255, 255, 255))
        else:
            text2 = font2.render(chordList[str(key)+str(octaveNum)][-1], True, (0, 255, 0))
        text2Rect = text2.get_rect()
        text2Rect.center = (coords[0], coords[1] + 100)
        coords[0] += 100
        screen.blit(text, textRect)
        screen.blit(text2, text2Rect)

def drawNums():
    coords = [50, 300]
    for text in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
        write = font.render(text, True, (255, 255, 255))
        writeRect = write.get_rect()
        writeRect.center = (coords[0], coords[1])
        coords[0] += 100
        screen.blit(write, writeRect)

def drawRoots():
    coords = [1000/14, 200]
    for text in ["C", "D", "E", "F", "G", "A", "B", "C#", "D#", "F#", "G#", "A#"]:
        write = font.render(text, True, (255, 255, 255))
        writeRect = write.get_rect()
        writeRect.center = (coords[0], coords[1])
        coords[0] += 1000/7
        screen.blit(write, writeRect)
        if coords[0] > 1000:
            coords[0] = 1000/14 + 1000/7
            coords[1] = 400

def drawTypes():
    types = ["M", "m", "7", "d", "m7", "M7"]
    length = len(types)
    coords = [1000 / (2*length), 300]
    for text in types:
        write = font.render(text, True, (255, 255, 255))
        writeRect = write.get_rect()
        writeRect.center = (coords[0], coords[1])
        coords[0] += 1000 / length
        screen.blit(write, writeRect)

def buildChord(root, tonality):
    upperRoot = root
    if len(root) > 1:
        root = chr(ord(root[0]) - ord("A") + ord("a"))
        root += "#"
    else:
        root = chr(ord(root[0]) - ord("A") + ord("a"))
    roots = ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]
    notes = ["a", "w", "s", "e", "d", "f", "t", "g", "y", "h", "u", "j"]
    noteIndex = roots.index(root)
    chord = [notes[noteIndex]]
    if tonality == "M":
        chord.append(notes[(noteIndex + 4)%12])
        chord.append(notes[(noteIndex + 7)%12])
    elif tonality == "m":
        chord.append(notes[(noteIndex + 3)%12])
        chord.append(notes[(noteIndex + 7)%12])
    elif tonality == "7":
        chord.append(notes[(noteIndex + 4)%12])
        chord.append(notes[(noteIndex + 7)%12])
        chord.append(notes[(noteIndex + 10)%12])
    elif tonality == "d":
        chord.append(notes[(noteIndex + 3)%12])
        chord.append(notes[(noteIndex + 6)%12])
    elif tonality == "m7":
        chord.append(notes[(noteIndex + 3)%12])
        chord.append(notes[(noteIndex + 7)%12])
        chord.append(notes[(noteIndex + 10)%12])
    elif tonality == "M7":
        chord.append(notes[(noteIndex + 4) % 12])
        chord.append(notes[(noteIndex + 7) % 12])
        chord.append(notes[(noteIndex + 11) % 12])

    chord.append(0)
    chord.append(upperRoot + tonality)
    print(upperRoot + tonality)
    return chord



def setChordList(chordList):
    roots = ["C", "D", "E", "F", "G", "A", "B", "C#", "D#", "F#", "G#", "A#"]
    positions = []
    coords = [1000/14, 200]
    for item in roots:
        positions.append((coords[0], coords[1]))
        coords[0] += 1000/7
        if coords[0] > 1000:
            coords[0] = 1000/14 + 1000/7
            coords[1] = 400

    types = ["M", "m", "7", "d", "m7", "M7"]
    typePositions = []
    coords = [1000 / (2*len(types)), 300]
    for item in roots:
        typePositions.append((coords[0], coords[1]))
        coords[0] += 1000 / len(types)

    stage = 0
    selected = False
    while not selected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return chordList
                else:
                    if stage == 0:
                        try:
                            key = str(event.unicode)
                            if key in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
                                stage += 1
                                keyToEdit = key
                                print(keyToEdit)
                        except:
                            pass
            if event.type == pygame.MOUSEBUTTONUP:
                if stage == 1:
                    pos = pygame.mouse.get_pos()
                    for i in range(len(positions)):
                        if (math.sqrt((pos[0] - positions[i][0])**2 + (pos[1] - positions[i][1])**2)) < 50:
                            root = roots[i]
                            print(root)
                            stage += 1
                if stage == 2:
                    pos = pygame.mouse.get_pos()
                    for i in range(len(typePositions)):
                        if (math.sqrt((pos[0] - typePositions[i][0]) ** 2 + (pos[1] - typePositions[i][1]) ** 2)) < 50:
                            tonality = types[i]
                            print(tonality)
                            stage += 1
                            selected = True

        screen.fill((0, 0, 0))
        if stage == 0:
            drawNums()
        if stage == 1:
            drawRoots()
        if stage == 2:
            drawTypes()
        pygame.display.update()

    chord = buildChord(root, tonality)

    for i in range(8):
        newChord = []
        for j in range(len(chord)-2):
            newChord.append(chord[j] + str(i))
        newChord.append(chord[-2])
        newChord.append(chord[-1])
        chordList[str(keyToEdit)+str(i)] = newChord
        print(str(keyToEdit)+str(i))
        print(chordList[str(keyToEdit)+str(i)])

    return chordList



def createKeyboard():

    #DEFAULT CHORD LIST
    chordList = {}
    for num in range(8):
        chordList["1" + str(num)] = ["a" + str(num), "d" + str(num), "g" + str(num), 0, "CM"]
        chordList["2" + str(num)] = ["s" + str(num), "f" + str(num), "h" + str(num), 0, "Dm"]
        chordList["3" + str(num)] = ["d" + str(num), "g" + str(num), "j" + str(num), 0, "Em"]
        chordList["4" + str(num)] = ["a" + str(num), "f" + str(num), "h" + str(num), 0, "FM"]
        chordList["5" + str(num)] = ["s" + str(num), "g" + str(num), "j" + str(num), 0, "GM"]
        chordList["6" + str(num)] = ["a" + str(num), "d" + str(num), "h" + str(num), 0, "Am"]
        chordList["7" + str(num)] = ["a" + str(num), "d" + str(num), "g" + str(num), "u" + str(num), 0, "C7"]
        chordList["8" + str(num)] = ["d" + str(num), "g" + str(num), "k" + str(num), 0, "C1"]
        chordList["9" + str(num)] = ["s" + str(num), "f" + str(num), "g" + str(num), "j" + str(num), 0, "G7"]
        chordList["0" + str(num)] = ["a" + str(num), "e" + str(num), "g" + str(num), "u" + str(num), 0, "Cm7"]

    chordKeys = "1234567890"
    keylist = 'awsedftgyhuj'
    modifiers = [pygame.K_LEFT, pygame.K_RIGHT]
    octave = 4
    chordOctave = 4
    played = False
    while True:
        #played = True
        if not played:
            for i in range(36, len(notesList)-1-47):
                mod = int(i/12)
                key = keylist[i-mod*12]+str(mod)
                print(notesList[i])
                freq = firstFreq * 2 ** (((1/12)) * i)
                sample = makeNote(freq)
                notes[key] = [sample, notesList[i], freq, 0]
                notes[key][0].set_volume(0.33)
                notes[key][0].play()
                notes[key][0].fadeout(1000)
                #notes[key][0].play()
                #notes[key][0].fadeout(1)
                #pygame.time.wait(1)
                if key[0] == "a":
                    freq = firstFreq * 2 ** (((1 / 12)) * (i+12))
                    sample = makeNote(freq)
                    key = "k" + key[1]
                    notes[key] = [sample, notesList[i+12], freq, 0]
                    notes[key][0].set_volume(0.33)

            played = True
            keylist = 'awsedftgyhujk'
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_RETURN:
                    print(chordList)
                    chordList = setChordList(chordList)
                    print(chordList)
                else:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        if event.key == pygame.K_LEFT:
                            octave -= 1
                        elif event.key == pygame.K_RIGHT:
                            octave += 1

                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_TAB:
                        if event.key == pygame.K_BACKSPACE:
                            chordOctave -= 1
                        elif event.key == pygame.K_TAB:
                            chordOctave += 1
                        print(chordOctave)

                    elif str(event.unicode) in keylist:
                        key = str(event.unicode)
                        try:
                            print(notes[key + str(octave)][1])
                            #notes[key + str(octave)][0].play()
                            playNote(key + str(octave))
                        except:
                            print("not in dictionary")

                    elif str(event.unicode) in chordKeys:
                        key = str(event.unicode) + str(chordOctave)
                        print(key)
                        try:
                            playChord(chordList[key])
                            chordList[key][-2] = 1
                            print(chordList[key])
                        except:
                            print("not a chord")
            if event.type == pygame.KEYUP and event.key not in modifiers:
                try:
                    key = str(event.unicode)+str(octave)
                    #notes[key][0].fadeout(100)
                    releaseNote(key)
                except:
                    pass
                try:
                    key = str(event.unicode)+ str(chordOctave)
                    print("releasing")
                    releaseChord(chordList[key])
                    chordList[key][-2] = 0
                except:
                    pass


        screen.fill((0, 0, 0))
        drawKeyboard(notes)
        drawChordList(chordList, chordOctave)
        pygame.display.update()


createKeyboard()
pygame.mixer.quit()
