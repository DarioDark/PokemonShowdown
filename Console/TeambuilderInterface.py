from tkinter import *
from tkinter import Label, PhotoImage
from PIL import Image
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

        self.tabs = customtkinter.CTkTabview(self.mainframe, height=750, width=500, corner_radius=20)
        self.tabs.pack(pady=10)
        self.tabs_objects = [PokemonTab(self.tabs, i) for i in range(1, 7)]

        self.create_tabs()

    def create_tabs(self):
        pass


class PokemonTab:
    def __init__(self, master, index: int):
        self.master = master
        self.column = index
        self.tab = self.master.add(f"  Pokemon {index}  ")

        self.tab.grid_rowconfigure(0, weight=1)
        self.tab.grid_rowconfigure(1, weight=1)

        self.tab.grid_columnconfigure(0, weight=1)

        self.upper_frame = customtkinter.CTkFrame(self.tab, corner_radius=20)
        self.upper_frame.grid(row=0, column=0, sticky="nsew")
        self.upper_frame.grid_propagate(False)  # Prevent resizing based on contents

        self.lower_frame = customtkinter.CTkFrame(self.tab, corner_radius=20)
        self.lower_frame.grid(row=1, column=0, sticky="nsew")
        self.lower_frame.grid_propagate(False)

        self.my_image = PhotoImage(file="../Images/pixel-art-pokeball.png")

        self.my_label = Label(self.upper_frame, image=self.my_image)
        self.my_label.image = self.my_image
        self.my_label.grid(row=0, column=0)


        # Create a canvas to display the pokemon
        # self.canvas = customtkinter.CTkCanvas(self.upper_frame, width=200, height=150)
        #self.canvas.grid(row=0, column=0, sticky="N, W, E, S")
        #image = ImageTk.PhotoImage(Image.open(f"../Images/pixel-art-pokeball.png"))
        #self.img_item = self.canvas.create_image(50, 75, anchor=W, image=image)
        #self.canvas.image = image

def main():
    root = customtkinter.CTk()
    TeambuilderInterface(root)
    root.mainloop()


if __name__ == "__main__":
    main()