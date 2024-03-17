from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import customtkinter

from PokemonListConsole import AVAILABLE_POKEMONS


class TeambuilderInterface:
    def __init__(self, master):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        self.master = master
        self.master.title("Teambuilder")
        self.master.geometry("800x800")
        self.master.resizable(False, False)

        self.mainframe = customtkinter.CTkFrame(self.master)
        self.mainframe.pack(fill=BOTH, expand=True)

        self.create_tabs()

    def create_tabs(self):
        self.tabs = customtkinter.CTkTabview(self.mainframe, height=750, width=500)
        self.tabs.pack(pady=10)

        for i in range(1, 7):
            PokemonTab(self.tabs, i)

        # Make the tabs take the entire space in width
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=2)  # Increase the weight to make the tabs a little taller


class PokemonTab:
    def __init__(self, master, column: int):
        self.master = master
        self.column = column
        self.tab = customtkinter.CTkFrame(self.master)
        self.master.add(f"  Pokemon {column}  ")

        # Creating the frames
        self.image_frame = customtkinter.CTkFrame(self.tab)
        self.utilities_frame = customtkinter.CTkFrame(self.tab)
        self.moves_frame = customtkinter.CTkFrame(self.tab)
        self.stats_frame = customtkinter.CTkFrame(self.tab)

        # Séparators
        self.separator1 = ttk.Separator(self.tab, orient=VERTICAL)
        self.separator2 = ttk.Separator(self.tab, orient=VERTICAL)
        self.separator3 = ttk.Separator(self.tab, orient=HORIZONTAL)

        self.image_frame.grid(row=0, column=0, sticky="nsew")
        self.separator1.grid(row=0, column=1, sticky="ns")
        self.utilities_frame.grid(row=0, column=2, sticky="nsew")
        self.separator2.grid(row=0, column=3, sticky="ns")
        self.moves_frame.grid(row=0, column=4, sticky="nsew")
        self.separator3.grid(row=1, column=0, columnspan=5, sticky="ew")
        self.stats_frame.grid(row=2, column=0, columnspan=5, sticky="nsew")

        # Set the weights for the rows and columns
        self.tab.rowconfigure(0, weight=1)
        self.tab.rowconfigure(2, weight=3)
        self.tab.columnconfigure(0, weight=0)
        self.tab.columnconfigure(1, weight=0)  # Pas de poids pour le séparateur
        self.tab.columnconfigure(2, weight=1)
        self.tab.columnconfigure(3, weight=0)  # Pas de poids pour le séparateur
        self.tab.columnconfigure(4, weight=1)

        self.utilities_frame.grid_propagate(False)
        self.moves_frame.grid_propagate(False)

        # Create a canvas to display the pokemon
        self.canvas = customtkinter.CTkCanvas(self.image_frame, width=200, height=150)
        self.canvas.grid(row=0, column=0, sticky="N, W, E, S")
        image = ImageTk.PhotoImage(Image.open(f"../Images/pixel-art-pokeball.png"))
        self.img_item = self.canvas.create_image(50, 75, anchor=W, image=image)
        self.canvas.image = image

        # Create a dropdown menu to select a pokemon
        self.var = StringVar(self.image_frame)
        self.var.set("Select a Pokemon")
        self.var.trace("w", self.on_pokemon_selected)

        options = ttk.Combobox(self.image_frame, textvariable=self.var, values=[pokemon.name for pokemon in AVAILABLE_POKEMONS], width=30, state="readonly")
        options.grid(row=1, column=0)





    def on_pokemon_selected(self, *args):
        selected_pokemon = self.var.get()
        if selected_pokemon != "Select a Pokemon":
            image = ImageTk.PhotoImage(Image.open(f"../Images/Sprites/{selected_pokemon.lower().replace(' ', '-')}.gif"))
            self.canvas.delete(self.img_item)
            self.img_item = self.canvas.create_image(100, 75, anchor=CENTER, image=image)
            self.canvas.image = image


def main():
    root = customtkinter.CTk()
    app = TeambuilderInterface(root)
    root.mainloop()


if __name__ == "__main__":
    main()