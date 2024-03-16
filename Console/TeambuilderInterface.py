from tkinter import *
from tkinter import ttk
from customtkinter import *


# basic customtkinter interface
class TeambuilderInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("Teambuilder")
        self.master.geometry("800x600")
        self.master.resizable(False, False)

        self.mainframe = ttk.Frame(self.master, padding="5 5 5 5")
        self.mainframe.grid(row=0, column=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        self.create_menu()
        self.create_tabs()
        self.add_content_to_tabs()

    # def create_menu(self):
        # self.menubar = Menu(self.master)
        # self.master.config(menu=self.menubar)

        # self.filemenu = Menu(self.menubar, tearoff=0)
        # self.filemenu.add_command(label="New", command=self.donothing)
        # self.filemenu.add_command(label="Open", command=self.donothing)
        # self.filemenu.add_command(label="Save", command=self.donothing)
        # self.filemenu.add_command(label="Save as...", command=self.donothing)
        # self.filemenu.add_command(label="Close", command=self.donothing)
        # self.filemenu.add_separator()
        # self.filemenu.add_command(label="Exit", command=self.master.quit)
        # self.menubar.add_cascade(label="File", menu=self.filemenu)

        # self.editmenu = Menu(self.menubar, tearoff=0)
        # self.editmenu.add_command(label="Undo", command=self.donothing)
        # self.editmenu.add_separator()
        # self.editmenu.add_command(label="Cut", command=self.donothing)
        # self.editmenu.add_command(label="Copy", command=self.donothing)
        # self.editmenu.add_command(label="Paste", command=self.donothing)
        # self.editmenu.add_command(label="Delete", command=self.donothing)
        # self.editmenu.add_command(label="Select All", command=self.donothing)
        # self.menubar.add_cascade(label="Edit", menu=self.editmenu)

        # self.helpmenu = Menu(self.menubar, tearoff=0)
        # self.helpmenu.add_command(label="Help Index", command=self.donothing)
        # self.helpmenu.add_command(label="About...", command=self.donothing)
        # self.menubar.add_cascade(label="Help", menu=self.helpmenu)

    def create_tabs(self):
        self.tabs = ttk.Notebook(self.mainframe)
        self.tabs.grid(row=0, column=0, sticky=(N, W, E, S))

        self.tab1 = ttk.Frame(self.tabs)
        self.tabs.add(self.tab1, text="Tab 1")

        self.tab2 = ttk.Frame(self.tabs)
        self.tabs.add(self.tab2, text="Tab 2")

        self.tab3 = ttk.Frame(self.tabs)
        self.tabs.add(self.tab3, text="Tab 3")

    def add_content_to_tabs(self):
        # Ajout de contenu à l'onglet 1
        label1 = ttk.Label(self.tab1, text="Contenu de l'onglet 1")
        label1.grid(row=0, column=0)

        # Ajout de contenu à l'onglet 2
        label2 = ttk.Label(self.tab2, text="Contenu de l'onglet 2")
        label2.grid(row=0, column=0)

    def donothing(self):
        pass

def main():
    root = Tk()
    app = TeambuilderInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()