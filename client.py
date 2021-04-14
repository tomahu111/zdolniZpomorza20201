import socket
import threading
from tkinter import *

PORT = 37234
# HOST = '192.168.0.143'
HOST = socket.gethostbyname('S4-K001')
BUFFER = 1024


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

client_host = socket.gethostname()
client_ip = str(socket.gethostbyname(client_host)).encode("utf8")

client_socket.send(client_ip)

info = client_socket.recv(BUFFER).decode("utf8")
print(info)



def mainwindow():
    master = Tk()
    canva = Canvas(master, background="#FEFEFE", cursor="pencil")
    canva.grid(row=1, column=0, columnspan=100, sticky="nsew")

    master.mainloop()

def receive():
    while True:
        info = client_socket.recv(BUFFER).decode("utf8")
        converted = eval(info)

thread1 = threading.Thread(target=receive)
thread1.start()
thread2 = threading.Thread(target=mainwindow)
thread2.start()