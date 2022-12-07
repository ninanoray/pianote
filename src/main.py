import csv
import pygame
from pygame import mixer

import piano_lists as pl
import piano_gui as gui
import note as nt

#-----함수선언----------------------------------------------------------------------------------------------------------#
#GUI 제목/설명
def draw_title_bar(screen, font_1, font_2):
    # 타이틀
    title_text = font_1.render('Pianote', True, 'white')
    screen.blit(title_text, (10, 18))
    title_text = font_1.render('Pianote', True, 'black')
    screen.blit(title_text, (12, 20))
    intro_1 = 260
    intro_2 = 600
    # 기능 설명 : 키
    instruction_text = font_2.render('[↑↓] 키 : 왼손 옥타브 변경', True, 'black')
    screen.blit(instruction_text, (WIDTH - intro_1, 10))
    instruction_text2 = font_2.render('[←→] 키 : 오른손 옥타브 변경', True, 'black')
    screen.blit(instruction_text2, (WIDTH - intro_1, 30))
    instruction_text3 = font_2.render('BackSpace 키 : 마지막 음표 삭제', True, 'black')
    screen.blit(instruction_text3, (WIDTH - intro_1, 50))
    instruction_text4 = font_2.render('Space 바 : 악보 재생', True, 'blue')
    screen.blit(instruction_text4, (WIDTH - intro_1, 70))
    instruction_text5 = font_2.render('Esc 키 : Pianote 종료. 악보 저장.', True, 'red')
    screen.blit(instruction_text5, (WIDTH - intro_1, 90))
    # 기능 설명 : 음표클릭
    instruction2_text = font_2.render('음표 좌클릭 : 클릭 음표 다음부터 입력', True, 'black')
    screen.blit(instruction2_text, (WIDTH - intro_2, 10))
    instruction2_text2 = font_2.render('음표 우클릭 : 클릭 음표 삭제', True, 'black')
    screen.blit(instruction2_text2, (WIDTH - intro_2, 30))
    instruction2_text3 = font_2.render('음표 휠업/휠다운 : 음표 길이 변경(?분음표)', True, 'black')
    screen.blit(instruction2_text3, (WIDTH - intro_2, 50))

# 텍스트(파일명)를 받는 GUI
def input_text_gui(screen, font, text, input):
    img_text_1 = font.render(text, True, 'black') # 설명 문구
    img_text_2 = font.render("파일명 :", True, 'blue')
    rect_text_1 = img_text_1.get_rect()
    rect_text_2 = img_text_2.get_rect()
    rect_text_1.topleft = (40, 50)
    rect_text_2.topleft = (40, 100)

    img_input = font.render(input, True, 'red') # 텍스트 입력창
    rect = img_input.get_rect()
    rect.topleft = (140, 100)
    cursor = pygame.Rect(rect.topright, (2, rect.height))

    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, 500)
    time_counter = 0

    run = True
    while(run):
        screen.fill('white')
        screen.blit(img_text_1, rect_text_1)
        screen.blit(img_text_2, rect_text_2)
        screen.blit(img_input, rect)
        if time_counter % 2: # 커서 깜박임
            pygame.draw.rect(screen, 'red', cursor)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if len(input) > 0:
                        input = input[:-1]
                else:
                    input += event.unicode
                img_input = font.render(input, True, 'red')
                rect.size = img_input.get_size()
                cursor.topleft = rect.topright

                # Enter 누르면 종료
                if event.key == 13:
                    run = False

            if event.type == timer_event:
                time_counter +=1

        pygame.display.update()

    return input

# 음표 오선지에 그리기
def draw_step_note(note, step):
    # B4이하 음표 8분음표 16분음표 간격 조정
    if (note.get_note() > 4) and note.is_down:
        step = note.draw_note(step) + (note.WIDTH2 - note.WIDTH)
    else:
        step = note.draw_note(step)
    # 오선지 윗선 넘기면 음표에 줄표시
    SPACE = nt.Sheet.INTERVAL_LINE
    if (note.rect.y < nt.Sheet.Y_SHEET + SPACE) and not note.is_down:
        pygame.draw.line(screen, 'black', [note.rect.x - 2, nt.Sheet.Y_SHEET + SPACE],
                         [note.rect.x + 22, nt.Sheet.Y_SHEET + SPACE], 2)
    # 오선지 아랫선 넘기면 음표에 줄표시
    BOTTOM_SHEET = nt.Sheet.Y_SHEET + SPACE * 7
    NOTE_HEAD = note.rect.y + note.HEIGHT
    A = 2  # 조정값
    for i in range(4):
        if (BOTTOM_SHEET + SPACE * i + A < NOTE_HEAD) and note.is_down:
            pygame.draw.line(screen, 'black', [note.rect.x - 4, BOTTOM_SHEET + SPACE * i],
                             [note.rect.x + 22, BOTTOM_SHEET + SPACE * i], 2)

    return step

#-----main-------------------------------------------------------------------------------------------------------------#
if __name__ == '__main__':
    WHITE_SOUNDS = []
    BLACK_SOUNDS = []
    
    FPS = 30

    CUSTOM_COL_1 = (245, 230, 207)
    CUSTOM_COL_2 = (187, 146, 100)

    piano_pitches = pl.piano_pitches
    white_pitches = pl.white_pitches
    black_pitches = pl.black_pitches

    WIDTH = 50 * len(white_pitches)
    HEIGHT = 500

    #------------------------------------------------#

    # pygame 생성
    pygame.init()
    pygame.mixer.set_num_channels(50)
    pygame.display.set_caption("Pianote")
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    timer = pygame.time.Clock()

    # 폰트
    font = pygame.font.SysFont('arial', 60)
    medium_font = pygame.font.SysFont('arial', 28)
    small_font = pygame.font.SysFont('arial', 16)
    real_small_font = pygame.font.SysFont('arial', 10)
    medium_font_kor = pygame.font.SysFont('malgungothic', 24)
    small_font_kor = pygame.font.SysFont('malgungothic', 16)

    # 소리 파일
    for white_pitch in white_pitches:
        WHITE_SOUNDS.append(mixer.Sound(f'../sound\piano_main\\{white_pitch}.wav'))
    for black_pitch in black_pitches:
        BLACK_SOUNDS.append(mixer.Sound(f'../sound\piano_main\\{black_pitch}.wav'))
    SOUND_PLAY_SEC = 2000 # 사운드 재생 시간

    nt.WHITE_SOUNDS = WHITE_SOUNDS
    nt.BLACK_SOUNDS = BLACK_SOUNDS

    # 피아노 GUI 클래스
    gui_piano = gui.PianoGUI(screen, WIDTH, HEIGHT, small_font, real_small_font)

    input_notes = [] # 프로그램에서 사용자가 입력할 악보 정보
    offset_note_input = 0 # 음표 입력 커서 오프셋
    music_sheets = [] # 오선지

    #----- 1 파일명 입력 받아 파일 불러오기-------------------------------------------------------------------------------#
    input_filename = ''  # 파일명
    instruction = "[START] 악보 파일명 입력 후 Enter (새로 시작 : 바로 Enter)"
    input_filename = input_text_gui(screen, medium_font_kor, instruction, input_filename)

    if input_filename[:-1]: # 아무것도 입력하지 않고 Enter 누르면 "\r"
        read_score = open(f"../scores/{input_filename[:-1]}.csv", 'r')
        reader = csv.reader(read_score)
        print('[START] 파일데이터')
        for sheet_notes_data in reader:
            print(sheet_notes_data)
            file_pitch = ''
            if len(music_sheets) > 0:
                file_sheet = nt.Sheet(screen, 'treble', '')
                music_sheets.append(file_sheet)
            else: # 처음에만 박자표를 그림
                first_sheet = nt.Sheet(screen, 'treble', '4/4')
                music_sheets.append(first_sheet)
            for i, data in enumerate(sheet_notes_data):
                if i%2 == 0:
                    file_pitch = data
                else:
                    file_note = nt.Note(screen, file_pitch, int(data))
                    music_sheets[-1].notes.append(file_note)
        offset_note_input = len(music_sheets[-1].notes)
        print(f'[START] Pianote 시작. 불러온 악보 파일명 : {input_filename[:-1]}.csv\n')
    else:
        first_sheet = nt.Sheet(screen, 'treble', '4/4')
        music_sheets.append(first_sheet)
        print('[START] Pianote 처음 시작.\n')

    #----- 2. 피아노 GUI------------------------------------------------------------------------------------------------#
    run = True
    while run:
        timer.tick(FPS)
        screen.fill(CUSTOM_COL_1)
        white_keys, black_keys = gui_piano.draw_piano()
        gui_piano.draw_hands()
        # 제목/설명 출력
        draw_title_bar(screen, font, small_font_kor)
        # 마지막 오선지 그리기
        sheet = music_sheets[-1]
        sheet.draw_sheet(WIDTH)

        for event in pygame.event.get():
            input_pitch = ""  # 입력한 음

            # 마우스 클릭
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 피아노 건반 클릭
                black_key = False
                for i in range(len(black_keys)):
                    if black_keys[i].collidepoint(event.pos):
                        BLACK_SOUNDS[i].play(0, SOUND_PLAY_SEC)
                        black_key = True
                        gui.active_blacks.append([i, 30])
                for i in range(len(white_keys)):
                    if white_keys[i].collidepoint(event.pos) and not black_key:
                        WHITE_SOUNDS[i].play(0, SOUND_PLAY_SEC)
                        gui.active_whites.append([i, 30])
                # 음표 클릭
                if sheet.notes:
                    for i, note in enumerate(sheet.notes):
                        if note.rect.collidepoint(event.pos):
                            # 좌클릭 : 클릭한 음표로 입력커서 이동
                            if event.button == 1:
                                offset_note_input = i + 1
                                print(f'[PIANOTE] 음표 입력커서 이동. offset: {music_sheets.index(sheet)}-{offset_note_input}')
                                break
                            # 우클릭 : 클릭한 음표 삭제
                            if event.button == 3:
                                print(f'[PIANOTE] 음표 삭제: {note.get_pitch()}({note.get_note()}th)')
                                sheet.notes.remove(note)
                                # 음표를 지우다 이전 오선지로 돌아가면
                                if len(music_sheets) > 1 and len(sheet.notes) < 2:
                                    music_sheets.remove(sheet)
                                    sheet = music_sheets.__getitem__(-1)
                                    offset_note_input = len(sheet.notes) - 1
                                break
                            # 휠업(4) : 음표 길어짐
                            tmp = sheet.notes.pop(i)
                            th = tmp.get_note()
                            if event.button == 5:
                                print(f'[PIANOTE] 음표({tmp.get_pitch()}) note 변경: {th}분음표 →', end=' ')
                                if th < 9:
                                    th = int(th * 2)
                                print(f'{th}분음표')
                            # 휠다운(5) : 음표 짧아짐
                            if event.button == 4:
                                print(f'[PIANOTE] 음표({tmp.get_pitch()}) note 변경: {th}분음표 →', end=' ')
                                if th > 2:
                                    th = int(th / 2)
                                print(f'{th}분음표')
                            tmp.set_note(th)
                            tmp.set_image()
                            tmp.draw_note(tmp.X)
                            sheet.notes.insert(i, tmp)


            # 키보드 값 입력
            if event.type == pygame.TEXTINPUT:
                # 왼손
                if event.text.upper() in gui_piano.left_dict:
                    input_pitch = gui_piano.left_dict[event.text.upper()]
                    # 음 출력
                    if gui_piano.left_dict[event.text.upper()][1] == 's':
                        index = black_pitches.index(gui_piano.left_dict[event.text.upper()])
                        BLACK_SOUNDS[index].play(0, SOUND_PLAY_SEC) # 소리 출력
                        gui.active_blacks.append([index, 30]) # 효과 출력
                    else:
                        index = white_pitches.index(gui_piano.left_dict[event.text.upper()])
                        WHITE_SOUNDS[index].play(0, SOUND_PLAY_SEC)
                        gui.active_whites.append([index, 30])
                # 오른손
                if event.text.upper() in gui_piano.right_dict:
                    input_pitch = gui_piano.right_dict[event.text.upper()]
                    # 음 출력
                    if gui_piano.right_dict[event.text.upper()][1] == 's':
                        index = black_pitches.index(gui_piano.right_dict[event.text.upper()])
                        BLACK_SOUNDS[index].play(0, SOUND_PLAY_SEC)
                        gui.active_blacks.append([index, 30])
                    else:
                        index = white_pitches.index(gui_piano.right_dict[event.text.upper()])
                        WHITE_SOUNDS[index].play(0, SOUND_PLAY_SEC)
                        gui.active_whites.append([index, 30])
                # 입력한 음 저장, Note 객체 생성!!
                if (input_pitch != ""):
                    print(f'[PIANOTE] 음표 입력: {input_pitch}')
                    new_note = nt.Note(screen, input_pitch, 4) # default : 4분음표
                    sheet.notes.insert(offset_note_input, new_note) # 오선지에 음표 추가
                    offset_note_input += 1


            # 키보드 키 이벤트
            if event.type == pygame.KEYDOWN:
                # 상/하/좌/우 키 : 옥타브 조절
                if event.key == pygame.K_RIGHT:
                    if gui_piano.right_oct < 5:
                        gui_piano.set_right_oct(gui_piano.get_right_oct() + 1)
                        print(f"[PIANOTE] 오른손 옥타브 : {gui_piano.get_right_oct()}")
                if event.key == pygame.K_LEFT:
                    if gui_piano.right_oct > 4:
                        gui_piano.set_right_oct(gui_piano.get_right_oct() - 1)
                        print(f"[PIANOTE] 오른손 옥타브 : {gui_piano.get_right_oct()}")
                if event.key == pygame.K_UP:
                    if gui_piano.left_oct < 5:
                        gui_piano.set_left_oct(gui_piano.get_left_oct() + 1)
                        print(f"[PIANOTE] 왼손 옥타브 : {gui_piano.get_left_oct()}")
                if event.key == pygame.K_DOWN:
                    if gui_piano.left_oct > 3:
                        gui_piano.set_left_oct(gui_piano.get_left_oct() - 1)
                        print(f"[PIANOTE] 왼손 옥타브 : {gui_piano.get_left_oct()}")
                gui_piano.update_keys_set()
                # delete 키 : 마지막 음표 삭제
                if event.key == pygame.K_BACKSPACE:
                    if sheet.notes:
                        removed_note = sheet.notes.pop()
                        print(f'[PIANOTE] 음표 삭제: {removed_note.get_pitch()}({removed_note.get_note()}th)')
                        # 음표를 지우다 이전 오선지로 돌아가면
                        if len(music_sheets) > 1 and len(sheet.notes) < 2:
                            music_sheets.remove(sheet)
                            sheet = music_sheets[-1]
                            offset_note_input = len(sheet.notes) - 1
                # Space 바 : 악보 재생
                if event.key == pygame.K_SPACE:
                    print("[PIANOTE] 악보 재생 중..", end=' ')
                    for play_sheet in music_sheets:
                        play_sheet.draw_sheet(WIDTH)
                        play_step = 0
                        for note in play_sheet.notes:
                            # 음표 오선지에 그리기
                            play_step = draw_step_note(note, play_step)
                            pygame.display.flip()

                            note.get_sound().play(0, SOUND_PLAY_SEC)
                            time = int(1000 / (note.get_note() / 4)) # 4/4박자에서 4분음표 1초에 1개
                            pygame.time.delay(time)

                    print("재생 완료")

                # ESC 키 : 프로그램 종료
                if event.key == pygame.K_ESCAPE:
                    print("\n[PIANOTE] Pianote GUI 종료")
                    run = False


        # 악보 그리기
        if sheet.notes:
            step = 0
            for note in sheet.notes:
                step = sheet.draw_step_note(note, step)

                # 오선지 밖으로 넘으면 오선지 다시 그림
                if note.X > WIDTH - note.WIDTH:
                    sheet.notes.remove(note) # 이전 오선지에 넘어간 노트를 제거하고
                    new_sheet = nt.Sheet(screen, 'treble', None)
                    new_sheet.notes.append(note) # 새로운 오선지에 넘어간 노트를 넘겨줌
                    music_sheets.append(new_sheet)

                    offset_note_input = 1

                    step = 0
                    note.set_X(10)
                    step = note.draw_note(step)

        pygame.display.flip()

    # 저장된 노트 정보
    saved_notes = []
    for sheet in music_sheets:
        notes_list = sheet.notes
        all_notes = []
        for note in notes_list:
            all_notes.extend([note.get_pitch(), note.get_note()])
        saved_notes.append(all_notes)

    print('\n-------------------------------')
    print('입력한 음표 정보')
    for i in range(len(saved_notes)):
        print(f'sheet{i} {saved_notes[i]}')
    print('-------------------------------\n')

#----- 3. 종료 후 악보 저장하기------------------------------------------------------------------------------------------#
    save_filename = input_filename[:-1]  # 파일명
    explain_txt = "[END] 저장할 악보 파일명 입력후 Enter (저장없이 종료 : 빈칸으로 Enter)"
    save_filename = input_text_gui(screen, medium_font_kor, explain_txt, save_filename)

    if save_filename[:-1]:  # 아무것도 입력하지 않고 Enter 누르면 "\r"
        create_score = open(f'../scores/{save_filename[:-1]}.csv', 'w', newline='')
        writer = csv.writer(create_score)
        writer.writerows(saved_notes)
        print(f"[END] Pianote 종료. 저장한 악보 파일명 : {save_filename[:-1]}.csv")
    else:
        print("[END] Pianote 종료. 악보 저장 안함.")

    pygame.quit()  # GUI 종료