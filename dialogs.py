import tkinter as tk
def helpApp():
    helpWindow = tk.Toplevel()
    helpWindow.title("O nas ...")
    helpWindow.geometry("300x300")
    content = tk.Label(helpWindow, text = "Wszystko o programie")
    content.grid(row=1, column=1)

def connectWindow():
    connectWindow = tk.Toplevel()
    connectWindow.title("Połącz z serwerem...")
    connectWindow.geometry("600x450")
    label = tk.Label(connectWindow, text = "Wpisz IP serwera:")
    label.pack(side=tk.BOTTOM)