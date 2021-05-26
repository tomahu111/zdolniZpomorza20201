from tkinter import Menu
import dialogs as dialogs
from gui import ePaintGUI, myWindow


menu = None
def createMenu(root):
    # Create menu
    menu = Menu(root)
    # Menu pliku
    filemenu = Menu(menu,tearoff=0)
    filemenu.add_command(label="Otwórz")
    filemenu.add_command(label="Połącz z serwerem", command=dialogs.connectWindow)
    filemenu.add_command(label="Uruchom serwer", command=dialogs.serverManWindow)
    filemenu.add_command(label="Zapisz")
    filemenu.add_command(label="Drukuj")
    filemenu.add_separator()
    filemenu.add_command(label="Ustawienia")
    filemenu.add_command(label="Wyjście", command=root.quit())
    menu.add_cascade(label="Plik", menu=filemenu)
    # Menu edycji
    editmenu = Menu(menu,tearoff=0)
    editmenu.add_command(label="Kopiuj")
    editmenu.add_command(label="Wklej")
    editmenu.add_command(label="Obróć w prawo")
    editmenu.add_command(label="Obróć w lewo")
    editmenu.add_command(label="Odbij w poziomie", command=lambda: myWindow.rotateObjects())
    editmenu.add_command(label="Odbij w pionie")
    editmenu.add_command(label="Resetuj ustawienia pędzla")
    editmenu.add_command(label="Wyczyść", command=lambda: root.resetCanva())

    menu.add_cascade(label="Edycja", menu=editmenu)
    # Menu pomocy
    helpmenu = Menu(menu, tearoff=0)
    helpmenu.add_command(label="O aplikacji", command=dialogs.helpApp)
    menu.add_cascade(label="Pomoc", menu=helpmenu)
    return menu
