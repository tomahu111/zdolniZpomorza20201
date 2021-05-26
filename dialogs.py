import tkinter as tk
from tkinter import messagebox
from enum import Enum

from PIL import ImageTk, Image
from epserver import *

import gui

server_started=False

def messagewindow(type, title, message):
    if type == msgboxtype.info:
        messagebox.showinfo(title=title, message=message)
    elif type == msgboxtype.warning:
        messagebox.showwarning(title=title,message=message)
    elif type == msgboxtype.error:
        messagebox.showerror(title=title,message=message)
    else:
        raise Exception("Nie podano typu wiadomości dla messagewindow")

class msgboxtype(Enum):
    info = 1
    warning = 2
    error = 3

def helpApp():
    helpWindow = tk.Toplevel()
    helpWindow.resizable(False,False)
    helpWindow.title("O nas ...")
    helpWindow.geometry("450x300")

    contentframe = tk.Frame(helpWindow)
    contentframe.pack(side=tk.TOP)
    #icon = ImageTk.PhotoImage(Image.open("img/logo.png"))
    #iconpanel = tk.Label(contentframe, image=icon)
    #iconpanel.pack(side=tk.TOP)

    title = tk.Label(contentframe, text = "ePaint",wraplength=400, justify="left", font=('Segoe UI',24))
    titledesc = tk.Label(contentframe, text = "Program do rysowania z funkcjonalnością udostępniania rysunku innym użytkownikom w sieci.",wraplength=400, justify="left", font=('Arial',12))
    title.pack(side=tk.TOP, padx=10,pady=10)
    titledesc.pack(side=tk.TOP, padx=10,pady=10)

    creditframe = tk.Frame(contentframe)
    creditframe.pack(side=tk.TOP)
    text1 = tk.Label(creditframe,text="Program stworzony przez:",font=('Arial',12)).pack(side=tk.TOP)

    with open("credits.txt", "r", encoding="utf-8") as credits:
        for line in credits:
            text = tk.Label(creditframe,text=line).pack(side=tk.TOP)

    

# Zarządzanie połączeniem
class serverStatusUI:
    statusLabel = None
    startButton = None

    @staticmethod
    def toggleStatus(status):
        try:
            if status == True:
                serverStatusUI.statusLabel.config(text="Uruchomony")
                serverStatusUI.startButton.config(text="Zatrzymaj Serwer")
            else:
                serverStatusUI.statusLabel.config(text="Wyłączony")
                serverStatusUI.startButton.config(text="Uruchom Serwer")
        except:
            print("Próbowano zmienić status dialogu który jeszcze nie istnieje!")

def connectWindow():
    connectWindow = tk.Toplevel()
    connectWindow.resizable(False,False)
    connectWindow.title("Połącz z serwerem...")
    connectWindow.geometry("200x70")

    label = tk.Label(connectWindow, text = "Wpisz IPv4 serwera:")
    textinput = tk.Entry(connectWindow)
    textinput.insert(tk.END, '192.168.16.22')
    connectbutton = tk.Button(connectWindow, height=10, width=20, text="Połącz", command=lambda: connectToServer(textinput.get()))

    label.pack(side=tk.TOP)
    textinput.pack(side=tk.TOP)
    connectbutton.pack(side=tk.TOP)

def startServer():
    global server_started
    from gui import myWindow
    print("Starting...")
    myWindow.changeMode(programMode.server)
    if(server_started):
        serverStatusUI.statusLabel['text']='Wyłączony'
        server_started=False
    else:
        serverStatusUI.statusLabel['text']='Włączony'
        server_started=True
    
def serverManWindow():
    serverWindow = tk.Toplevel()
    serverWindow.resizable(False,False)
    serverWindow.title("Zarządzanie serwerem")
    serverWindow.geometry("200x70")

    label = tk.Label(serverWindow, text="Status serwera:")
    serverStatusUI.statusLabel = tk.Label(serverWindow, text="Wyłączony")
    serverStatusUI.startButton = tk.Button(serverWindow, height=10, width=20, text="Uruchom serwer", command=startServer)

    label.pack(side=tk.TOP)
    serverStatusUI.statusLabel.pack(side=tk.TOP)
    serverStatusUI.startButton.pack(side=tk.BOTTOM)


def infowindow(text):
    infowindow = tk.Toplevel()
    infowindow.resizable(False,False)
    infowindow.geometry("150x50")

    label = tk.Label(infowindow, text=text)
    label.pack(side=tk.TOP)



def connectToServer(ip):
    import ipaddress
    try:
        a = ipaddress.ip_address(ip)
    except:
        messagewindow(msgboxtype.error, title="Serwer", message="Niepoprawny adres IP")
        return -1
    #infowindow("Uruchamianie serwera...")
    from gui import myWindow

    # Przygotuj do polaczenia

    # Reset canva
    myWindow.resetCanva()
    # Zmien tryb na taki gdzie nie mozna rysowac
    myWindow.changeMode(gui.programMode.client)
    # Tworzymy objekt epclient, dopóki istnieje program będzie odbierał informacje
    clientprog = Epclient2(ip, guiInstance=myWindow)
    clientprog.start()
