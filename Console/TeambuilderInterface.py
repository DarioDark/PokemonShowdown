from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

from PokemonListConsole import AVAILABLE_POKEMONS


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
        self.create_tabs()

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
        # self.helpmenu.add_command(label="Help Index", command=self.donothing)        for i in range(1, 7):
        # self.helpmenu.add_command(label="About...", command=self.donothing)
        # self.menubar.add_cascade(label="Help", menu=self.helpmenu)

    def create_tabs(self):
        self.tabs = ttk.Notebook(self.mainframe, height=300, width=200)
        self.tabs.grid(row=0, sticky=(N, W, E, S))

        for i in range(1, 7):
            PokemonTab(self.tabs, i)

        # Make the tabs take the entire space in width
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=2)  # Increase the weight to make the tabs a little taller


class PokemonTab:
    def __init__(self, master, column: int):
        self.master = master
        self.column = column
        self.tab = ttk.Frame(self.master)
        self.master.add(self.tab, text=f"Pokemon {column}")

        # Create the frames
        self.image_frame = Frame(self.tab)
        self.utilities_frame = Frame(self.tab)
        self.moves_frame = Frame(self.tab)
        self.stats_frame = Frame(self.tab)

        self.image_frame.grid(row=0, column=0, sticky="N, W, E, S")
        self.utilities_frame.grid(row=0, column=1, sticky="N, W, E, S")
        self.moves_frame.grid(row=0, column=2, sticky="N, W, E, S")
        self.stats_frame.grid(row=1, sticky="N, W, E, S")

        # Create a canvas to display the pokemon
        self.canvas = Canvas(self.image_frame, width=200, height=150)
        self.canvas.grid(row=0, column=0, sticky="N, W, E, S")
        image = ImageTk.PhotoImage(Image.open(f"../Images/pixel-art-pokeball.png"))
        self.img_item = self.canvas.create_image(50, 75, anchor=W, image=image)
        self.canvas.image = image

        # Create a dropdown menu to select a pokemon
        self.var = StringVar(self.image_frame)
        self.var.set("Select a Pokemon")
        self.var.trace("w", self.on_pokemon_selected)

        options = ttk.Combobox(self.image_frame, textvariable=self.var, values=[pokemon.name for pokemon in AVAILABLE_POKEMONS])
        options.grid(row=1, column=0)

    def on_pokemon_selected(self, *args):
        selected_pokemon = self.var.get()
        if selected_pokemon != "Select a Pokemon":
            image = ImageTk.PhotoImage(Image.open(f"../Images/Sprites/{selected_pokemon.lower().replace(' ', '-')}.gif"))
            self.canvas.delete(self.img_item)
            self.img_item = self.canvas.create_image(100, 75, anchor=CENTER, image=image)
            self.canvas.image = image


def main():
    root = Tk()
    app = TeambuilderInterface(root)
    root.mainloop()


if __name__ == "__main__":
    main()