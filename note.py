import pygame
import piano_lists as pl

class Note: # 음표
    WIDTH = 32
    WIDTH2 = 46
    HEIGHT = 60

    # 음표 이미지
    IMG_note_2 = pygame.image.load("images/note_half.png")
    IMG_note_2 = pygame.transform.scale(IMG_note_2, (WIDTH, HEIGHT))
    IMG_note_2up = pygame.image.load("images/note_half_up.png")
    IMG_note_2up = pygame.transform.scale(IMG_note_2up, (WIDTH, HEIGHT))
    IMG_note_4 = pygame.image.load("images/note_quarter.png")
    IMG_note_4 = pygame.transform.scale(IMG_note_4, (WIDTH, HEIGHT))
    IMG_note_4up = pygame.image.load("images/note_quarter_up.png")
    IMG_note_4up = pygame.transform.scale(IMG_note_4up, (WIDTH, HEIGHT))
    IMG_note_8 = pygame.image.load("images/note_eighth.png")
    IMG_note_8 = pygame.transform.scale(IMG_note_8, (WIDTH2, HEIGHT))
    IMG_note_8up = pygame.image.load("images/note_eighth_up.png")
    IMG_note_8up = pygame.transform.scale(IMG_note_8up, (WIDTH, HEIGHT))
    IMG_note_16 = pygame.image.load("images/note_sixteenth.png")
    IMG_note_16 = pygame.transform.scale(IMG_note_16, (WIDTH2, HEIGHT))
    IMG_note_16up = pygame.image.load("images/note_sixteenth_up.png")
    IMG_note_16up = pygame.transform.scale(IMG_note_16up, (WIDTH, HEIGHT))
    IMG_SHARP = pygame.image.load("images/sharp.png")
    IMG_SHARP = pygame.transform.scale(IMG_SHARP, (37, 14 * 3))
    IMG_FLAT = pygame.image.load("images/flat.png")
    IMG_FLAT = pygame.transform.scale(IMG_FLAT, (19, 14 * 3))

    def __init__(self, screen, white_sounds, black_sounds, pitch, note=4):
        self.screen = screen
        self.WHITE_SOUNDS = white_sounds
        self.BLACK_SOUNDS = black_sounds

        self.set_pitch(pitch)
        self.note = note
        self.set_image()
        self.set_sound()

    def set_pitch(self, name):
        if 's' in name:
            self.pitch = name.replace('s', '#')
        else:
            self.pitch = name

    def set_image(self):
        index_B4 = pl.piano_pitches.index("B4") # 4옥타브 시
        index_pitch = pl.piano_pitches.index(self.pitch)

        # 4옥타브 시를 넘어서 음표 꼬리를 밑으로 내리는 가
        if index_pitch < index_B4:
            self.is_down = True
            if self.note == 2:
                self.image = self.IMG_note_2
            elif self.note == 4:
                self.image = self.IMG_note_4
            elif self.note == 8:
                self.image = self.IMG_note_8
            elif self.note == 16:
                self.image = self.IMG_note_16
        else:
            self.is_down = False
            if self.note == 2:
                self.image = self.IMG_note_2up
            elif self.note == 4:
                self.image = self.IMG_note_4up
            elif self.note == 8:
                self.image = self.IMG_note_8up
            elif self.note == 16:
                self.image = self.IMG_note_16up

    def get_pitch(self):
        return self.pitch

    def set_note(self, th):
        self.note = th
    def get_note(self):
        return self.note

    def set_sound(self):
        if '#' not in self.pitch:
            index_sound = pl.white_pitches.index(self.pitch)
            self.sound = self.WHITE_SOUNDS[index_sound]
        else:
            pitch = self.pitch.replace('#', 's')
            index_sound = pl.black_pitches.index(pitch)
            self.sound = self.BLACK_SOUNDS[index_sound]
    def get_sound(self):
        return self.sound

    #음표 그리기
    def draw_note(self, step):
        Y_C3 = 166  # 오선지 C4(도) 선 위치
        Y_B4 = 212  # 오선지 B4(시) 선 위치
        START_MARGIN = 42 + 22 + 10 # 높은음자리표w + 박자표w + a
        if step > 0:
            self.X = self.WIDTH + step
        else:
            self.X = START_MARGIN

        pitch_name = ""
        if len(self.pitch):
            pitch_name = self.pitch[0:2]
        index_C4 = pl.white_pitches.index("C4")
        index_pitch = pl.white_pitches.index(pitch_name)
        level = index_pitch - index_C4

        self.rect = self.image.get_rect()

        if self.is_down:
            self.rect.y = Y_C3 - level * 7 # 7 = 오선지 interval/2
        else:
            self.rect.y = Y_B4 - level * 7
        if '#' in self.pitch: # 반음이면 '#' 붙임
            rect = self.IMG_SHARP.get_rect()
            self.X += 14
            rect.x = self.X - self.WIDTH + 4
            rect.y = self.rect.y + self.HEIGHT/2 + 2
            self.screen.blit(self.IMG_SHARP, rect)
        self.rect.x = self.X
        self.screen.blit(self.image, self.rect)

        return self.X

    def set_X(self, x):
        self.X = x