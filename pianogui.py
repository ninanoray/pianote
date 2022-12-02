import pygame
import piano_lists as pl
from pygame import mixer

class PianoGUI:
    MIN_OCT = 3 # 최소 옥타브

    def __init__(self, screen, width, height,
                 white_sounds, black_sounds, small_font, real_small_font):
        self.screen = screen

        self.WIDTH = width
        self.HEIGHT = height

        self.left_oct = self.MIN_OCT + 1
        self.right_oct = self.MIN_OCT + 2

        self.white_sounds = white_sounds
        self.black_sounds = black_sounds

        self.left_hand = pl.left_hand
        self.right_hand = pl.right_hand
        self.white_labels = pl.white_pitches # 백건
        self.black_labels = pl.black_labels # 흑건

        self.small_font = small_font
        self.real_small_font = real_small_font

        self.update_keys_set()

    def set_left_oct(self, oct):
        self.left_oct = oct
    def get_left_oct(self):
        return self.left_oct

    def set_right_oct(self, oct):
        self.right_oct = oct
    def get_right_oct(self):
        return self.right_oct

    def update_keys_set(self): # 키설정 업데이트
        self.left_dict = {'Z': f'C{self.left_oct}',
                          'S': f'C{self.left_oct}s',
                          'X': f'D{self.left_oct}',
                          'D': f'D{self.left_oct}s',
                          'C': f'E{self.left_oct}',
                          'V': f'F{self.left_oct}',
                          'G': f'F{self.left_oct}s',
                          'B': f'G{self.left_oct}',
                          'H': f'G{self.left_oct}s',
                          'N': f'A{self.left_oct}',
                          'J': f'A{self.left_oct}s',
                          'M': f'B{self.left_oct}'}
        self.right_dict = {'W': f'F{self.right_oct - 1}',
                           '3': f'F{self.right_oct - 1}s',
                           'E': f'G{self.right_oct - 1}',
                           '4': f'G{self.right_oct - 1}s',
                           'R': f'A{self.right_oct - 1}',
                           '5': f'A{self.right_oct - 1}s',
                           'T': f'B{self.right_oct - 1}',
                           'Y': f'C{self.right_oct}',
                           '7': f'C{self.right_oct}s',
                           'U': f'D{self.right_oct}',
                           '8': f'D{self.right_oct}s',
                           'I': f'E{self.right_oct}',
                           'O': f'F{self.right_oct}',
                           '0': f'F{self.right_oct}s',
                           'P': f'G{self.right_oct}',
                           '-': f'G{self.right_oct}s',
                           '[': f'A{self.right_oct}',
                           '=': f'A{self.right_oct}s',
                           ']': f'B{self.right_oct}'}

    # 피아노 모양 생성
    def draw_piano(self, whites, blacks):
        white_w = 35
        white_h = 200
        black_w = 24
        black_h = 100

        # 백건
        white_rects = []
        for i in range(len(self.white_labels)):
            rect = pygame.draw.rect(self.screen, 'white',
                                    [i*white_w, self.HEIGHT-white_h, white_w, white_h], 0, 2)
            white_rects.append(rect)
            pygame.draw.rect(self.screen, 'black',
                             [i*white_w, self.HEIGHT-white_h, white_w, white_h], 2, 2)
            # 노트 이름 텍스트
            key_label = self.small_font.render(self.white_labels[i], True, 'black')
            self.screen.blit(key_label, (i * white_w + 8, self.HEIGHT - 20))
        # 키 누름 표시
        for i in range(len(whites)):
            if whites[i][1] > 0:
                j = whites[i][0]
                pygame.draw.rect(self.screen, 'green',
                                 [j*white_w, self.HEIGHT-white_h, white_w, white_h], 2, 2)
                whites[i][1] -= 1

        # 흑건
        LINE_CDE = 2 # 도레미 흑건
        LINE_FGAB = 3 # 파솔라시 흑건
        skip_count = 0
        last_skip = LINE_FGAB
        skip_track = 0
        black_rects = []
        for i in range(len(self.black_labels)):
            rect = pygame.draw.rect(self.screen, 'black',
                                    [black_w + (i*white_w) + (skip_count*white_w),
                                     self.HEIGHT-white_h, black_w, black_h], 0, 2)
            # 키 누름 표시
            for q in range(len(blacks)):
                if blacks[q][0] == i:
                    if blacks[q][1] > 0:
                        pygame.draw.rect(self.screen, 'green',
                                         [black_w + (i*white_w) + (skip_count*white_w),
                                          self.HEIGHT-white_h, black_w, black_h], 2, 2)
                        blacks[q][1] -= 1
            # 노트 이름 텍스트
            key_label = self.real_small_font.render(self.black_labels[i], True, 'white')
            self.screen.blit(key_label,
                             (black_w + (i*white_w) + (skip_count*white_w) + 4,
                              self.HEIGHT - 120))
            black_rects.append(rect)
            # 흑건 등장 패턴
            skip_track += 1
            if last_skip == LINE_CDE and skip_track == LINE_FGAB:
                last_skip = LINE_FGAB
                skip_track = 0
                skip_count += 1
            elif last_skip == LINE_FGAB and skip_track == LINE_CDE:
                last_skip = LINE_CDE
                skip_track = 0
                skip_count += 1

        return white_rects, black_rects, whites, blacks

    # 키설명
    def draw_hands(self):
        rect_w = 35
        rect_w7 = rect_w * 7
        rect_w11 = rect_w * 11
        rect_h = 30

        # 왼손
        pygame.draw.rect(self.screen, 'dark gray',
                         [((self.left_oct - self.MIN_OCT) * rect_w7),
                          self.HEIGHT - 60, rect_w7, rect_h], 0, 4)
        pygame.draw.rect(self.screen, 'black',
                         [((self.left_oct - self.MIN_OCT) * rect_w7),
                          self.HEIGHT - 60, rect_w7, rect_h], 4, 4)
        for i in range(len(self.left_hand)):
            color = 'white'
            blank_space=10
            if (i==0 or i==2 or i==4 or i==5 or i==7 or i==9 or i==11):
                pass # 백건
            else:
                color = 'black' # 흑건
            if (i < 5):
                pass
            else:
                blank_space += 16 # 흑건 없는 부분 띄움
            text = self.small_font.render(self.left_hand[i], True, color)
            self.screen.blit(text, (((self.left_oct - 3) * 245) + 18 * i + blank_space, self.HEIGHT - 55))

        # 오른손
        pygame.draw.rect(self.screen, 'dark gray', [((self.right_oct - self.MIN_OCT) * rect_w7 - rect_w * 4),
                                                    self.HEIGHT - 86, rect_w11, rect_h], 0, 4)
        pygame.draw.rect(self.screen, 'black', [((self.right_oct - self.MIN_OCT) * rect_w7 - rect_w * 4),
                                                self.HEIGHT - 86, rect_w11, rect_h], 4, 4)

        for i in range(len(self.right_hand)):
            color = 'white'
            blank_space = 10
            if (i==0 or i==2 or i==4 or i==6 or i==7 or i==9 or
                    i==11 or i==12 or i==14 or i==16 or i==18):
                pass # 백건
            else:
                color = 'black' # 흑건
            if (i < 7):
                pass
            elif (i < 12):
                blank_space += 16 # 흑건 없는 부분 띄움
            else:
                blank_space += 32 # 흑건 없는 부분 띄움
            text = self.small_font.render(self.right_hand[i], True, color)
            self.screen.blit(text,
                             (((self.right_oct - 3) * rect_w7 - rect_w * 4) + 18 * i + blank_space,
                              self.HEIGHT - 81))

class Note: # 음표
    WIDTH = 30
    HEIGHT = 60

    # 음표 이미지
    IMG_note_2 = pygame.image.load("images/note_half.png")
    IMG_note_2 = pygame.transform.scale(IMG_note_2, (WIDTH, HEIGHT))
    IMG_note_2up = pygame.image.load("images/note_half.png")
    IMG_note_2up = pygame.transform.scale(IMG_note_2up, (WIDTH, HEIGHT))
    IMG_note_2up = pygame.transform.rotate(IMG_note_2up, 180)
    IMG_note_4 = pygame.image.load("images/note_quarter.png")
    IMG_note_4 = pygame.transform.scale(IMG_note_4, (WIDTH, HEIGHT))
    IMG_note_4up = pygame.image.load("images/note_quarter.png")
    IMG_note_4up = pygame.transform.scale(IMG_note_4up, (WIDTH, HEIGHT))
    IMG_note_4up = pygame.transform.rotate(IMG_note_4up, 180)
    IMG_note_8 = pygame.image.load("images/note_eighth.png")
    IMG_note_8 = pygame.transform.scale(IMG_note_8, (WIDTH, HEIGHT))
    IMG_note_8up = pygame.image.load("images/note_eighth_up.png")
    IMG_note_8up = pygame.transform.scale(IMG_note_8up, (WIDTH, HEIGHT))
    IMG_note_16 = pygame.image.load("images/note_sixteenth.png")
    IMG_note_16 = pygame.transform.scale(IMG_note_16, (WIDTH, HEIGHT))
    IMG_note_16up = pygame.image.load("images/note_sixteenth_up.png")
    IMG_note_16up = pygame.transform.scale(IMG_note_16up, (WIDTH, HEIGHT))

    def __init__(self, screen, pitch, note):
        self.screen = screen
        self.list_pitches = pl.piano_pitches

        self.set_pitch_value(pitch)
        self.set_note_value(note)
        self.set_note_image()

    def set_pitch_value(self, name):
        if len(name) > 2:
            if name[-1] == "s" or "#":
                self.pitch = name[0] + name[1] + "#"
        else:
            self.pitch = name

    def set_note_value(self, name):
        if name == "4" or "4th" or 4 or "quarter":
            self.note = 4 # 4분 음표
        elif name == "8" or "8th" or 8 or "eighth":
            self.note = 8 # 8분 음표
        elif name == "2" or "2nd" or 2 or "second" or "half":
            self.note = 2 # 2분 음표
        elif name == "16" or "16th" or 2 or "sixteenth":
            self.note = 16 # 16분 음표
        else:
            self.note = None

    def set_note_image(self):
        index_B4 = self.list_pitches.index("B4") # 4옥타브 시
        index_pitch = self.list_pitches.index(self.pitch)

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

    #음표 그리기
    def draw_note(self, step):
        Y_C3 = 166  # 오선지 C4(도) 선 위치
        Y_B4 = 212  # 오선지 B4(시) 선 위치
        X = self.WIDTH + step

        pitch_name = ""
        if len(self.pitch):
            pitch_name = self.pitch[0:2]
        index_C4 = pl.white_pitches.index("C4")
        index_pitch = pl.white_pitches.index(pitch_name)
        level = index_pitch - index_C4

        if self.is_down:
            self.screen.blit(self.image, (X, Y_C3 - level*7))
        else:
            self.screen.blit(self.image, (X, Y_B4 - level * 7))

        return X

#GUI 제목/설명
def draw_title_bar(screen, font, medium_font):
    instruction_text = medium_font.render('Up/Down Key Change Left Hand octave', True, 'black')
    screen.blit(instruction_text, (WIDTH - 480, 10))
    instruction_text2 = medium_font.render('Left/Right Key Change Right Hand octave', True, 'black')
    screen.blit(instruction_text2, (WIDTH - 480, 50))
    # img = pygame.transform.scale(pygame.image.load('logo.png'), [150, 150])
    # screen.blit(img, (-20, -30))
    title_text = font.render('Python Piano GUI', True, 'white')
    screen.blit(title_text, (10, 18))
    title_text = font.render('Python Piano GUI', True, 'black')
    screen.blit(title_text, (12, 20))

#오선지 그리기
def draw_music_sheet(screen, width):
    y = 120
    height = 154
    interval = 14

    pygame.draw.rect(screen, 'white', [0, y, width, height])
    for i in range(1, 6) :
        pygame.draw.line(screen, 'black', [0, y + i * interval + interval],
                         [width, y + i * interval + interval], 2)

if __name__ == '__main__':
    FPS = 60

    piano_pitches = pl.piano_pitches
    white_pitches = pl.white_pitches
    black_pitches = pl.black_pitches

    WIDTH = 50 * len(white_pitches)
    HEIGHT = 500

    white_sounds = []
    black_sounds = []
    active_whites = []
    active_blacks = []

    input_notes = []

    #########################################################
    pygame.init()
    pygame.mixer.set_num_channels(50)
    pygame.display.set_caption("Piano GUI")
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    timer = pygame.time.Clock()

    # 폰트
    font = pygame.font.SysFont('arial', 48)
    medium_font = pygame.font.SysFont('arial', 28)
    small_font = pygame.font.SysFont('arial', 16)
    real_small_font = pygame.font.SysFont('arial', 10)

    # 소리 파일
    for i in range(len(white_pitches)):
        white_sounds.append(mixer.Sound(f'sound\\{white_pitches[i]}.wav'))
    for i in range(len(black_pitches)):
        black_sounds.append(mixer.Sound(f'sound\\{black_pitches[i]}.wav'))

    # 피아노 GUI 클래스
    gui_piano = PianoGUI(screen, WIDTH, HEIGHT, white_sounds, black_sounds, small_font, real_small_font)

    run = True
    while run:
        timer.tick(FPS)
        screen.fill('gray')
        white_keys, black_keys, active_whites, active_blacks = gui_piano.draw_piano(active_whites, active_blacks)
        gui_piano.draw_hands()
        draw_title_bar(screen, font, medium_font)
        draw_music_sheet(screen, WIDTH)

        for event in pygame.event.get():
            input_pitch = ""  # 입력한 음

            if event.type == pygame.QUIT:
                run = False
            # 마우스 클릭
            if event.type == pygame.MOUSEBUTTONDOWN:
                black_key = False
                for i in range(len(black_keys)):
                    if black_keys[i].collidepoint(event.pos):
                        black_sounds[i].play(0, 1000)
                        black_key = True
                        active_blacks.append([i, 30])
                for i in range(len(white_keys)):
                    if white_keys[i].collidepoint(event.pos) and not black_key:
                        white_sounds[i].play(0, 3000)
                        active_whites.append([i, 30])
            # 키보드 입력
            if event.type == pygame.TEXTINPUT:
                # 왼손
                if event.text.upper() in gui_piano.left_dict:
                    input_pitch = gui_piano.left_dict[event.text.upper()]
                    # 음 출력
                    if gui_piano.left_dict[event.text.upper()][-1] == 's':
                        index = black_pitches.index(gui_piano.left_dict[event.text.upper()])
                        black_sounds[index].play(0, 1000)
                        active_blacks.append([index, 30])
                    else:
                        index = white_pitches.index(gui_piano.left_dict[event.text.upper()])
                        white_sounds[index].play(0, 1000)
                        active_whites.append([index, 30])
                # 오른손
                if event.text.upper() in gui_piano.right_dict:
                    input_pitch = gui_piano.right_dict[event.text.upper()]
                    # 음 출력
                    if gui_piano.right_dict[event.text.upper()][-1] == 's':
                        index = black_pitches.index(gui_piano.right_dict[event.text.upper()])
                        black_sounds[index].play(0, 1000)
                        active_blacks.append([index, 30])
                    else:
                        index = white_pitches.index(gui_piano.right_dict[event.text.upper()])
                        white_sounds[index].play(0, 1000)
                        active_whites.append([index, 30])
                # 입력한 음 저장
                if (input_pitch != ""):
                    note = Note(screen, input_pitch, 4)
                    input_notes.append(note)


            if event.type == pygame.KEYDOWN:
                # 상/하/좌/우 키 : 옥타브 조절
                if event.key == pygame.K_RIGHT:
                    if gui_piano.right_oct < 5:
                        gui_piano.set_right_oct(gui_piano.get_right_oct() + 1)
                if event.key == pygame.K_LEFT:
                    if gui_piano.right_oct > 4:
                        gui_piano.set_right_oct(gui_piano.get_right_oct() - 1)
                if event.key == pygame.K_UP:
                    if gui_piano.left_oct < 5:
                        gui_piano.set_left_oct(gui_piano.get_left_oct() + 1)
                if event.key == pygame.K_DOWN:
                    if gui_piano.left_oct > 3:
                        gui_piano.set_left_oct(gui_piano.get_left_oct() - 1)
                gui_piano.update_keys_set()
                # delete 키 : 마지막 음표 삭제
                if event.key == pygame.K_DELETE:
                    if input_notes:
                        input_notes.pop()
                # ESC 키 : 프로그램 종료
                if event.key == pygame.K_ESCAPE:
                    print("프로그램 종료")
                    run = False

        if input_notes:
            step = 0
            for index, note in enumerate(input_notes):
                step = note.draw_note(step)

        pygame.display.flip()

    pygame.quit()