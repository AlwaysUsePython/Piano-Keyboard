import pygame
import numpy as np
import time

notesList = ['C0', 'C#0', 'D0', 'D#0', 'E0', 'F0', 'F#0', 'G0', 'G#0', 'A0', 'A#0', 'B0', 'C1', 'C#1', 'D1', 'D#1', 'E1', 'F1', 'F#1', 'G1', 'G#1', 'A1', 'A#1', 'B1', 'C2', 'C#2', 'D2', 'D#2', 'E2', 'F2', 'F#2', 'G2', 'G#2', 'A2', 'A#2', 'B2', 'C3', 'C#3', 'D3', 'D#3', 'E3', 'F3', 'F#3', 'G3', 'G#3', 'A3', 'A#3', 'B3', 'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4', 'C5', 'C#5', 'D5', 'D#5', 'E5', 'F5', 'F#5', 'G5', 'G#5', 'A5', 'A#5', 'B5', 'C6', 'C#6', 'D6', 'D#6', 'E6', 'F6', 'F#6', 'G6', 'G#6', 'A6', 'A#6', 'B6', 'C7', 'C#7', 'D7', 'D#7', 'E7', 'F7', 'F#7', 'G7', 'G#7', 'A7', 'A#7', 'B7', 'C8', 'C#8', 'D8', 'D#8', 'E8', 'F8', 'F#8', 'G8', 'G#8', 'A8', 'A#8', "B8", "C9"]


pygame.init()
pygame.mixer.init()

pygame.mixer.set_num_channels(50)

played = False

screen = pygame.display.set_mode((1000, 600))

def playNote(frequency, duration =15, samplingRate = 44100):
    frames = int(duration * samplingRate)

    # Divide the duration into frames and make an array with the appropriate cos value in each
    waveTable = np.cos(2 * np.pi * frequency * np.linspace(0, duration, frames))

    # transform it into a 16 bit wave file that pygame can mix
    sound = np.asarray([32767 * waveTable, 32767 * waveTable]).T.astype(np.int16)
    sound = pygame.sndarray.make_sound(sound.copy())

    return sound

firstFreq = 16.3516

notes = {}
keylist = 'awsedftgyhuj'
modifiers = [pygame.K_LEFT, pygame.K_RIGHT]
octave = 4


while True:
    if not played:
        for i in range(len(notesList)-1):
            mod = int(i/12)
            key = keylist[i-mod*12]+str(mod)
            print(notesList[i])
            freq = firstFreq * 2 ** (((1/12)) * i)
            sample = playNote(freq)
            notes[key] = [sample, notesList[i], freq]
            notes[key][0].set_volume(0.33)
            #notes[key][0].play()
            #notes[key][0].fadeout(1)
            #pygame.time.wait(1)
            if key[0] == "a":
                freq = firstFreq * 2 ** (((1 / 12)) * (i+12))
                sample = playNote(freq)
                key = "k" + key[1]
                notes[key] = [sample, notesList[i+12], freq]
                notes[key][0].set_volume(0.33)

        played = True
        keylist = 'awsedftgyhujk'
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            else:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    if event.key == pygame.K_LEFT:
                        octave -= 1
                    elif event.key == pygame.K_RIGHT:
                        octave += 1

                elif str(event.unicode) in keylist:
                    key = str(event.unicode)
                    try:
                        print(notes[key + str(octave)][1])
                        notes[key + str(octave)][0].play()
                    except:
                        print("not in dictionary")
        if event.type == pygame.KEYUP and event.key not in modifiers:
            try:
                key = str(event.unicode)+str(octave)
                notes[key][0].fadeout(100)
            except:
                break



    screen.fill((0, 0, 0))
    pygame.display.update()


pygame.mixer.quit()
