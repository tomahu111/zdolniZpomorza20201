import threading
from tkinter import *
from tkinter.ttk import *
from tkinter import colorchooser
from enum import Enum
import dialogs
class programMode(Enum):
    normal = 0
    client = 1
    server = 2

class ePaintGUI:
    def __init__(self, master):
        master.iconbitmap("img/logo.ico")
        self.mode = programMode.normal
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
        self.style = Style()
        self.style.configure("Padding.TButton", padding=10)
        self.style.configure("CurrentColor.TLabel",
                        padding=10, background=self.colorLabel)

        # obiekty na oknie
        self.currThick = Label(master, text=str(
            self.counter), style="CurrentColor.TLabel")
        self.currThick.grid(row=0, column=1, sticky="W")
        self.thicknessSlider = Scale(master, from_=1, to=10,
                                     command=self.updateThick, variable=IntVar(), value=1)
        self.thicknessSlider.grid(row=0, column=3)

        # resetowanie canva
        self.resetButton = Button(
            master, text="reset", command=self.resetCanva)
        self.resetButton.grid(row=0, column=6)

        # ustawienie canva
        self.canva = Canvas(master, background="#FEFEFE", cursor="pencil")
        self.canva.grid(row=1, column=0, columnspan=100, sticky="nsew")

        self.bindEvents()
        self.createMenu(master)
        

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
    def createMenu(self,root):
        # Create menu
        menu = Menu(root)
        # Menu pliku
        filemenu = Menu(menu,tearoff=0)
        filemenu.add_command(label="Otwórz")
        filemenu.add_command(label="Połącz z serwerem", command=dialogs.connectWindow)
        filemenu.add_command(label="Uruchom serwer", command=dialogs.serverManWindow)
        filemenu.add_command(label="Zapisz")
        filemenu.add_command(label="Drukuj")
        filemenu.add_command(label="Wyślij faxem")
        filemenu.add_command(label="Wyślij e-mailem")
        filemenu.add_separator()
        filemenu.add_command(label="Ustawienia")
        filemenu.add_command(label="Wyjście", command=root.quit())
        menu.add_cascade(label="Plik", menu=filemenu)
        # Menu edycji
        editmenu = Menu(menu,tearoff=0)
        editmenu.add_command(label="Kopiuj")
        editmenu.add_command(label="Wklej")
        editmenu.add_command(label="Obróć w prawo")
        editmenu.add_command(label="Obróć w lewo")
        editmenu.add_command(label="Odbij w poziomie", command=lambda: self.rotateObjects())
        editmenu.add_command(label="Odbij w pionie")
        editmenu.add_command(label="Resetuj ustawienia pędzla")
        editmenu.add_command(label="Wyczyść")

        menu.add_cascade(label="Edycja", menu=editmenu)
        # Menu pomocy
        helpmenu = Menu(menu, tearoff=0)
        helpmenu.add_command(label="O aplikacji", command=dialogs.helpApp)
        menu.add_cascade(label="Pomoc", menu=helpmenu)
        self.master.config(menu=menu)

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

        self.style.configure("CurrentColor.TLabel",
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

    # Zmiana funkcjonalności programu
    def unbindEvents(self):
        self.canva.unbind("<Button-1>")
        self.canva.unbind("<B1-Motion>")
    def bindEvents(self):
        self.canva.bind("<Button-1>", self.m1click)
        self.canva.bind("<B1-Motion>", self.m_move)
    def changeMode(self,mode):
        if mode == programMode.client:
            self.unbindEvents()
            # uruchom wątek do nasłuchiwania


        elif mode == programMode.server or mode == programMode.normal:
            self.bindEvents()

    def rotateObjects(self):
        objs = self.getAllIDs()
        for o in objs:
            self.canva.

    def getAllIDs(self):
        return self.canva.find_all()

myWindow = None
def initGui():
    root = Tk()
    myWindow = ePaintGUI(root)
    myWindow.resetCanva()
    root.mainloop()


