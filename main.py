from tkinter import *
from menus import createMenu
import socket


root = Tk()
root.title("Nowa aplikacja")
#root.geometry("300x300")
root.state("zoomed")


root.rowconfigure(1, weight=1)
root.columnconfigure(4, weight=1)

#variables
counter = 1
x1=0
y1=0
col = "#000000"

hostname=socket.gethostname()
HOST=socket.gethostbyname(hostname)

#functions

def increaseThick():
    global counter
    counter=counter+1
    currThick.config(text=str(counter))

def decreaseThick():
    global counter
    if(counter>1):
        counter=counter-1
        currThick.config(text=str(counter))

def chooseColor(newCol):
    global col
    col=newCol
def m1click(event):
    global x1, y1
    x1=event.x
    y1=event.y
def m_move(event):
    global x1, y1, col, counter
    if((abs(x1-event.x) + abs(y1-event.y)) <= counter):
        canva.create_oval(event.x-counter, event.y-counter, event.x+counter, event.y+counter, fill=col, outline=col)
    else:
        canva.create_line(x1, y1, event.x, event.y, fill = col, width=counter*2)
    #canva.create_oval(x1-counter, y1-counter, event.x+counter, event.y+counter, fill=col)
    x1=event.x
    y1=event.y
def resetCanva():
    global counter, blackButton, redButton, greenButton, blueButton, canva
    canva.delete('all')
    counter=1
    currThick.config(text=str(counter))
    blackButton=canva.create_rectangle(10, 10, 30, 30, fill="#000000")
    redButton=canva.create_rectangle(10, 35, 30, 55, fill="#FF0000")
    greenButton=canva.create_rectangle(10, 60, 30, 80, fill="#00FF00")
    blueButton=canva.create_rectangle(10, 85, 30, 105, fill="#0000FF")
    whiteButton=canva.create_rectangle(10, 110, 30, 130, fill="#FFFFFF")
    chooseColor("#000000")
    
    canva.tag_bind(blackButton, "<Button-1>", lambda w: chooseColor("#000000"))
    canva.tag_bind(redButton, "<Button-1>", lambda w: chooseColor("#FF0000"))
    canva.tag_bind(greenButton, "<Button-1>", lambda w: chooseColor("#00FF00"))
    canva.tag_bind(blueButton, "<Button-1>", lambda w: chooseColor("#0000FF"))
    canva.tag_bind(whiteButton, "<Button-1>", lambda w: chooseColor("#FFFFFF"))

#buttons
#blackButton = Button(root, text="black", padx=5, pady=15, command=chooseBlack)
#redButton = Button(root, text="red", padx=5, pady=15, command=chooseRed)
#greenButton = Button(root, text="green", padx=5, pady=15, command=chooseGreen)
#blueButton = Button(root, text="blue", padx=5, pady=15, command=chooseBlue)

mOneButton = Button(root, text="-1", padx=5, pady=15, command=decreaseThick)
pOneButton = Button(root, text="+1", padx=5, pady=15, command=increaseThick)

exitButton = Button(root, text="exit", padx=10, pady=10,
               font=('Arial', 11), command=exit)
resetButton = Button(root, text="reset", padx=10, pady=10, command=resetCanva)

#labels
currThick = Label(root, text=str(counter), font=('Arial', 16), bg="red", padx=10, pady=10)
hostLabel = Label(root, text=str(HOST), padx=20, pady=15)

#canvas
canva = Canvas(root, background = "#FEFEFE")

menu = createMenu(root)
root.config(menu=menu)

#grid
#blackButton.grid(row=0, column=0)
#redButton.grid(row=0, column=1)
#greenButton.grid(row=0, column=2)
#blueButton.grid(row=0, column=3)

mOneButton.grid(row=0, column=0)
currThick.grid(row=0, column=1, sticky="W")
pOneButton.grid(row=0, column=2)

hostLabel.grid(row=0, column=4)

resetButton.grid(row=0, column=6)
exitButton.grid(row=0, column=7)

canva.grid(row=1, column=0, columnspan=100, sticky="nsew")

resetCanva()

#blackButton=canva.create_rectangle(10, 10, 30, 30, fill="#000000")
#canva.tag_bind(blackButton, "<Button-1>", lambda w: chooseColor("#000000"))

#redButton=canva.create_rectangle(10, 35, 30, 55, fill="#FF0000")
#canva.tag_bind(redButton, "<Button-1>", lambda w: chooseColor("#FF0000"))

#greenButton=canva.create_rectangle(10, 60, 30, 80, fill="#00FF00")
#canva.tag_bind(greenButton, "<Button-1>", lambda w: chooseColor("#00FF00"))

#blueButton=canva.create_rectangle(10, 85, 30, 105, fill="#0000FF")
#canva.tag_bind(blueButton, "<Button-1>", lambda w: chooseColor("#0000FF"))



#canva.create_line(0, 0, 300, 600, fill="#00FF00", width=5)

#canva.create_rectangle(20, 50, 40, 80, fill="#FF0000");

canva.bind("<Button-1>", m1click)
canva.bind("<B1-Motion>", m_move)

root.mainloop()
