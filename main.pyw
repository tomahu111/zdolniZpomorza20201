import threading
from tkinter import *
from tkinter.ttk import *
from tkinter import colorchooser
import platform
import socket
from gui import *

def main():
    initGui()

main_thread = threading.Thread(target=main)
main_thread.start()
