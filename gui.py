from tkinter import *
import os
import wrong


def start(var, file, tuning):
    var.set(wrong.disp(file, 44100, tuning))


class GUI:
    def __init__(self, master):
        self.master = master
        master.title("HE HAS MASTERED PITCH")

        self.label = Label(master, text="HE HAS MASTERED PITCH")
        self.label.config(font=('Courier', 44))
        self.label.pack()

        variable = StringVar(master)
        # variable.set("-- choose file --")
        menu = OptionMenu(master, variable, *[i for i in os.listdir('.') if i.endswith('.wav')])
        menu.pack()

        note = StringVar(master)
        Label(master, text="Enter Tuning Note: ").pack()
        self.tuningnote = Entry(master, textvariable=note)
        self.tuningnote.pack()

        outp = StringVar(master)
        printing = Label(master, textvariable=outp)
        printing.config(font=('Courier', 10))
        printing.pack()

        self.go = Button(master, text="Start",
                         command=lambda: start(outp, variable.get(), note.get() if note.get() else None))
        self.go.pack()

        # for file in os.listdir('.'):
        # if file.endswith('.wav'):
        # label = Label(master, text=wrong.disp("notes.wav", 44100, "A#3"))
        # label.config(font=('Courier', 30))
        # label.pack()


root = Tk()
gui = GUI(root)
root.mainloop()