import pygame
from tkinter import * #gui
import time

pygame.init()

# gui 창 만들기
root = Tk()
root.title("piano")
root.geometry('1700x700+0+0')

frame = Frame(root, bg="medium purple", bd=20, relief=RIDGE)
frame.grid()

frame1 = Frame(frame, bg="medium purple", bd=20, relief=RIDGE)
frame1.grid()
frame3 = Frame(frame, bg="white", relief=FLAT)
frame3.grid()

str1 = StringVar()
str1.set("Just Like Music")
Date1 = StringVar()
Time1 = StringVar()

Date1.set(time.strftime("%Y-%m-%d"))
Time1.set(time.strftime("%H:%M/%S"))

#======================백건 소리=============================
def value_note_Click(note):
      str1.set(note)
      sound = pygame.mixer.Sound(note + ".wav")
      sound.play()
#======================백건 소리=============================
def pressKey(event):
      if (event.char == 'a'):
            value_note_Click("C3")

      elif (event.char == 's'):
            value_note_Click("D3")

      elif (event.char == 'd'):
            value_note_Click("E3")

      elif (event.char == 'f'):
            value_note_Click("F3")

      elif (event.char == 'g'):
            value_note_Click("G3")

      elif (event.char == 'h'):
            value_note_Click("A3")

      elif (event.char == 'j'):
            value_note_Click("B3")

      elif (event.char == 'k'):
            value_note_Click("C4")

      elif (event.char == 'l'):
            value_note_Click("D4")

      elif (event.char == ';'):
            value_note_Click("E4")

      elif (event.char == "'"):
            value_note_Click("F4")

      elif (event.char == 'w'):
            value_note_Click("C3s")

      elif (event.char == 'e'):
            value_note_Click("D3s")

      elif (event.char == 't'):
            value_note_Click("F3s")

      elif (event.char == 'y'):
            value_note_Click("G3s")

      elif (event.char == 'u'):
            value_note_Click("A3s")

      elif (event.char == 'o'):
            value_note_Click("C4s")

      elif (event.char == 'p'):
            value_note_Click("D4s")

      elif (event.char == ']'):
            value_note_Click("F4s")
#=======================Label with Title============================

Label(frame1, text="Piano",font=('arial', 25, 'bold'), padx=8, pady=8, bd=5, bg="medium purple",
      fg="white", justify=CENTER).grid(row=0, column=0, columnspan=4)

#=================================제목==================================

txtDisplay = Entry(frame1, textvariable=str1, font=('arial', 18, 'bold'), bd=34, bg="medium purple",
                   fg="white", justify=CENTER).grid(row=1, column=0)
txtDate = Entry(frame1, textvariable=Date1, font=('arial', 18, 'bold'), bd=34, bg="medium purple",
                   fg="white", justify=CENTER).grid(row=1, column=1)
txtTime = Entry(frame1, textvariable=Time1, font=('arial', 18, 'bold'), bd=34, bg="medium purple",
                   fg="white", justify=CENTER).grid(row=1, column=2)

#===============================백건 버튼====================================
ButtonWidth = 3
ButtonHeight = 8
'''
class Btn:
      def __init__(self, note, col):
            self.note = note
            self.col = col
            self.btn = Button(frame3, width=ButtonWidth, height=ButtonHeight, text=note, font=('arial',25,'bold'),
                              bd=5, bg="white", command=lambda :value_note_Click(note), fg="black")
            self.btn.grid(row=1, column=col)
'''
class Btn:
      def __init__(self, note, col):
            self.note = note
            self.col = col
            self.btn = Button(frame3, width=ButtonWidth, height=ButtonHeight, text="\n\n\n"+note, font=('arial',25,'bold'),
                              bd=5, bg="white", command=lambda :value_note_Click(note), fg="black")
            self.btn.grid(row=0, column=col)

notes = ["C3", "D3", "E3", "F3", "G3", "A3", "B3", "C4", "D4", "E4",
         "F4", "G4", "A4", "B4", "C5", "D5", "E5", "F5", "G5", "A5", "B5"]

buttons = [Btn(note, i+1) for i, note in enumerate(notes, len(notes))]


#=================================흑건 버튼==================================

SharpButtonWidth = 3
SharpButtonHeight = 4
BlankSpaceWidth = 9

class Btn_Sharp:
      def __init__(self, note, col):
            self.note = note
            self.col = col

            if (note is not None):
                  self.btn = Button(frame3, width=SharpButtonWidth, height=SharpButtonHeight,
                                    text=note, font=('arial',25,'bold'), bd=5, bg="black",
                                    command=lambda :value_note_Click(note.replace('#','s')), fg="white")
                  self.btn.place(x = 76*col - 1560, y=0)
            else:
                  self.btn = Button(frame3, width=BlankSpaceWidth, height=0,
                                    state=DISABLED, relief=FLAT, bg="white")
                  self.btn.place(x = 76*col - 1560, y=0)

notes_sharp = ["C3#", "D3#", None, "F3#", "G3#", "A3#", None, "C4#", "D4#", None,
               "F4#", "G4#", "A4#", None, "C5#", "D5#", None, "F5#", "G5#", "A5#"]

buttons_sharp = [Btn_Sharp(note, i+1) for i, note in enumerate(notes_sharp, len(notes_sharp))]


root.bind("<KeyPress>", pressKey) # 키보드 입력 명령어

root.mainloop()