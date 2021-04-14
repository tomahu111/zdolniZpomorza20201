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
    connectWindow.geometry("100x50")
    label = tk.Label(connectWindow, text = "Wpisz IP serwera:")
    label.pack(side=tk.BOTTOM)

    textinput = tk.Text(connectWindow, height=10, width=40)
    textinput.pack()

    connectbutton = tk.Button(connectWindow, hight=10, width=20, text="Połącz")
    connectbutton.pack()