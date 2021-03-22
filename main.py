from tkinter import *
from tkinter.ttk import *
from tkinter import colorchooser
from menus import createMenu
import platform
import socket


root = Tk()
root.iconbitmap("img/logo.ico")
root.title("ePaint")
#root.geometry("300x300")
if platform.system() == "Linux":
    root.attributes('-zoomed', True)
else:
    root.state("zoomed")
    


root.rowconfigure(1, weight=1)
root.columnconfigure(4, weight=1)

#variables
counter = 1
x1=0
y1=0
col = "#000000"

style = Style()
style.configure("Padding.TButton",padding=10)
style.configure("CurrentColor.TLabel", padding=10, background=col)

hostname=socket.gethostname()
HOST=socket.gethostbyname(hostname)

#functions

def updateThick(skala):
    global counter
    counter=int(float(skala))
    currThick.config(text=str(counter))

def chooseColor(newCol):
    global col
    if newCol == "custom":
        newCol = colorchooser.askcolor()[1]
        if newCol is None: return
    # Wybor koloru tekstu
    col = newCol
    red = int(col[1:3],16)
    green = int(col[3:5],16)
    blue = int(col[5:7],16)
    if (red*0.299 + green*0.587 + blue*0.144) > 186: 
        textcolor = "black"
    else: textcolor = "white"

    style.configure("CurrentColor.TLabel", background=col, foreground=textcolor)

def freeDraw(x,y,thickness=1,color="black"):
    canva.create_oval(x-thickness, y-thickness, x+thickness, y+thickness, fill=color, outline=color)
def m1click(event):
    global x1, y1
    x1=event.x
    y1=event.y
    freeDraw(x1,y1,thickness=counter,color=col)
def m_move(event):
    global x1, y1, col, counter
    #TODO jakas klasa do tego?
    xdiff = x1-event.x
    ydiff = y1-event.y
    maxnum = max(abs(xdiff),abs(ydiff))
    for i in range(maxnum):
        x = int(event.x + (float(i)/maxnum * xdiff))
        y = int(event.y + (float(i)/maxnum * ydiff))
        freeDraw(x,y,thickness=counter,color=col)
    x1=event.x
    y1=event.y
def resetCanva():
    global counter, blackButton, redButton, greenButton, blueButton, canva
    canva.delete('all')
    counter=1
    currThick.config(text=str(counter))
    thicknessSlider.set(1)
    blackButton=canva.create_rectangle(10, 10, 30, 30, fill="#000000")
    redButton=canva.create_rectangle(10, 35, 30, 55, fill="#FF0000")
    greenButton=canva.create_rectangle(10, 60, 30, 80, fill="#00FF00")
    blueButton=canva.create_rectangle(10, 85, 30, 105, fill="#0000FF")
    whiteButton=canva.create_rectangle(10, 110, 30, 130, fill="#FFFFFF")
    customColorButton=canva.create_oval(10, 135, 30, 155, fill="#000000", outline="red")
    chooseColor("#000000")
    
    canva.tag_bind(blackButton, "<Button-1>", lambda w: chooseColor("#000000"))
    canva.tag_bind(redButton, "<Button-1>", lambda w: chooseColor("#FF0000"))
    canva.tag_bind(greenButton, "<Button-1>", lambda w: chooseColor("#00FF00"))
    canva.tag_bind(blueButton, "<Button-1>", lambda w: chooseColor("#0000FF"))
    canva.tag_bind(whiteButton, "<Button-1>", lambda w: chooseColor("#FFFFFF"))
    canva.tag_bind(customColorButton, "<Button-1>", lambda w: chooseColor("custom"))

# mOneButton = Button(root, text="-1", padx=5, pady=15, command=decreaseThick)
# pOneButton = Button(root, text="+1", padx=5, pady=15, command=increaseThick)

# exitButton = Button(root, text="exit", padx=10, pady=10,
#                font=('Arial', 11), command=exit)
# resetButton = Button(root, text="reset", padx=10, pady=10, command=resetCanva)


currThick = Label(root, text=str(counter),style="CurrentColor.TLabel")
thicknessSlider = Scale(root,from_=1,to=10,command=updateThick, variable=IntVar(),value=1)

exitButton = Button(root, text="exit", command=exit)
resetButton = Button(root, text="reset", command=resetCanva)

#labels
# currThick = Label(root, text=str(counter), font=('Arial', 16), bg="red")


hostLabel = Label(root, text=str(hostname))
#canvas
canva = Canvas(root,background = "#FEFEFE", cursor="pencil")

menu = createMenu(root)
root.config(menu=menu)

#grid
#blackButton.grid(row=0, column=0)
#redButton.grid(row=0, column=1)
#greenButton.grid(row=0, column=2)
#blueButton.grid(row=0, column=3)



#mOneButton.grid(row=0, column=0)
currThick.grid(row=0, column=1, sticky="W")
#pOneButton.grid(row=0, column=2)
thicknessSlider.grid(row=0,column=3)

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
