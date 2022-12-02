import pygame
import piano_lists as pl
import PianoGUI as gui
from pygame import mixer

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

    def __init__(self, screen, pitch, note=4):
        self.screen = screen
        self.list_pitches = pl.piano_pitches

        self.set_pitch(pitch)
        self.note = note
        self.set_image()

    def set_pitch(self, name):
        print(name)
        if 's' in name:
            self.pitch = name.replace('s', '#')
        else:
            self.pitch = name

    def set_image(self):
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

    def get_pitch(self):
        return self.pitch

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
            self.screen.blit(self.image, (X, Y_C3 - level*7)) # 7 = 오선지 interval/2
        else:
            self.screen.blit(self.image, (X, Y_B4 - level*7))

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
    gui_piano = gui.PianoGUI(screen, WIDTH, HEIGHT, white_sounds, black_sounds, small_font, real_small_font)

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
                    note = Note(screen, input_pitch)
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

    # 저장된 노트 정보
    saved_notes = [note.get_pitch() for note in input_notes]
    print(saved_notes)