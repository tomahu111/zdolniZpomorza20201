import threading
from tkinter import *
from tkinter.ttk import *
from tkinter import colorchooser
from menus import createMenu
import platform
import socket
from gui import *



# funkcja główna


# definiowanie połaczenia

PORT = 37234
BUFFER = 1024
hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname)

def main():
    initGui()

def hostLabel():
    global HOST
    print(HOST)


def hostMain():
    hostLabel()


main_thread = threading.Thread(target=main)
main_thread.start()

host_thread = threading.Thread(target=hostMain)
host_thread.start()
