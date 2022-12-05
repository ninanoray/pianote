import pygame
import piano_lists as pl

# 소리를 출력하는 건반 효과
active_whites = []
active_blacks = []

class PianoGUI:
    MIN_OCT = 3 # 최소 옥타브

    def __init__(self, screen, width, height, font_1, font_2):
        self.screen = screen

        self.WIDTH = width
        self.HEIGHT = height

        self.left_oct = self.MIN_OCT + 1
        self.right_oct = self.MIN_OCT + 2

        self.left_hand = pl.left_hand
        self.right_hand = pl.right_hand
        self.white_labels = pl.white_pitches # 백건
        self.black_labels = pl.black_labels # 흑건

        self.small_font = font_1
        self.real_small_font = font_2

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
    def draw_piano(self):
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
        for i in range(len(active_whites)):
            if active_whites[i][1] > 0:
                j = active_whites[i][0]
                pygame.draw.rect(self.screen, 'green',
                                 [j*white_w, self.HEIGHT-white_h, white_w, white_h], 2, 2)
                active_whites[i][1] -= 1

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
            for q in range(len(active_blacks)):
                if active_blacks[q][0] == i:
                    if active_blacks[q][1] > 0:
                        pygame.draw.rect(self.screen, 'green',
                                         [black_w + (i*white_w) + (skip_count*white_w),
                                          self.HEIGHT-white_h, black_w, black_h], 2, 2)
                        active_blacks[q][1] -= 1
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

        return white_rects, black_rects

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