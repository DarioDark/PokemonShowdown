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

        # Create the Pokemon image
        self.pokemon_image = Label(self.tab, image="")
        self.pokemon_image.grid(row=0, column=self.column, sticky=(N, W, E, S))


        self.show_gif("../images/Sprites/charizard.gif")

        self.var = StringVar(self.tab)
        self.var.set("Select a Pokemon")  # initial value

        # Trace the variable for changes
        self.var.trace("w", self.on_pokemon_selected)

        options = [pokemon.name for pokemon in AVAILABLE_POKEMONS]
        drop = OptionMenu(self.tab, self.var, options[0], *options[1:])
        drop.grid(row=1, column=column, sticky=(N, W, E, S))

    def on_pokemon_selected(self, *args):
        selected_pokemon = self.var.get()
        if selected_pokemon != "Select a Pokemon":
            self.update_data(selected_pokemon)

    def show_gif(self, gif_path: str):
        self.gif_image = Image.open(gif_path)
        frames = self.gif_image.n_frames
        image_objects = [PhotoImage(file=gif_path, format=f"gif -index {i}") for i in range(frames)]

        count = 0
        def animate(count):
            frame = image_objects[count]
            count += 1
            self.pokemon_image.configure(image=frame)
            if count == frames:
                count = 0
            self.master.after(50, lambda: animate(count))

        animate(count)

    def update_data(self, selected_pokemon: str):
        self.pokemon_image.configure(file=f"../images/{selected_pokemon.lower()}.png")


def main():
    root = Tk()
    app = TeambuilderInterface(root)
    root.mainloop()


if __name__ == "__main__":
    main()