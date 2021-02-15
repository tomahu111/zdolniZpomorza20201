from tkinter import Menu
import dialogs as dialogs

menu = None
def createMenu(root):
    # Create menu
    menu = Menu(root)
    # Menu pliku
    filemenu = Menu(menu,tearoff=0)
    filemenu.add_command(label="Otwórz")
    filemenu.add_command(label="Połącz z serwerem")
    filemenu.add_command(label="Zapisz")
    filemenu.add_command(label="Drukuj")
    filemenu.add_command(label="Wyślij faxem")
    filemenu.add_command(label="Wyślij e-mailem")
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
    editmenu.add_command(label="Odbij w poziomie")
    editmenu.add_command(label="Odbij w pionie")
    editmenu.add_command(label="Resetuj ustawienia pędzla")
    editmenu.add_command(label="Wyczyść")

    menu.add_cascade(label="Edycja", menu=editmenu)
    # Menu pomocy
    helpmenu = Menu(menu, tearoff=0)
    helpmenu.add_command(label="O aplikacji", command=dialogs.helpApp)
    menu.add_cascade(label="Pomoc", menu=helpmenu)
    return menu