import threading
from tkinter import *
from tkinter.ttk import *
from tkinter import colorchooser
from menus import createMenu
import platform
import socket


# class okna z rysowaniem

class ePaintGUI:
    def __init__(self, master):
        self.master = master
        self.col = "#000000"
        self.x1, self.x2 = 0, 0
        self.x, self.y = 1, 1
        self.counter = 1
        self.colorLabel = "white"
        # zmienne
        # global counter, blackButton, redButton, greenButton, blueButton, canva

        # ustawienie główne okna
        master.title('ePaint')
        master.rowconfigure(1, weight=1)
        master.columnconfigure(4, weight=1)
        style = Style()
        style.configure("Padding.TButton", padding=10)
        style.configure("CurrentColor.TLabel",
                        padding=10, background=self.colorLabel)

        # obiekty na oknie
        self.currThick = Label(root, text=str(
            self.counter), style="CurrentColor.TLabel")
        self.currThick.grid(row=0, column=1, sticky="W")
        self.thicknessSlider = Scale(root, from_=1, to=10,
                                     command=self.updateThick, variable=IntVar(), value=1)
        self.thicknessSlider.grid(row=0, column=3)

        # resetowanie canva
        self.resetButton = Button(
            master, text="reset", command=self.resetCanva)
        self.resetButton.grid(row=0, column=6)

        # ustawienie canva
        self.canva = Canvas(master, background="#FEFEFE", cursor="pencil")
        self.canva.grid(row=1, column=0, columnspan=100, sticky="nsew")

    def updateThick(self, skala):
        self.counter = int(float(skala))
        self.currThick.config(text=str(self.counter))

    # resetowanie funkcji
    def resetCanva(self):
        self.canva.delete('all')
        self.counter = 1
        self.thicknessSlider.set(1)
        self.currThick.config(text=str(self.counter))
        self.blackButton = self.canva.create_rectangle(
            10, 10, 30, 30, fill="#000000")
        self.redButton = self.canva.create_rectangle(
            10, 35, 30, 55, fill="#FF0000")
        self.greenButton = self.canva.create_rectangle(
            10, 60, 30, 80, fill="#00FF00")
        self.blueButton = self.canva.create_rectangle(
            10, 85, 30, 105, fill="#0000FF")
        self.whiteButton = self.canva.create_rectangle(
            10, 110, 30, 130, fill="#FFFFFF")
        self.customColorButton = self.canva.create_oval(
            10, 135, 30, 155, fill="#000000", outline="#000000")

        self.chooseColor("#000000")

        self.canva.tag_bind(self.blackButton, "<Button-1>",
                            lambda w: self.chooseColor("#000000"))
        self.canva.tag_bind(self.redButton, "<Button-1>",
                            lambda w: self.chooseColor("#FF0000"))
        self.canva.tag_bind(self.greenButton, "<Button-1>",
                            lambda w: self.chooseColor("#00FF00"))
        self.canva.tag_bind(self.blueButton, "<Button-1>",
                            lambda w: self.chooseColor("#0000FF"))
        self.canva.tag_bind(self.whiteButton, "<Button-1>",
                            lambda w: self.chooseColor("#FFFFFF"))
        self.canva.tag_bind(self.customColorButton, "<Button-1>",
                            lambda w: self.chooseColor("custom"))

    # zmiana koloru
    def chooseColor(self, newColor):
        self.col
        if newColor == "custom":
            newColor = colorchooser.askcolor()[1]
            if newColor is None:
                return
        # Wybor koloru tekstu
        self.col = newColor
        red = int(self.col[1:3], 16)
        green = int(self.col[3:5], 16)
        blue = int(self.col[5:7], 16)
        if (red*0.299 + green*0.587 + blue*0.144) > 186:
            textcolor = "black"
        else:
            textcolor = "white"

        style.configure("CurrentColor.TLabel",
                        background=self.col, foreground=textcolor)

    # rysowanie dowolne na canva
    def freeDraw(self, thickness=1, color="#000000"):
        self.canva.create_oval(self.x-thickness, self.y-thickness, self.x+thickness,
                               self.y+thickness, fill=color, outline=color)

    def m1click(self, event):
        self.x1 = event.x
        self.y1 = event.y
        self.freeDraw(thickness=self.counter, color=self.col)

    def m_move(self, event):
        xdiff = self.x1-event.x
        ydiff = self.y1-event.y
        maxnum = max(abs(xdiff), abs(ydiff))
        for i in range(maxnum):
            self.x = int(event.x + (float(i)/maxnum * xdiff))
            self.y = int(event.y + (float(i)/maxnum * ydiff))
            self.freeDraw(thickness=self.counter, color=self.col)
        self.x1 = event.x
        self.y1 = event.y
        print(self.x1, self.y1, self.x, self.y)


root = Tk()
menu = createMenu(root)
root.config(menu=menu)
style = Style()


# funkcja główna


def main():
    global myWindow
    myWindow = ePaintGUI(root)
    myWindow.resetCanva()

    myWindow.canva.bind("<Button-1>", myWindow.m1click)
    myWindow.canva.bind("<B1-Motion>", myWindow.m_move)


# definiowanie połaczenia

PORT = 37234
BUFFER = 1024
hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname)


def hostLabel():
    global HOST
    print(HOST)


def hostMain():
    hostLabel()


main_thread = threading.Thread(target=main)
main_thread.start()

host_thread = threading.Thread(target=hostMain)
host_thread.start()

root.mainloop()
