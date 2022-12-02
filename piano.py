import pygame
import piano_lists as pl
from pygame import mixer

#########################################################
#                      초기화
pygame.init()

fps = 60
timer = pygame.time.Clock()
WIDTH = 50 * len(pl.white_pitches)
HEIGHT = 400
screen = pygame.display.set_mode([WIDTH, HEIGHT])
white_sounds = []
black_sounds = []
active_whites = []
active_blacks = []
MIN_OCT = 3 # 최소 옥타브
left_oct = MIN_OCT + 1
right_oct = MIN_OCT + 2

left_hand = pl.left_hand
right_hand = pl.right_hand
piano_notes = pl.piano_pitches
white_notes = pl.white_pitches
black_notes = pl.black_pitches
black_labels = pl.black_labels

font = pygame.font.SysFont('arial', 48)
medium_font = pygame.font.SysFont('arial', 28)
small_font = pygame.font.SysFont('arial', 16)
real_small_font = pygame.font.SysFont('arial', 10)

#########################################################

#GUI 제목/설명
def draw_title_bar():
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

# 피아노 모양 생성
def draw_piano(whites, blacks):
    white_w = 35
    white_h = 200
    black_w = 24
    black_h = 100

    # 백건
    white_rects = []
    for i in range(len(white_notes)):
        rect = pygame.draw.rect(screen, 'white', [i*white_w, HEIGHT-white_h, white_w, white_h], 0, 2)
        white_rects.append(rect)
        pygame.draw.rect(screen, 'black', [i*white_w, HEIGHT-white_h, white_w, white_h], 2, 2)
        # 노트 이름 텍스트
        key_label = small_font.render(white_notes[i], True, 'black')
        screen.blit(key_label, (i * white_w + 8, HEIGHT - 20))
    # 키 누름 표시
    for i in range(len(whites)):
        if whites[i][1] > 0:
            j = whites[i][0]
            pygame.draw.rect(screen, 'green', [j*white_w, HEIGHT-white_h, white_w, white_h], 2, 2)
            whites[i][1] -= 1

    # 흑건
    LINE_CDE = 2 # 도레미 흑건
    LINE_FGAB = 3 # 파솔라시 흑건
    skip_count = 0
    last_skip = LINE_FGAB
    skip_track = 0
    black_rects = []
    for i in range(len(black_labels)):
        rect = pygame.draw.rect(screen, 'black', [black_w + (i*white_w) + (skip_count*white_w),
                                                  HEIGHT-white_h, black_w, black_h], 0, 2)
        # 키 누름 표시
        for q in range(len(blacks)):
            if blacks[q][0] == i:
                if blacks[q][1] > 0:
                    pygame.draw.rect(screen, 'green', [black_w + (i*white_w) + (skip_count*white_w),
                                                       HEIGHT-white_h, black_w, black_h], 2, 2)
                    blacks[q][1] -= 1
        # 노트 이름 텍스트
        key_label = real_small_font.render(black_labels[i], True, 'white')
        screen.blit(key_label, (black_w + (i*white_w) + (skip_count*white_w) + 4, HEIGHT - 120))
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
def draw_hands(rightOct, leftOct, rightHand, leftHand):
    rect_w = 35
    rect_w7 = rect_w * 7
    rect_w11 = rect_w * 11
    rect_h = 30

    # 왼손
    pygame.draw.rect(screen, 'dark gray', [((leftOct-MIN_OCT) * rect_w7), HEIGHT - 60, rect_w7, rect_h], 0, 4)
    pygame.draw.rect(screen, 'black', [((leftOct-MIN_OCT) * rect_w7), HEIGHT - 60, rect_w7, rect_h], 4, 4)
    for i in range(len(leftHand)):
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
        text = small_font.render(leftHand[i], True, color)
        screen.blit(text, (((leftOct-3) * 245) + 18*i + blank_space, HEIGHT - 55))

    # 오른손
    pygame.draw.rect(screen, 'dark gray', [((rightOct-MIN_OCT) * rect_w7 - rect_w*4), HEIGHT - 86, rect_w11, rect_h], 0, 4)
    pygame.draw.rect(screen, 'black', [((rightOct-MIN_OCT) * rect_w7 - rect_w*4), HEIGHT - 86, rect_w11, rect_h], 4, 4)
    for i in range(len(rightHand)):
        color = 'white'
        blank_space = 10
        if (i==0 or i==2 or i==4 or i==6 or i==7 or i==9 or i==11 or i==12 or i==14 or i==16 or i==18):
            pass # 백건
        else:
            color = 'black' # 흑건
        if (i < 7):
            pass
        elif (i < 12):
            blank_space += 16 # 흑건 없는 부분 띄움
        else:
            blank_space += 32 # 흑건 없는 부분 띄움
        text = small_font.render(rightHand[i], True, color)
        screen.blit(text, (((rightOct - 3) * rect_w7 - rect_w*4) + 18 * i + blank_space, HEIGHT - 81))

if __name__ == '__main__':
    pygame.mixer.set_num_channels(50)

    for i in range(len(white_notes)):
        white_sounds.append(mixer.Sound(f'sound\\{white_notes[i]}.wav'))

    for i in range(len(black_notes)):
        black_sounds.append(mixer.Sound(f'sound\\{black_notes[i]}.wav'))

    pygame.display.set_caption("Piano GUI")

    run = True
    while run:
        # 클릭 키 연결
        left_dict = {'Z': f'C{left_oct}',
                     'S': f'C{left_oct}s',
                     'X': f'D{left_oct}',
                     'D': f'D{left_oct}s',
                     'C': f'E{left_oct}',
                     'V': f'F{left_oct}',
                     'G': f'F{left_oct}s',
                     'B': f'G{left_oct}',
                     'H': f'G{left_oct}s',
                     'N': f'A{left_oct}',
                     'J': f'A{left_oct}s',
                     'M': f'B{left_oct}'}

        right_dict = {'W': f'F{right_oct-1}',
                      '3': f'F{right_oct-1}s',
                      'E': f'G{right_oct-1}',
                      '4': f'G{right_oct-1}s',
                      'R': f'A{right_oct-1}',
                      '5': f'A{right_oct-1}s',
                      'T': f'B{right_oct-1}',
                      'Y': f'C{right_oct}',
                      '7': f'C{right_oct}s',
                      'U': f'D{right_oct}',
                      '8': f'D{right_oct}s',
                      'I': f'E{right_oct}',
                      'O': f'F{right_oct}',
                      '0' : f'F{right_oct}s',
                      'P': f'G{right_oct}',
                      '-': f'G{right_oct}s',
                      '[': f'A{right_oct}',
                      '=': f'A{right_oct}s',
                      ']': f'B{right_oct}'}

        timer.tick(fps)
        screen.fill('gray')
        white_keys, black_keys, active_whites, active_blacks = draw_piano(active_whites, active_blacks)
        draw_hands(right_oct, left_oct, right_hand, left_hand)
        draw_title_bar()

        for event in pygame.event.get():
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
                if event.text.upper() in left_dict:
                    if left_dict[event.text.upper()][-1] == 's':
                        index = black_notes.index(left_dict[event.text.upper()])
                        black_sounds[index].play(0, 1000)
                        active_blacks.append([index, 30])
                    else:
                        index = white_notes.index(left_dict[event.text.upper()])
                        white_sounds[index].play(0, 1000)
                        active_whites.append([index, 30])
                if event.text.upper() in right_dict:
                    if right_dict[event.text.upper()][-1] == 's':
                        index = black_notes.index(right_dict[event.text.upper()])
                        black_sounds[index].play(0, 1000)
                        active_blacks.append([index, 30])
                    else:
                        index = white_notes.index(right_dict[event.text.upper()])
                        white_sounds[index].play(0, 1000)
                        active_whites.append([index, 30])

            # 상/하/좌/우 키 : 옥타브 조절
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if right_oct < 5:
                        right_oct += 1
                if event.key == pygame.K_LEFT:
                    if right_oct > 4:
                        right_oct -= 1
                if event.key == pygame.K_UP:
                    if left_oct < 5:
                        left_oct += 1
                if event.key == pygame.K_DOWN:
                    if left_oct > 3:
                        left_oct -= 1

        pygame.display.flip()
    pygame.quit()