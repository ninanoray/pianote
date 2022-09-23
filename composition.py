import vlc
import time

class Pitch:
    def __int__(self, name, len):
        self.name = name
        self.len = len
        self.file = ""

    def play(self):
        sound = vlc.MediaPlayer(self.file)
        sound.play()
        time.sleep(self.len)

class C(Pitch):
    def __int__(self, name, len):
        super().__int__(name, len)
        self.name = name
        self.c4 = "sound\main\C4.mp3"
        self.c5 = "sound\main\C5.mp3"
        self.file = self.match_file()

    def match_file(self):
        if self.name == "c4":
            return self.c4
        elif self.name == "c5":
            return self.c5


if __name__ == '__main__':
    c4 = Pitch('c4', 1)

