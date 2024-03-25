from PIL import Image
import customtkinter

from PokemonListConsole import AVAILABLE_POKEMONS, POKEMONS


class TeambuilderInterface(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        self.title("Teambuilder")
        self.resizable(False, False)
        self.update_idletasks()  # Update window geometry

        width = 1000
        height = 750

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")

        self.mainframe = customtkinter.CTkFrame(self.master)
        self.mainframe.pack(fill=customtkinter.BOTH, expand=True)

        self.create_tabs()

    def create_tabs(self):
        self.tabs = customtkinter.CTkTabview(self.mainframe, height=700, width=800, corner_radius=20)
        self.tabs.pack(pady=10)
        self.tabs_objects = [PokemonTab(self.tabs, i) for i in range(1, 7)]


class PokemonTab:
    def __init__(self, master, index: int):
        self.master = master
        self.column = index
        self.tab = self.master.add(f"  Pokemon {index}  ")

        self.create_frames()
        self.place_frames()

    @property
    def selected_pokemon(self):
        return self.pokemon_frame.selected_pokemon

    def create_frames(self):
        self.pokemon_frame = PokemonFrame(self.tab, self)
        self.moves_frame = MovesFrame(self.tab, self)
        self.stats_frame = StatsFrame(self.tab, self)

    def place_frames(self):
        # Layout
        self.tab.grid_rowconfigure(0, weight=1)
        self.tab.grid_rowconfigure(1, weight=2)
        self.tab.grid_columnconfigure(0, weight=1)
        self.tab.grid_columnconfigure(1, weight=2)

        self.pokemon_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.moves_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.stats_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

    def update_frames(self):
        self.stats_frame.update_stats_frame()
        self.moves_frame.update_moves_frame()

    def create_moves_frame(self):
        self.moves_frame = customtkinter.CTkFrame(self.tab, corner_radius=20)
        self.moves_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.moves_frame.grid_propagate(False)


class PokemonFrame(customtkinter.CTkFrame):
    def __init__(self, master, pokemon_tab: PokemonTab):
        super().__init__(master, corner_radius=20, width=20, height=30, border_width=1, border_color="red")
        self.master = master
        self.pokemonTab: PokemonTab = pokemon_tab

        self.selected_pokemon = None

        self.create_widgets()
        self.place_widgets()

    def create_widgets(self):
        self.pokemon_frame_title = customtkinter.CTkLabel(self, text="Pokemon", font=("Arial", 20, "bold"), corner_radius=35)
        self.image = customtkinter.CTkImage(dark_image=Image.open("../Images/Static_sprites/empty-sprite.png"), size=(124, 124))
        self.label = customtkinter.CTkLabel(self, text="", image=self.image)
        self.label.image = self.image

        self.pokemon_var = customtkinter.StringVar(value="None")
        self.pokemon_selector = customtkinter.CTkComboBox(self,
                                                          values=[pokemon.name for pokemon in AVAILABLE_POKEMONS],
                                                          corner_radius=10,
                                                          variable=self.pokemon_var,
                                                          command=self.on_pokemon_change)

    def place_widgets(self):
        # Layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.pokemon_frame_title.place(x=40, y=10)
        self.label.place(x=33, y=70)
        self.pokemon_selector.place(x=22, y=200)

    def on_pokemon_change(self, choice: str):
        self.selected_pokemon = POKEMONS[choice]
        self.update_pokemon_frame()
        self.pokemonTab.update_frames()
        self.configure(border_color="green")

        # Reset the EVs
        self.hp_ev_var = customtkinter.StringVar(value="0")
        self.attack_ev_var = customtkinter.StringVar(value="0")
        self.defense_ev_var = customtkinter.StringVar(value="0")
        self.spe_attack_ev_var = customtkinter.StringVar(value="0")
        self.spe_defense_ev_var = customtkinter.StringVar(value="0")
        self.speed_ev_var = customtkinter.StringVar(value="0")

    def update_pokemon_frame(self):
        image_path = f"../Images/Static_Sprites/{self.selected_pokemon.name.lower()}.png"
        self.image = customtkinter.CTkImage(Image.open(image_path), size=(124, 124))
        self.label.configure(image=self.image)
        self.label.image = self.image


class MovesFrame(customtkinter.CTkFrame):
    def __init__(self, master, pokemon_tab: PokemonTab):
        super().__init__(master, corner_radius=20)
        self.master = master
        self.pokemon_tab: PokemonTab = pokemon_tab

    def create_widgets(self):
        self.moves_frame_title = customtkinter.CTkLabel(self, text="Moves", font=("Arial", 20, "bold"), corner_radius=35)

    def place_widgets(self):
        self.moves_frame_title.place(x=222, y=10)

    def update_moves_frame(self):
        self.create_widgets()
        self.place_widgets()


class StatsFrame(customtkinter.CTkFrame):
    def __init__(self, master, pokemon_tab: PokemonTab):
        super().__init__(master, corner_radius=20)
        self.master = master
        self.pokemon_tab: PokemonTab = pokemon_tab

        self.update_ev_vars()

    @property
    def remaining_ev(self):
        if self.hp_ev_var.get() == '':
            self.hp_ev_var.set('0')
        if self.attack_ev_var.get() == '':
            self.attack_ev_var.set('0')
        if self.defense_ev_var.get() == '':
            self.defense_ev_var.set('0')
        if self.spe_attack_ev_var.get() == '':
            self.spe_attack_ev_var.set('0')
        if self.spe_defense_ev_var.get() == '':
            self.spe_defense_ev_var.set('0')
        remaining_ev = 508 - int(self.hp_ev_var.get()) - int(self.attack_ev_var.get()) - int(self.defense_ev_var.get()) - int(self.spe_attack_ev_var.get()) - int(self.spe_defense_ev_var.get()) - int(self.speed_ev_var.get())
        if remaining_ev > 0:
            self.remaining_ev_counter_label.configure(text=f"Remaining EVs: {remaining_ev}")
        return remaining_ev

    @property
    def selected_pokemon_hp(self):
        if self.hp_ev_var.get() == '':
            self.hp_ev_var.set('0')
        if self.pokemon_tab.selected_pokemon:
            return self.pokemon_tab.selected_pokemon.max_hp + int(self.hp_ev_var.get()) // 4

    @property
    def selected_pokemon_attack(self):
        if self.attack_ev_var.get() == '':
            self.attack_ev_var.set('0')
        if self.pokemon_tab.selected_pokemon:
            return self.pokemon_tab.selected_pokemon.attack_stat + int(self.attack_ev_var.get()) // 4

    @property
    def selected_pokemon_defense(self):
        if self.defense_ev_var.get() == '':
            self.defense_ev_var.set('0')
        if self.pokemon_tab.selected_pokemon:
            return self.pokemon_tab.selected_pokemon.defense_stat + int(self.defense_ev_var.get()) // 4

    @property
    def selected_pokemon_spe_attack(self):
        if self.spe_attack_ev_var.get() == '':
            self.spe_attack_ev_var.set('0')
        if self.pokemon_tab.selected_pokemon:
            return self.pokemon_tab.selected_pokemon.special_attack_stat + int(self.spe_attack_ev_var.get()) // 4

    @property
    def selected_pokemon_spe_defense(self):
        if self.spe_defense_ev_var.get() == '':
            self.spe_defense_ev_var.set('0')
        if self.pokemon_tab.selected_pokemon:
            return self.pokemon_tab.selected_pokemon.special_defense_stat + int(self.spe_defense_ev_var.get()) // 4

    @property
    def selected_pokemon_speed(self):
        if self.speed_ev_var.get() == '':
            self.speed_ev_var.set('0')
        if self.pokemon_tab.selected_pokemon:
            return self.pokemon_tab.selected_pokemon.speed_stat + int(self.speed_ev_var.get()) // 4

    def check_remaining_ev(self):
        if self.remaining_ev < 0:
            self.remaining_ev_counter_label.lower()
            self.evs_max_exceeded_label.lift()  # Show the label
            self.configure(border_color="red", border_width=2)
        elif self.remaining_ev == 0:
            self.remaining_ev_counter_label.configure(text="EVs maximum reached!", text_color="green")
            self.configure(border_color="green", border_width=1)
            self.remaining_ev_counter_label.lift()
        else:
            self.remaining_ev_counter_label.configure(text_color="white")
            self.remaining_ev_counter_label.lift()
            self.evs_max_exceeded_label.lower()  # Hide the label
            self.configure(border_width=0)

    def create_stat_lines(self):
        self.stat_lines = [StatLine(self, self.pokemon_tab, "HP", self.pokemon_tab.selected_pokemon.max_hp, self.hp_ev_var, 90),
                           StatLine(self, self.pokemon_tab, "Attack", self.pokemon_tab.selected_pokemon.attack_stat, self.attack_ev_var, 120),
                           StatLine(self, self.pokemon_tab, "Defense", self.pokemon_tab.selected_pokemon.defense_stat, self.defense_ev_var, 150),
                           StatLine(self, self.pokemon_tab, "Sp. Atk.", self.pokemon_tab.selected_pokemon.special_attack_stat, self.spe_attack_ev_var, 180),
                           StatLine(self, self.pokemon_tab, "Sp. Def.", self.pokemon_tab.selected_pokemon.special_defense_stat, self.spe_defense_ev_var, 210),
                           StatLine(self, self.pokemon_tab, "Speed", self.pokemon_tab.selected_pokemon.speed_stat, self.speed_ev_var, 240)]

    def create_widgets(self):
        self.stats_frame_title = customtkinter.CTkLabel(self, text="Stats", font=("Arial", 20, "bold"), corner_radius=35)
        self.base_label = customtkinter.CTkLabel(self, text="Base", font=("Arial", 13, "italic"))
        self.ev_label = customtkinter.CTkLabel(self, text="EVs", font=("Arial", 12, "italic"))
        self.total_label = customtkinter.CTkLabel(self, text="Total", font=("Arial", 13, "italic"))

        # Stats alert labels
        self.remaining_ev_counter_label = customtkinter.CTkLabel(self, text=f"Remaining EVs: 508", font=("Arial", 10, "bold", "italic"),
                                                                 text_color="white")

        self.evs_max_exceeded_label = customtkinter.CTkLabel(self, text="EVs maximum exceeded!", font=("Arial", 10, "bold", "italic"), text_color="red",
                                                             compound="left", corner_radius=30, padx=5,
                                                             image=customtkinter.CTkImage(Image.open("../Images/red-warning-icon.png"), size=(20, 20)))

        self.create_stat_lines()

    def place_widgets(self):
        # Layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        # Title and italic labels
        self.stats_frame_title.place(x=335, y=10)
        self.base_label.place(x=125, y=64)
        self.ev_label.place(x=380, y=64)
        self.total_label.place(x=622, y=64)

        # Stats alert labels
        self.remaining_ev_counter_label.place(x=460, y=285)
        self.evs_max_exceeded_label.place(x=420, y=285)

        self.evs_max_exceeded_label.lower()

    def update_ev_vars(self):
        self.hp_ev_var = customtkinter.StringVar(value="0")
        self.attack_ev_var = customtkinter.StringVar(value="0")
        self.defense_ev_var = customtkinter.StringVar(value="0")
        self.spe_attack_ev_var = customtkinter.StringVar(value="0")
        self.spe_defense_ev_var = customtkinter.StringVar(value="0")
        self.speed_ev_var = customtkinter.StringVar(value="0")

    def update_stats_frame(self):
        self.update_ev_vars()
        self.create_widgets()
        self.place_widgets()


class StatLine:
    stat_to_method = {
        "HP": "selected_pokemon_hp",
        "Attack": "selected_pokemon_attack",
        "Defense": "selected_pokemon_defense",
        "Sp. Atk.": "selected_pokemon_spe_attack",
        "Sp. Def.": "selected_pokemon_spe_defense",
        "Speed": "selected_pokemon_speed"
    }

    def __init__(self, master: StatsFrame, pokemon_tab: PokemonTab, stat_name: str, base_stat: int, ev_var: customtkinter.StringVar, y_position: int):
        self.master = master
        self.pokemon_tab = pokemon_tab
        self.stat_name = stat_name
        self.base_stat = base_stat
        self.ev_var = ev_var
        self.y_position = y_position

        self.create_stat_line()
        self.place_widgets()

    @property
    def selected_pokemon_stat(self):
        return getattr(self.master, self.stat_to_method[self.stat_name])

    def create_stat_line(self):
        self.stat_name_label = customtkinter.CTkLabel(self.master, text=self.stat_name, font=("Arial", 15), anchor="e", width=80)

        self.base_stat_number_label = customtkinter.CTkLabel(self.master, text=str(self.base_stat), font=("Arial", 15))

        self.progress_bar = customtkinter.CTkProgressBar(self.master,
                                                         width=200,
                                                         determinate_speed=1,
                                                         progress_color="green")
        self.progress_bar.set(self.base_stat / 500)
        self.config_progress_bar_color()

        self.ev_var.trace_add("write", self.entry_change)
        self.ev_entry = customtkinter.CTkEntry(self.master, width=40, font=("Arial", 15), textvariable=self.ev_var)

        self.slider = customtkinter.CTkSlider(self.master,
                                              from_=0,
                                              to=min(252, max(self.master.remaining_ev, 0)),
                                              orientation=customtkinter.HORIZONTAL,
                                              width=200,
                                              command=self.slider_change,
                                              number_of_steps=63)
        self.slider.set(0)

        self.total_label = customtkinter.CTkLabel(self.master, text=str(self.base_stat), font=("Arial", 15))

    def place_widgets(self):
        self.stat_name_label.place(x=25, y=self.y_position)
        self.base_stat_number_label.place(x=125, y=self.y_position)
        self.progress_bar.place(x=155, y=self.y_position + 10)
        self.ev_entry.place(x=370, y=self.y_position)
        self.slider.place(x=415, y=self.y_position + 5)
        self.total_label.place(x=625, y=self.y_position)

    def slider_change(self, value):
        value = int(value)
        if self.master.remaining_ev <= 0 and value > int(self.ev_var.get()):
            self.slider.set(int(self.ev_var.get()))
            return

        self.ev_var.set(str(value))
        self.slider.set(value)

        self.progress_bar.set(self.selected_pokemon_stat / 500)
        self.master.check_remaining_ev()

    def entry_change(self, *args):
        value = self.ev_var.get()
        self.config_progress_bar_color()

        if self.master.remaining_ev > 0:
            if value == '':
                value = '0'
                self.ev_var.set('')

        self.slider_change(int(value))
        self.total_label.configure(text=self.selected_pokemon_stat)

    def config_progress_bar_color(self):
        if not self.selected_pokemon_stat:
            return
        if self.selected_pokemon_stat < 100:
            self.progress_bar.configure(progress_color="red")
        elif self.selected_pokemon_stat < 150:
            self.progress_bar.configure(progress_color="orange")
        elif self.selected_pokemon_stat < 225:
            self.progress_bar.configure(progress_color="yellow")
        elif self.selected_pokemon_stat < 300:
            self.progress_bar.configure(progress_color="green")
        elif self.selected_pokemon_stat > 500:
            self.progress_bar.configure(progress_color="cyan")


def main():
    t = TeambuilderInterface()
    t.mainloop()


if __name__ == "__main__":
    main()
