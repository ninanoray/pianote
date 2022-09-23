from pygame import mixer
import vlc
import time

c4 = "sound\main\C4.mp3"
d4 = "sound\main\D4.mp3"
e4 = "sound\main\E4.mp3"

def play(fileList, timeLen) :
    for file in fileList:
        sound = vlc.MediaPlayer(file)
        sound.play()
    time.sleep(timeLen)

play([c4], 1)
play([e4], 1)