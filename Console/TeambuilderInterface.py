from PIL import Image, ImageTk
import customtkinter

from PokemonListConsole import AVAILABLE_POKEMONS, POKEMONS

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class TeambuilderInterface(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Teambuilder")
        self.geometry("1000x650")
        self.resizable(False, False)

        self.mainframe = customtkinter.CTkFrame(self.master)
        self.mainframe.pack(fill=customtkinter.BOTH, expand=True)

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
        self.frames_filled = False

        self.create_pokemon_frame()
        self.create_moves_frame()
        self.create_stats_frame()

        self.tab.grid_rowconfigure(0, weight=1)
        self.tab.grid_rowconfigure(1, weight=1)
        self.tab.grid_columnconfigure(0, weight=1)
        self.tab.grid_columnconfigure(1, weight=2)

    def create_pokemon_frame(self):
        self.pokemon_frame = customtkinter.CTkFrame(self.tab, corner_radius=20, width=20, height=20)
        self.pokemon_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.pokemon_frame.grid_propagate(False)

        self.pokemon_frame_title = customtkinter.CTkLabel(self.pokemon_frame, text="Pokemon", font=("Arial", 20), corner_radius=35)
        self.pokemon_frame_title.place(x=40, y=10)

        self.image = customtkinter.CTkImage(dark_image=Image.open("../Images/Static_sprites/greninja.png"), size=(124, 124))
        self.label = customtkinter.CTkLabel(self.pokemon_frame, text="", image=self.image)
        self.label.image = self.image
        self.label.place(x=33, y=70)

        self.pokemon_var = customtkinter.StringVar(value="None")
        self.pokemon_selector = customtkinter.CTkComboBox(self.pokemon_frame,
                                                          values=[pokemon.name for pokemon in AVAILABLE_POKEMONS],
                                                          corner_radius=10,
                                                          variable=self.pokemon_var,
                                                          command=self.on_pokemon_change)
        self.pokemon_selector.place(x=22, y=200)

    def update_pokemon_frame(self):
        image_path = f"../Images/Static_Sprites/{self.selected_pokemon.name.lower()}.png"
        self.image = customtkinter.CTkImage(Image.open(image_path), size=(124, 124))
        self.label.configure(image=self.image)
        self.label.image = self.image
        self.selected_pokemon = POKEMONS[self.pokemon_var.get()]
        if not self.frames_filled:
            self.fill_stats_frame()
            self.frames_filled = True

    def on_pokemon_change(self, choice: str):
        self.selected_pokemon = POKEMONS[choice]
        self.update_pokemon_frame()
        print(self.selected_pokemon.name, self.selected_pokemon)

    def create_moves_frame(self):
        self.moves_frame = customtkinter.CTkFrame(self.tab, corner_radius=20)
        self.moves_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.moves_frame.grid_propagate(False)

    def create_stats_frame(self):
        self.stats_frame = customtkinter.CTkFrame(self.tab, corner_radius=20)
        self.stats_frame.grid(row=1, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.stats_frame.grid_propagate(False)

    def fill_stats_frame(self):
        self.stats_frame_title = customtkinter.CTkLabel(self.stats_frame, text="Stats", font=("Arial", 20), corner_radius=35)
        self.stats_frame_title.place(x=45, y=10)

        # Hp
        self.hp_stat_name_label = customtkinter.CTkLabel(self.stats_frame, text="HP ", font=("Arial", 15))
        self.hp_stat_name_label.place(x=20, y=40)
        self.hp_progress_bar = customtkinter.CTkProgressBar(self.stats_frame,
                                                            width=200,
                                                            determinate_speed=1,
                                                            progress_color="green")
        self.hp_progress_bar.place(x=60, y=50)
        self.hp_progress_bar.set(750)

        self.ev_var = customtkinter.StringVar(value="0")
        self.ev_var.trace_add("write", self.hp_entry_change)
        self.hp_ev_entry = customtkinter.CTkEntry(self.stats_frame, width=40, font=("Arial", 15), textvariable=self.ev_var)
        self.hp_ev_entry.place(x=520, y=40)

        self.hp_slider = customtkinter.CTkSlider(self.stats_frame,
                                                    from_=0,
                                                    to=252,
                                                    orientation=customtkinter.HORIZONTAL,
                                                    width=200,
                                                    command=self.hp_slider_change,
                                                    number_of_steps=63)
        self.hp_slider.place(x=270, y=46)
        self.hp_stat_number_label = customtkinter.CTkLabel(self.stats_frame, text="0", font=("Arial", 15))
        self.hp_stat_number_label.place(x=480, y=41)


    def hp_slider_change(self, value):
        if int(value) < 50:
            self.hp_progress_bar.configure(progress_color="red")
        elif int(value) < 100:
            self.hp_progress_bar.configure(progress_color="orange")
        elif int(value) < 150:
            self.hp_progress_bar.configure(progress_color="green")
        else:
            self.hp_progress_bar.configure(progress_color="cyan")

        self.hp_progress_bar.set(int(value))
        self.hp_stat_number_label.configure(text=int(value))
        self.ev_var.set(str(int(value)))

    def hp_entry_change(self, *args):
        value = self.ev_var.get()
        if value == '':
            value = '0'
            self.ev_var.set('')
        self.hp_slider.set(int(value))
        self.hp_stat_number_label.configure(text=int(value))



def main():
    t = TeambuilderInterface()
    t.mainloop()


if __name__ == "__main__":
    main()
