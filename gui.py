import threading
import tkinter as tk
from tkinter.ttk import *
from tkinter import colorchooser
from enum import Enum
from typing import Tuple
import dialogs
import operator
import epserver
import socket
import pickle
import queue
import time

buffor=[]
from sys import platform
class programMode(Enum):
    normal = 0
    client = 1
    server = 2

class ePaintGUI:
    def __init__(self, master):
        if platform == "win32":
            master.iconbitmap("img/logo.ico")
        self.mode = programMode.normal
        self.master = master
        self.col = "#000000"
        self.pos1 = (0,0)
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
                                     command=self.updateThick, variable=tk.IntVar(), value=1)
        self.thicknessSlider.grid(row=0, column=3)

        # resetowanie canva
        self.resetButton = Button(
            master, text="reset", command=self.resetCanva)
        self.resetButton.grid(row=0, column=6)

        # ustawienie canva
        self.canva = tk.Canvas(master, background="#FEFEFE", cursor="pencil")
        self.canva.grid(row=1, column=0, columnspan=100, sticky="nsew")
        self.m1depressed = False
        
        # Serwer
        self.sendingQueue = queue.Queue()

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

        def createColorButton(img,posx,posy,color):
            colorBtn = tk.Button(self.master, text = "", image=fakeimg, anchor = "w", width = 15, height=15, background=color,activebackground = "#FFFFFF", relief = "solid", compound="c",borderwidth=1,command=lambda: self.chooseColor(color))
            self.canva.create_window(posx,posy, anchor="nw", window=colorBtn)
            colorBtn.image = fakeimg

        fakeimg = tk.PhotoImage(width=1, height=1)
        createColorButton(fakeimg,10,10,"#000000")
        createColorButton(fakeimg,10,35,"#FF0000")
        createColorButton(fakeimg,10,60,"#00FF00")
        createColorButton(fakeimg,10,85,"#0000FF")
        createColorButton(fakeimg,10,110,"#FFFFFF")
        
    # zmiana koloru
    def createMenu(self,root):
        # Create menu
        menu = tk.Menu(root)
        # Menu pliku
        filemenu = tk.Menu(menu,tearoff=0)
        filemenu.add_command(label="Otwórz")
        filemenu.add_command(label="Połącz z serwerem", command=dialogs.connectWindow)
        filemenu.add_command(label="Uruchom serwer", command=dialogs.serverManWindow)
        filemenu.add_command(label="Zapisz")
        filemenu.add_command(label="Drukuj")
        filemenu.add_command(label="Wyślij faxem")
        filemenu.add_command(label="Wyślij e-mailem")
        filemenu.add_separator()
        #filemenu.add_command(label="Ustawienia")
        filemenu.add_command(label="Wyjście", command=root.quit())
        menu.add_cascade(label="Plik", menu=filemenu)
        # Menu edycji
        editmenu = tk.Menu(menu,tearoff=0)
        editmenu.add_command(label="Obróć w prawo")
        editmenu.add_command(label="Obróć w lewo")
        editmenu.add_command(label="Odbij w poziomie", command=lambda: self.mirrorObjects(0))
        editmenu.add_command(label="Odbij w pionie", command=lambda: self.mirrorObjects(1))
        editmenu.add_command(label="Resetuj ustawienia pędzla", command=lambda: self.resetBrush())
        editmenu.add_command(label="Wyczyść")

        menu.add_cascade(label="Edycja", menu=editmenu)
        # Menu pomocy
        helpmenu = tk.Menu(menu, tearoff=0)
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
    def freeDraw(self,pos, thickness=1, color="#000000"):
        
        self.canva.create_oval(pos[0]-thickness, pos[1]-thickness, pos[0]+thickness,
                               pos[1]+thickness, fill=color, outline=color)

    def draw2points(self, pos2, pos1, thickness=1,color="#000000"):
        posDiff = tuple(map(operator.sub, pos2, pos1))
        maxnum = max(abs(posDiff[0]), abs(posDiff[1]))
        for i in range(maxnum):
            newPos = ( int(pos1[0] + (float(i)/maxnum * posDiff[0])), int(pos1[1] + (float(i)/maxnum * posDiff[1])) )
            self.freeDraw(newPos, thickness=thickness, color=color)

    def m1down(self,event):
        self.m1depressed = True
        # Zapisz pozycje poprzedniego klikniecia
        self.pos1 = (event.x, event.y)
        self.freeDraw(self.pos1, thickness=self.counter, color=self.col)
    def m1up(self,event):
        self.m1depressed = False
    def m1move(self,event):
        if self.m1depressed == True:
            pos = (event.x, event.y)
            posDiff = tuple(map(operator.sub, self.pos1, pos))
            maxnum = max(abs(posDiff[0]), abs(posDiff[1]))
            self.draw2points(pos, self.pos1, thickness=self.counter, color=self.col)
            # Wyslij do wszystkich klientow starą i nową pozycje
            # Format danych: [(pos1), (pos2), thick, color]
            data = [pos, self.pos1, self.counter, self.col]
            if self.mode == programMode.server:
                self.packAndSend(data)
            self.pos1 = (event.x, event.y)

    def packAndSend(self,data):
        # pickle the data
        data = pickle.dumps(data)
        self.server.prepMessage(data,isEncoded=True)
    # Zmiana funkcjonalności programu
    def unbindEvents(self):
        self.canva.unbind("<Button-1>")
        self.canva.unbind("<B1-Motion>")
    def bindEvents(self):
        self.canva.bind("<Button-1>", self.m1down)
        self.canva.bind("<B1-Motion>", self.m1move)
        self.canva.bind("<ButtonRelease-1>", self.m1up)

    def mirrorObjects(self,mode):
        width = self.canva.winfo_screenwidth()
        height = self.canva.winfo_screenheight()
        objs = self.getAllIDs()
        for o in objs:
            coords = self.canva.coords(o)
            if len(coords)>3:
                if mode == 0: # W pionie
                    x1 = width - coords[0]
                    roznica = coords[0] - coords[2]
                    self.canva.coords(o, x1, coords[1], x1+roznica, coords[3])
                elif mode == 1: # W poziomie
                    y1 = height - coords[1]
                    roznica = coords[1] - coords[3]
                    self.canva.coords(o, coords[0], y1 , coords[2], y1+roznica)
    def getAllIDs(self):
        return self.canva.find_all()

    def changeMode(self, mode):
        self.mode = mode
        if mode in programMode:
            if mode == programMode.client:
                self.unbindEvents()
            elif mode == programMode.server:
                self.bindEvents()
                print("uruchamianie serwera")
                # uruchom serwer (utworzenie obiektu UberSocket)
                self.server = epserver.UberSocket(ip=socket.gethostname())
                self.server.start()
                # svThread = threading.Thread(target=self.serverSendThread)
                # svThread.start()
    def drawFromData(self, pos1, pos2, thickness, color):
        posDiff = tuple(map(operator.sub, pos1, pos2))
        maxnum = max(abs(posDiff[0]), abs(posDiff[1]))
        for i in range(maxnum):
            newPos = ( int(pos1[0] + (float(i)/maxnum * posDiff[0])), int(pos1[1] + (float(i)/maxnum * posDiff[1])) )
            self.freeDraw(newPos, thickness=thickness, color=color)
    def resetBrush(self):
        self.updateThick(1)
        self.thicknessSlider.set(1)
        self.chooseColor("#000000")

myWindow = None
def initGui():
    global myWindow
    root = tk.Tk()
    myWindow = ePaintGUI(root)
    myWindow.resetCanva()
    root.mainloop()


