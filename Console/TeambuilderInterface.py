from tkinter import *
from tkinter import Label, PhotoImage
from PIL import Image, ImageTk
import customtkinter

from PokemonListConsole import AVAILABLE_POKEMONS, POKEMONS


class TeambuilderInterface:
    def __init__(self, master):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        self.master = master
        self.master.title("Teambuilder")
        self.master.geometry("1000x650")
        self.master.resizable(False, False)

        self.mainframe = customtkinter.CTkFrame(self.master)
        self.mainframe.pack(fill=BOTH, expand=True)

        self.create_tabs()

    def create_tabs(self):
        self.tabs = customtkinter.CTkTabview(self.mainframe, height=600, width=800, corner_radius=20)
        self.tabs.pack(pady=10)
        self.tabs_objects = [PokemonTab(self.tabs, i) for i in range(1, 7)]


class PokemonTab:
    def __init__(self, master, index: int):
        self.master = master
        self.column = index
        self.tab = self.master.add(f"  Pokemon {index}  ")
        self.selected_pokemon = None

        self.create_pokemon_frame()
        self.create_moves_frame()
        self.create_stats_frame()

        self.tab.grid_rowconfigure(0, weight=1)
        self.tab.grid_rowconfigure(1, weight=1)
        self.tab.grid_columnconfigure(0, weight=1)
        self.tab.grid_columnconfigure(1, weight=2)


    def create_pokemon_frame(self):
        self.pokemon_frame = customtkinter.CTkFrame(self.tab, corner_radius=20, width=250, height=250)
        self.pokemon_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.pokemon_frame.grid_propagate(False)

        self.pokemon_frame_title = customtkinter.CTkLabel(self.pokemon_frame, text="Pokemon", font=("Arial", 15), corner_radius=35, padx=0)
        self.pokemon_frame_title.pack(side=TOP, pady=15)

        self.photo_image = ImageTk.PhotoImage(Image.open("../Images/pixel-art-pokeball.png"))

        image = customtkinter.CTkImage(dark_image=Image.open("../Images/venusaur-mega.png"), size=(150, 150))
        self.label = customtkinter.CTkLabel(self.pokemon_frame, text="", image=image, corner_radius=10)
        self.label.image = image
        self.label.pack(side=TOP, fill=BOTH, expand=True, pady=15)

        self.pokemon_var = customtkinter.StringVar(value="None")
        self.pokemon_selector = customtkinter.CTkComboBox(self.pokemon_frame,
                                                          values=[pokemon.name for pokemon in AVAILABLE_POKEMONS],
                                                          corner_radius=10,
                                                          variable=self.pokemon_var,
                                                          command=self.on_pokemon_change)
        self.pokemon_selector.pack(side=BOTTOM, pady=15)

    def update_pokemon_frame(self):
        image_path = f"../Images/Sprites/{self.selected_pokemon.name.lower()}.gif"
        image = Image.open(image_path)
        max_size = (200, 200)
        image.thumbnail(max_size)
        photo_image = ImageTk.PhotoImage(image)
        self.label.configure(image=photo_image)
        self.label.image = photo_image


    def on_pokemon_change(self, choice: str):
        self.selected_pokemon = POKEMONS[choice]
        self.update_pokemon_frame()
        print(self.selected_pokemon.name, self.selected_pokemon)

    def create_moves_frame(self):
        self.moves_frame = customtkinter.CTkFrame(self.tab, corner_radius=20)
        self.moves_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.moves_frame.grid_propagate(False)

    def create_stats_frame(self):
        self.lower_frame = customtkinter.CTkFrame(self.tab, corner_radius=20)
        self.lower_frame.grid(row=1, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.lower_frame.grid_propagate(False)


def main():
    root = customtkinter.CTk()
    TeambuilderInterface(root)
    root.mainloop()


if __name__ == "__main__":
    main()
