import tkinter as tk
from tkinter import messagebox
from enum import Enum

def messagewindow(type, title, message):
    if type == msgboxtype.info:
        messagebox.showinfo(title=title, message=message)
    elif type == msgboxtype.warning:
        messagebox.showwarning(title=title,message=message)
    elif type == msgboxtype.error:
        messagebox.showerror(title=title,message=message)

class msgboxtype(Enum):
    info = 1
    warning = 2
    error = 3

def helpApp():
    helpWindow = tk.Toplevel()
    helpWindow.title("O nas ...")
    helpWindow.geometry("300x300")
    content = tk.Label(helpWindow, text = "Wszystko o programie")
    content.grid(row=1, column=1)

# Zarządzanie połączeniem
class serverStatusUI:
    running = False
    statusLabel = None
    startButton = None

    @staticmethod
    def toggleStatus():
        serverStatusUI.running = not serverStatusUI.running
        try:
            print("zamiana")
            if serverStatusUI == True:
                print("1")
                statusLabel.config(text="Uruchomony")
                startButton.config(text="Zatrzymaj Serwer")
            else:
                statusLabel.config(text="Wyłączony")
                startButton.config(text="Uruchom Serwer")
        except:
            print("Próbowano zmienić status dialogu który jeszcze nie istnieje!")

def connectWindow():
    connectWindow = tk.Toplevel()
    connectWindow.resizable(False,False)
    connectWindow.title("Połącz z serwerem...")
    connectWindow.geometry("200x70")

    label = tk.Label(connectWindow, text = "Wpisz IPv4 serwera:")
    textinput = tk.Entry(connectWindow)
    connectbutton = tk.Button(connectWindow, height=10, width=20, text="Połącz")

    label.pack(side=tk.TOP)
    textinput.pack(side=tk.TOP)
    connectbutton.pack(side=tk.TOP)

def startServer():
    import epserver
    epserver.setup() # Bez argumentow oznacza automatyczne uzyskanie ip oraz domyslny port: 37234
    serverStatusUI.toggleStatus()
    if epserver.start() == False:
        print("Serwer jest już uruchomiony!")
    else:
        pass


        

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





def connect(ip):
    import ipaddress
    try:
        a = ipaddress.ip_address(ip)
    except:
        messagewindow(msgboxtype.error, title="Serwer", message="Niepoprawny adres IP")
        return -1
    import epserver
    infowindow("Uruchamianie serwera...")
    epserver.setup(ip=ip)
    epserver.start()