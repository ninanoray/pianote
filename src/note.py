import pygame
import piano_lists as pl

# 소리 파일 : main.py 에서 받는다
WHITE_SOUNDS = []
BLACK_SOUNDS = []

# 오선지 요소(오선지 5줄)
INTERVAL_LINE = 14 # 선 사이 간격
Y_SHEET = 120 # 오선지 Y 좌표
H_SHEET = INTERVAL_LINE * (4 + 2 + 5) # 내부 간격: 4칸, 외부 간격 위: 2칸, 외부 간격 아래: 5칸
W_CLEF = 42 # 높은 음자리표 width
W_METER = 22 # 박자표 width

# 오선지 그리기
def draw_music_sheet(screen, width_gui):
    IMG_TREBLE_CLEF = pygame.image.load("../images/treble_clef.png")
    IMG_TREBLE_CLEF = pygame.transform.scale(IMG_TREBLE_CLEF, (W_CLEF, INTERVAL_LINE * 6))
    IMG_FOUR_FOURTH = pygame.image.load("../images/four_fourth.png")
    IMG_FOUR_FOURTH = pygame.transform.scale(IMG_FOUR_FOURTH, (W_METER, INTERVAL_LINE * 4))

    # 오선지 배경 그리기
    pygame.draw.rect(screen, 'white', [0, Y_SHEET, width_gui, H_SHEET + INTERVAL_LINE]) # INTERVAL_LINE 그냥 추가 여백
    # 오선지 선 그리기
    for i in range(0, 5):
        pygame.draw.line(screen, 'black', [0, Y_SHEET + (i + 2) * INTERVAL_LINE], # 외부 간격 위: 2칸
                         [width_gui, Y_SHEET + (i + 2) * INTERVAL_LINE], 2)

    screen.blit(IMG_TREBLE_CLEF, (0, Y_SHEET + INTERVAL_LINE))
    screen.blit(IMG_FOUR_FOURTH, (W_CLEF, Y_SHEET + INTERVAL_LINE * 2))

class Note: # 음표
    WIDTH = 32 # 음표 이미지 넓이
    WIDTH2 = 46 # 꼬리올린 8분음표, 꼬리올린 16분음표 전용
    HEIGHT = 60 # 음표 이미지 높이

    # 음표 이미지
    IMG_note_2 = pygame.image.load("../images/note_half.png")
    IMG_note_2 = pygame.transform.scale(IMG_note_2, (WIDTH, HEIGHT))
    IMG_note_2up = pygame.image.load("../images/note_half_up.png")
    IMG_note_2up = pygame.transform.scale(IMG_note_2up, (WIDTH, HEIGHT))
    IMG_note_4 = pygame.image.load("../images/note_quarter.png")
    IMG_note_4 = pygame.transform.scale(IMG_note_4, (WIDTH, HEIGHT))
    IMG_note_4up = pygame.image.load("../images/note_quarter_up.png")
    IMG_note_4up = pygame.transform.scale(IMG_note_4up, (WIDTH, HEIGHT))
    IMG_note_8 = pygame.image.load("../images/note_eighth.png")
    IMG_note_8 = pygame.transform.scale(IMG_note_8, (WIDTH2, HEIGHT))
    IMG_note_8up = pygame.image.load("../images/note_eighth_up.png")
    IMG_note_8up = pygame.transform.scale(IMG_note_8up, (WIDTH, HEIGHT))
    IMG_note_16 = pygame.image.load("../images/note_sixteenth.png")
    IMG_note_16 = pygame.transform.scale(IMG_note_16, (WIDTH2, HEIGHT))
    IMG_note_16up = pygame.image.load("../images/note_sixteenth_up.png")
    IMG_note_16up = pygame.transform.scale(IMG_note_16up, (WIDTH, HEIGHT))
    IMG_SHARP = pygame.image.load("../images/sharp.png")
    IMG_SHARP = pygame.transform.scale(IMG_SHARP, (37, INTERVAL_LINE * 3))
    IMG_FLAT = pygame.image.load("../images/flat.png")
    IMG_FLAT = pygame.transform.scale(IMG_FLAT, (19, INTERVAL_LINE * 3))

    def __init__(self, screen, pitch, note = 4):
        self.screen = screen

        self.set_pitch(pitch) # 음(CDEFGAB)
        self.note = note # 2, 4, 8, 16분 음표
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
            if self.note == 2: # 2분음표
                self.image = self.IMG_note_2
            elif self.note == 4: # 4분음표
                self.image = self.IMG_note_4
            elif self.note == 8: # 8분음표
                self.image = self.IMG_note_8
            elif self.note == 16: # 16분음표
                self.image = self.IMG_note_16
        else:
            self.is_down = False
            if self.note == 2: # 2분음표
                self.image = self.IMG_note_2up
            elif self.note == 4: # 4분음표
                self.image = self.IMG_note_4up
            elif self.note == 8: # 8분음표
                self.image = self.IMG_note_8up
            elif self.note == 16: # 16분음표
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
            self.sound = WHITE_SOUNDS[index_sound]
        else:
            pitch = self.pitch.replace('#', 's')
            index_sound = pl.black_pitches.index(pitch)
            self.sound = BLACK_SOUNDS[index_sound]
    def get_sound(self):
        return self.sound

    #음표 그리기
    def draw_note(self, step):
        Y_C3 = Y_SHEET + INTERVAL_LINE*3 + 4  # 오선지 C4(도) 선 위치(음표 꼬리 올림)
        Y_B4 = Y_SHEET + INTERVAL_LINE*2 + self.HEIGHT + 4  # 오선지 B4(시) 선 위치(음표 꼬리 내림)
        START_MARGIN = W_CLEF + W_METER + 10 # 높은음자리표w + 박자표w + a

        if step > 0:
            self.X = self.WIDTH + step
        else:
            self.X = START_MARGIN

        pitch_name = ""
        if len(self.pitch):
            pitch_name = self.pitch[0] + self.pitch[-1]
        index_C4 = pl.white_pitches.index("C4")
        index_pitch = pl.white_pitches.index(pitch_name)
        level = index_pitch - index_C4

        self.rect = self.image.get_rect()

        # 음표 꼬리 설정
        if self.is_down:
            self.rect.y = Y_C3 - level * INTERVAL_LINE/2 # 오선지 interval
        else:
            self.rect.y = Y_B4 - level * INTERVAL_LINE/2

        # 반음에 '#' 붙임
        if '#' in self.pitch:
            rect = self.IMG_SHARP.get_rect()
            self.X += 14
            rect.x = self.X - self.WIDTH + 4
            if self.is_down:
                rect.y = self.rect.y + self.HEIGHT/2 + 2
            else:
                rect.y = self.rect.y - INTERVAL_LINE
            self.screen.blit(self.IMG_SHARP, rect)

        self.rect.x = self.X
        self.screen.blit(self.image, self.rect)

        return self.X

    def set_X(self, x):
        self.X = x