import socket
import threading
from tkinter import *

PORT = 37234
# HOST = '192.168.0.143'
HOST = socket.gethostbyname('S4-K001')
BUFFER = 65536

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

client_host = socket.gethostname()
client_ip = str(socket.gethostbyname(client_host)).encode("utf8")

client_socket.send(client_ip)


print("Oczekiwanie na połączenie...")
info = client_socket.recv(BUFFER).decode("utf8")
print(info)


master = Tk()
canva = Canvas(master, background="#FEFEFE", cursor="pencil")
canva.grid(row=1, column=0, columnspan=100, sticky="nsew")
converted = []
def receive():
    global converted
    while True:
        
        info = client_socket.recv(BUFFER).decode("utf8")
        try:
            converted = eval((info))
        except:
            #print("Cos jest nie tak")
            converted = []
        print(converted)
        #print(converted)

def drawpoint(x1,y1, color, thickness):
    canva.create_oval(x1-thickness, y1-thickness, x1+thickness, y1+thickness, fill=color, outline=color)
    

def draw():
    global converted
    while True:
        if len(converted) > 0:
            x1 = converted[0]
            y1 = converted[1]
            x2 = converted[2]
            y2 = converted[3]
            color = converted[4]
            thickness = converted[5]
            converted.clear()
            xdiff = x1-x2
            ydiff = y1-y2
            maxnum = max(abs(xdiff), abs(ydiff))
            for i in range(maxnum):
                x = int(x2 + (float(i)/maxnum * xdiff))
                y = int(y2 + (float(i)/maxnum * ydiff))
                drawpoint(x,y, color, thickness)
            
            #canva.create_oval(x-1, y-1, x+1, y+1, fill="black", outline="black")


socketThread = threading.Thread(target=receive)
socketThread.start()
drawThread = threading.Thread(target=draw)
drawThread.start()
# def thread2():
master.mainloop()
# thread2= threading.Thread(target=thread2)
# thread2.start()