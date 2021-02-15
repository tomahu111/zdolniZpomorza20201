from tkinter import *
def helpApp():
    helpWindow = Toplevel()
    helpWindow.title("O nas ...")
    helpWindow.geometry("300x300")
    content = Label(helpWindow, text = "Wszystko o programie")
    content.grid(row=1, column=1)