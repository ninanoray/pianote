import csv

import pygame
from pygame import mixer

import piano_lists as pl
import piano_gui as GUI
import note as Note

#-----전역 변수---------------------------------------------------------------------------------------------------------#

#-----클래스 선언-------------------------------------------------------------------------------------------------------#


#-----함수 선언---------------------------------------------------------------------------------------------------------#
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

#-----main-------------------------------------------------------------------------------------------------------------#
if __name__ == '__main__':
    WHITE_SOUNDS = []
    BLACK_SOUNDS = []
    
    FPS = 60

    piano_pitches = pl.piano_pitches
    white_pitches = pl.white_pitches
    black_pitches = pl.black_pitches

    WIDTH = 50 * len(white_pitches)
    HEIGHT = 500

    #########################################################

    # pygame 생성
    pygame.init()
    pygame.mixer.set_num_channels(50)
    pygame.display.set_caption("Piano GUI")
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    timer = pygame.time.Clock()

    # 악보 파일 가져오기
    print("악보 파일(.csv)을 가져오시겠습니까?(y/아무거나)")
    is_yes = input()
    if is_yes == "y":
        print("파일명을 입력하세요: ")
        filename_score = input()
        read_score = open(f"scores/{filename_score}.csv", 'r')
        reader = csv.reader(read_score)
        input_notes = [Note.Note(screen, note_info[0], int(note_info[1])) for note_info in reader]
    else:
        input_notes = []  # 프로그램에서 사용자가 입력할 악보 정보

    # 폰트
    font = pygame.font.SysFont('arial', 48)
    medium_font = pygame.font.SysFont('arial', 28)
    small_font = pygame.font.SysFont('arial', 16)
    real_small_font = pygame.font.SysFont('arial', 10)

    # 소리 파일
    for i in range(len(white_pitches)):
        WHITE_SOUNDS.append(mixer.Sound(f'sound\\{white_pitches[i]}.wav'))
    for i in range(len(black_pitches)):
        BLACK_SOUNDS.append(mixer.Sound(f'sound\\{black_pitches[i]}.wav'))

    Note.WHITE_SOUNDS = WHITE_SOUNDS
    Note.BLACK_SOUNDS = BLACK_SOUNDS

    # 피아노 GUI 클래스
    gui_piano = GUI.PianoGUI(screen, WIDTH, HEIGHT, small_font, real_small_font)

    # 해당 리스트의 마지막 값 == 클릭 가능한 음표의 시작 인덱스
    count_music_sheet = [0]

    run = True
    offset_note_input = 0
    while run:
        timer.tick(FPS)
        screen.fill('gray')
        white_keys, black_keys = gui_piano.draw_piano()
        gui_piano.draw_hands()
        # 제목/설명 출력
        draw_title_bar(screen, font, medium_font)
        # 오선지 그리기
        Note.draw_music_sheet(screen, WIDTH)

        for event in pygame.event.get():
            input_pitch = ""  # 입력한 음

            # 마우스 클릭
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 피아노 건반 클릭
                black_key = False
                for i in range(len(black_keys)):
                    if black_keys[i].collidepoint(event.pos):
                        BLACK_SOUNDS[i].play(0, 1000)
                        black_key = True
                        GUI.active_blacks.append([i, 30])
                for i in range(len(white_keys)):
                    if white_keys[i].collidepoint(event.pos) and not black_key:
                        WHITE_SOUNDS[i].play(0, 3000)
                        GUI.active_whites.append([i, 30])
                # 음표 클릭
                if input_notes:
                    for i in range(count_music_sheet[-1], len(input_notes)):
                        if input_notes[i].rect.collidepoint(event.pos):
                            # 좌클릭 : 클릭한 음표로 입력커서 이동
                            if event.button == 1:
                                offset_note_input = i + 1
                                break
                            # 우클릭 : 클릭한 음표 삭제
                            if event.button == 3:
                                input_notes.pop(i)
                                break
                            # 휠업(4) : 음표 길어짐
                            tmp = input_notes.pop(i)
                            th = tmp.get_note()
                            if event.button == 5:
                                if th < 9:
                                    th = int(th * 2)
                            # 휠다운(5) : 음표 짧아짐
                            if event.button == 4:
                                if th > 2:
                                    th = int(th / 2)
                            tmp.set_note(th)
                            tmp.set_image()
                            tmp.draw_note(tmp.X)
                            input_notes.insert(i, tmp)


            # 키보드 값 입력
            if event.type == pygame.TEXTINPUT:
                # 왼손
                if event.text.upper() in gui_piano.left_dict:
                    input_pitch = gui_piano.left_dict[event.text.upper()]
                    # 음 출력
                    if gui_piano.left_dict[event.text.upper()][-1] == 's':
                        index = black_pitches.index(gui_piano.left_dict[event.text.upper()])
                        BLACK_SOUNDS[index].play(0, 1000) # 소리 출력
                        GUI.active_blacks.append([index, 30]) # 효과 출력
                    else:
                        index = white_pitches.index(gui_piano.left_dict[event.text.upper()])
                        WHITE_SOUNDS[index].play(0, 1000)
                        GUI.active_whites.append([index, 30])
                # 오른손
                if event.text.upper() in gui_piano.right_dict:
                    input_pitch = gui_piano.right_dict[event.text.upper()]
                    # 음 출력
                    if gui_piano.right_dict[event.text.upper()][-1] == 's':
                        index = black_pitches.index(gui_piano.right_dict[event.text.upper()])
                        BLACK_SOUNDS[index].play(0, 1000)
                        GUI.active_blacks.append([index, 30])
                    else:
                        index = white_pitches.index(gui_piano.right_dict[event.text.upper()])
                        WHITE_SOUNDS[index].play(0, 1000)
                        GUI.active_whites.append([index, 30])
                # 입력한 음 저장
                if (input_pitch != ""):
                    print(f'입력: {input_pitch}')
                    #==================Note 객체 생성===================
                    note = Note.Note(screen, input_pitch)
                    input_notes.insert(offset_note_input, note)
                    offset_note_input += 1


            # 키보드 키 이벤트
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
                        removed_note = input_notes.pop()
                        print(f'삭제: {removed_note.get_pitch()}({removed_note.get_note()}th)')
                # Enter 키 : 악보 재생
                if event.key == 13:
                    if input_notes:
                        for note in input_notes:
                            # 4/4박자에서 4분음표 1초에 1개
                            time = int(1000 / (note.get_note()/4))
                            note.get_sound().play(0, 1000)
                            pygame.time.delay(time)

                # ESC 키 : 프로그램 종료
                if event.key == pygame.K_ESCAPE:
                    print("GUI program 종료")
                    run = False


        # 음표를 옆으로 그려나가면서 오선지에 그려지는 것들
        if input_notes:
            step = 0
            for note in input_notes:
                # B4이하 음표 8분음표 16분음표 간격 조정
                if note.get_note() > 4 and note.is_down:
                    step = note.draw_note(step) + (note.WIDTH2-note.WIDTH)
                else:
                    step = note.draw_note(step)

                # 오선지 윗선 넘기면 음표에 줄표시
                SPACE = Note.INTERVAL_LINE
                if (note.rect.y < Note.Y_SHEET + SPACE) and not note.is_down:
                    pygame.draw.line(screen, 'black', [note.rect.x - 2, Note.Y_SHEET + SPACE],
                                     [note.rect.x + 22, Note.Y_SHEET + SPACE], 2)
                # 오선지 아랫선 넘기면 음표에 줄표시
                BOTTOM_SHEET = Note.Y_SHEET + SPACE * 7
                NOTE_HEAD = note.rect.y + note.HEIGHT
                A = 2 # 조정값
                for i in range(4):
                    if (BOTTOM_SHEET + SPACE * i + A < NOTE_HEAD) and note.is_down:
                        pygame.draw.line(screen, 'black', [note.rect.x - 4, BOTTOM_SHEET + SPACE * i],
                                         [note.rect.x + 22, BOTTOM_SHEET + SPACE * i], 2)

                # 오선지 밖으로 넘으면 오선지 다시 그림
                if note.X > WIDTH - note.WIDTH:
                    count_music_sheet.append(input_notes.index(note))
                    Note.draw_music_sheet(screen, WIDTH)
                    step = 0
                    note.set_X(10)
                    step = note.draw_note(step)
                # 음표를 지우다 이전 오선지로 돌아가면
                elif note.X > WIDTH - note.WIDTH * 2:
                    if count_music_sheet[-1] != 0: # 기본값(0)은 남김
                        count_music_sheet.pop()

        pygame.display.flip()

    pygame.quit() # GUI 종료

    # 저장된 노트 정보
    saved_notes = [(note.get_pitch(), note.get_note()) for note in input_notes]
    print(saved_notes)

    # 저장된 노트 정보로 csv 악보 파일 만들기
    print("\n악보를 저장하시겠습니까?(y/아무거나)")
    yes = input()
    if yes == "y":
        print("파일 이름을 입력하세요: ")
        filename = input()
        create_score = open(f'scores/{filename}.csv', 'w', newline='')
        writer = csv.writer(create_score)
        writer.writerows(saved_notes)
    else:
        print("저장하지 않고 종료했습니다")
        