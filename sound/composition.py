import vlc
import time

class Notes:
    def __init__(self, notes_str, len):
        self.notes_str = notes_str
        self.len = len
        self.objNote_list = self.string_decompose(self.notes_str)

    def string_decompose(self, str):
        note_list = str.split()

        return [Note(note_str, self.len) for note_str in note_list]

class Note():
    # octave range : 3 ~ 5
    def __init__(self, note_str, len):
        self.note_str = note_str
        self.pitch_list = ["C", "D", "E", "F", "G", "A", "B"]
        self.len = len

        self.file_path = "sound\main\\"
        self.key_file = "s"
        self.file = ""

    def set_properties(self, prop_str):
        prop_list = prop_str.split()
        for prop_tuple in [tuple(note) for note in prop_list]:
            self.pitch, self.octave, self.key = prop_tuple

    def set_pitch(self, str_pitch):
        index = [idx for idx, val in enumerate(self.pitch_list) if val == str_pitch]

        return (self.pitch_list[idx] for idx in index)

    def set_file_name(self):
        if self.key_state == "Flat":
            return self.file_path + "C" + str(self.octave) + self.key_file + ".mp3"
        else:
            return self.file_path + self.pitch + str(self.octave) + self.key_name + ".mp3"

    def set_key(self, key):
        if not key:
            self.key_name = ""
            return "Natural"
        elif key == ("#" or "sharp" or "s"):
            self.key_name = self.key_file
            return "Sharp"
        elif key == ("b" or "flat" or "f"):
            self.key_name = "f"
            return "Flat"

    def play(self):
        sound = vlc.MediaPlayer(self.file)
        sound.play()
        time.sleep(self.len)

if __name__ == '__main__':
