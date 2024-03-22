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
        height = 650

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height- height) // 2

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
        self.selected_pokemon = None

        # Stats variables
        self.hp_ev_var = customtkinter.StringVar(value="0")
        self.attack_ev_var = customtkinter.StringVar(value="0")
        self.defense_ev_var = customtkinter.StringVar(value="0")
        self.spe_attack_ev_var = customtkinter.StringVar(value="0")
        self.spe_defense_ev_var = customtkinter.StringVar(value="0")
        self.speed_ev_var = customtkinter.StringVar(value="0")

        self.create_pokemon_frame()
        self.create_moves_frame()
        self.create_stats_frame()

        self.tab.grid_rowconfigure(0, weight=1)
        self.tab.grid_rowconfigure(1, weight=1)
        self.tab.grid_columnconfigure(0, weight=1)
        self.tab.grid_columnconfigure(1, weight=2)

        self.evs_max_reached_label = customtkinter.CTkLabel(self.stats_frame,
                                                            text="EVs maximum reached",
                                                            font=("Arial", 15, "bold"),
                                                            text_color="orange",
                                                            compound="left",
                                                            corner_radius=30,
                                                            padx=5)

        self.evs_max_reached_label.place(x=537, y=5)  # adjust the position as needed
        self.evs_max_reached_label.lower()

        self.evs_max_exceeded_label = customtkinter.CTkLabel(self.stats_frame,
                                                             text="EVs maximum exceeded!",
                                                             font=("Arial", 15, "bold"),
                                                             text_color="red",
                                                             compound="left",
                                                             corner_radius=30,
                                                             padx=5,
                                                             image=customtkinter.CTkImage(Image.open("../Images/red-warning-icon.png"),
                                                                                          size=(20, 20)))
        self.evs_max_exceeded_label.place(x=495, y=5)  # adjust the position as needed
        self.evs_max_exceeded_label.lower()  # Hide the label initially

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
        return 508 - int(self.hp_ev_var.get()) - int(self.attack_ev_var.get()) - int(self.defense_ev_var.get()) - int(self.spe_attack_ev_var.get()) - int(self.spe_defense_ev_var.get()) - int(self.speed_ev_var.get())

    @property
    def selected_pokemon_hp(self):
        if self.hp_ev_var.get() == '':
            self.hp_ev_var.set('0')
        return self.selected_pokemon.max_hp + int(self.hp_ev_var.get()) // 4

    @property
    def selected_pokemon_attack(self):
        if self.attack_ev_var.get() == '':
            self.attack_ev_var.set('0')
        return self.selected_pokemon.attack_stat + int(self.attack_ev_var.get()) // 4

    @property
    def selected_pokemon_defense(self):
        if self.defense_ev_var.get() == '':
            self.defense_ev_var.set('0')
        return self.selected_pokemon.defense_stat + int(self.defense_ev_var.get()) // 4

    @property
    def selected_pokemon_spe_attack(self):
        if self.spe_attack_ev_var.get() == '':
            self.spe_attack_ev_var.set('0')
        return self.selected_pokemon.special_attack_stat + int(self.spe_attack_ev_var.get()) // 4

    @property
    def selected_pokemon_spe_defense(self):
        if self.spe_defense_ev_var.get() == '':
            self.spe_defense_ev_var.set('0')
        return self.selected_pokemon.special_defense_stat + int(self.spe_defense_ev_var.get()) // 4

    @property
    def selected_pokemon_speed(self):
        if self.speed_ev_var.get() == '':
            self.speed_ev_var.set('0')
        return self.selected_pokemon.speed_stat + int(self.speed_ev_var.get()) // 4

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

    def on_pokemon_change(self, choice: str):
        self.selected_pokemon = POKEMONS[choice]
        self.update_pokemon_frame()
        # Reset the EVs
        self.hp_ev_var = customtkinter.StringVar(value="0")
        self.attack_ev_var = customtkinter.StringVar(value="0")
        self.defense_ev_var = customtkinter.StringVar(value="0")
        self.spe_attack_ev_var = customtkinter.StringVar(value="0")
        self.spe_defense_ev_var = customtkinter.StringVar(value="0")
        self.speed_ev_var = customtkinter.StringVar(value="0")

        self.fill_stats_frame()

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
        self.stats_frame_title.place(x=55, y=10)

        # Base, Ev and total labels
        self.base_label = customtkinter.CTkLabel(self.stats_frame, text="Base", font=("Arial", 13, "italic"))
        self.base_label.place(x=85, y=34)

        self.ev_label = customtkinter.CTkLabel(self.stats_frame, text="EVs", font=("Arial", 12, "italic"))
        self.ev_label.place(x=335, y=34)

        self.total_label = customtkinter.CTkLabel(self.stats_frame, text="Total", font=("Arial", 13, "italic"))
        self.total_label.place(x=582, y=34)

        self.fill_hp_stat()
        self.fill_attack_stat()
        self.fill_defense_stat()
        self.fill_spe_attack_stat()
        self.fill_spe_defense_stat()
        self.fill_speed_stat()

    def fill_hp_stat(self):
        # Hp
        self.hp_stat_name_label = customtkinter.CTkLabel(self.stats_frame, text="HP", font=("Arial", 15), justify="right")
        self.hp_stat_name_label.place(x=45, y=57)

        self.hp_base_stat_number_label = customtkinter.CTkLabel(self.stats_frame, text=str(self.selected_pokemon.max_hp), font=("Arial", 15))
        self.hp_base_stat_number_label.place(x=85, y=56)

        self.hp_progress_bar = customtkinter.CTkProgressBar(self.stats_frame,
                                                            width=200,
                                                            determinate_speed=1,
                                                            progress_color="green")
        self.hp_progress_bar.place(x=115, y=67)
        self.hp_progress_bar.set(self.selected_pokemon_hp / 500)

        self.hp_ev_var.trace_add("write", self.hp_entry_change)
        self.hp_ev_entry = customtkinter.CTkEntry(self.stats_frame, width=40, font=("Arial", 15), textvariable=self.hp_ev_var)
        self.hp_ev_entry.place(x=330, y=57)

        self.hp_slider = customtkinter.CTkSlider(self.stats_frame,
                                                 from_=0,
                                                 to=min(252, max(self.remaining_ev, 0)),
                                                 orientation=customtkinter.HORIZONTAL,
                                                 width=200,
                                                 command=self.hp_slider_change,
                                                 number_of_steps=63)
        self.config_hp_progress_bar_color()
        self.hp_slider.set(0)
        self.hp_slider.place(x=375, y=63)

        self.total_hp_label = customtkinter.CTkLabel(self.stats_frame, text=self.selected_pokemon.max_hp, font=("Arial", 15))
        self.total_hp_label.place(x=585, y=57)

    def fill_attack_stat(self):
        # Attack
        self.attack_stat_name_label = customtkinter.CTkLabel(self.stats_frame, text="Attack", font=("Arial", 15), justify="right")
        self.attack_stat_name_label.place(x=25, y=90)

        self.attack_base_stat_number_label = customtkinter.CTkLabel(self.stats_frame, text=str(self.selected_pokemon.attack_stat), font=("Arial", 15))
        self.attack_base_stat_number_label.place(x=85, y=89)

        self.attack_progress_bar = customtkinter.CTkProgressBar(self.stats_frame,
                                                                width=200,
                                                                determinate_speed=1,
                                                                progress_color="green")
        self.attack_progress_bar.place(x=115, y=100)
        self.attack_progress_bar.set(self.selected_pokemon_attack / 500)

        self.attack_ev_var.trace_add("write", self.attack_entry_change)
        self.attack_ev_entry = customtkinter.CTkEntry(self.stats_frame, width=40, font=("Arial", 15), textvariable=self.attack_ev_var)
        self.attack_ev_entry.place(x=330, y=90)

        self.attack_slider = customtkinter.CTkSlider(self.stats_frame,
                                                     from_=0,
                                                     to=min(252, max(self.remaining_ev, 0)),
                                                     orientation=customtkinter.HORIZONTAL,
                                                     width=200,
                                                     command=self.attack_slider_change,
                                                     number_of_steps=63)
        self.config_attack_progress_bar_color()
        self.attack_slider.set(0)
        self.attack_slider.place(x=375, y=96)

        self.total_attack_label = customtkinter.CTkLabel(self.stats_frame, text=self.selected_pokemon.attack_stat, font=("Arial", 15))
        self.total_attack_label.place(x=585, y=90)

    def fill_defense_stat(self):
        # Defense
        self.defense_stat_name_label = customtkinter.CTkLabel(self.stats_frame, text="Defense", font=("Arial", 15), justify="right")
        self.defense_stat_name_label.place(x=12, y=123)

        self.defense_base_stat_number_label = customtkinter.CTkLabel(self.stats_frame, text=str(self.selected_pokemon.defense_stat), font=("Arial", 15))
        self.defense_base_stat_number_label.place(x=85, y=122)

        self.defense_progress_bar = customtkinter.CTkProgressBar(self.stats_frame,
                                                                 width=200,
                                                                 determinate_speed=1,
                                                                 progress_color="green")
        self.defense_progress_bar.place(x=115, y=133)
        self.defense_progress_bar.set(self.selected_pokemon_defense / 500)

        self.defense_ev_var.trace_add("write", self.defense_entry_change)
        self.defense_ev_entry = customtkinter.CTkEntry(self.stats_frame, width=40, font=("Arial", 15), textvariable=self.defense_ev_var)
        self.defense_ev_entry.place(x=330, y=123)

        self.defense_slider = customtkinter.CTkSlider(self.stats_frame,
                                                      from_=0,
                                                      to=min(252, max(self.remaining_ev, 0)),
                                                      orientation=customtkinter.HORIZONTAL,
                                                      width=200,
                                                      command=self.defense_slider_change,
                                                      number_of_steps=63)
        self.config_defense_progress_bar_color()
        self.defense_slider.set(0)
        self.defense_slider.place(x=375, y=129)

        self.total_defense_label = customtkinter.CTkLabel(self.stats_frame, text=self.selected_pokemon.defense_stat, font=("Arial", 15))
        self.total_defense_label.place(x=585, y=123)

    def fill_spe_attack_stat(self):
        # Special Attack
        self.spe_attack_stat_name_label = customtkinter.CTkLabel(self.stats_frame, text="Sp. Atk.", font=("Arial", 15), justify="right")
        self.spe_attack_stat_name_label.place(x=12, y=156)

        self.spe_attack_base_stat_number_label = customtkinter.CTkLabel(self.stats_frame, text=str(self.selected_pokemon.special_attack_stat), font=("Arial", 15))
        self.spe_attack_base_stat_number_label.place(x=85, y=155)

        self.spe_attack_progress_bar = customtkinter.CTkProgressBar(self.stats_frame,
                                                                    width=200,
                                                                    determinate_speed=1,
                                                                    progress_color="green")
        self.spe_attack_progress_bar.place(x=115, y=166)
        self.spe_attack_progress_bar.set(self.selected_pokemon_spe_attack / 500)

        self.spe_attack_ev_var.trace_add("write", self.spe_attack_entry_change)
        self.spe_attack_ev_entry = customtkinter.CTkEntry(self.stats_frame, width=40, font=("Arial", 15), textvariable=self.spe_attack_ev_var)
        self.spe_attack_ev_entry.place(x=330, y=156)

        self.spe_attack_slider = customtkinter.CTkSlider(self.stats_frame,
                                                         from_=0,
                                                         to=min(252, max(self.remaining_ev, 0)),
                                                         orientation=customtkinter.HORIZONTAL,
                                                         width=200,
                                                         command=self.spe_attack_slider_change,
                                                         number_of_steps=63)
        self.config_spe_attack_progress_bar_color()
        self.spe_attack_slider.set(0)
        self.spe_attack_slider.place(x=375, y=162)

        self.total_spe_attack_label = customtkinter.CTkLabel(self.stats_frame, text=self.selected_pokemon.special_attack_stat, font=("Arial", 15))
        self.total_spe_attack_label.place(x=585, y=156)

    def fill_spe_defense_stat(self):
        # Special Defense
        self.spe_defense_stat_name_label = customtkinter.CTkLabel(self.stats_frame, text="Sp. Def.", font=("Arial", 15), justify="right")
        self.spe_defense_stat_name_label.place(x=12, y=189)

        self.spe_defense_base_stat_number_label = customtkinter.CTkLabel(self.stats_frame, text=str(self.selected_pokemon.special_defense_stat), font=("Arial", 15))
        self.spe_defense_base_stat_number_label.place(x=85, y=188)

        self.spe_defense_progress_bar = customtkinter.CTkProgressBar(self.stats_frame,
                                                                     width=200,
                                                                     determinate_speed=1,
                                                                     progress_color="green")
        self.spe_defense_progress_bar.place(x=115, y=199)
        self.spe_defense_progress_bar.set(self.selected_pokemon_spe_defense / 500)

        self.spe_defense_ev_var.trace_add("write", self.spe_defense_entry_change)
        self.spe_defense_ev_entry = customtkinter.CTkEntry(self.stats_frame, width=40, font=("Arial", 15), textvariable=self.spe_defense_ev_var)
        self.spe_defense_ev_entry.place(x=330, y=189)

        self.spe_defense_slider = customtkinter.CTkSlider(self.stats_frame,
                                                          from_=0,
                                                          to=min(252, max(self.remaining_ev, 0)),
                                                          orientation=customtkinter.HORIZONTAL,
                                                          width=200,
                                                          command=self.spe_defense_slider_change,
                                                          number_of_steps=63)
        self.config_spe_defense_progress_bar_color()
        self.spe_defense_slider.set(0)
        self.spe_defense_slider.place(x=375, y=195)

        self.total_spe_defense_label = customtkinter.CTkLabel(self.stats_frame, text=self.selected_pokemon.special_defense_stat, font=("Arial", 15))
        self.total_spe_defense_label.place(x=585, y=189)

    def fill_speed_stat(self):
        # Speed
        self.speed_stat_name_label = customtkinter.CTkLabel(self.stats_frame, text="Speed ", font=("Arial", 15), justify="right")
        self.speed_stat_name_label.place(x=12, y=222)

        self.speed_base_stat_number_label = customtkinter.CTkLabel(self.stats_frame, text=str(self.selected_pokemon.speed_stat), font=("Arial", 15))
        self.speed_base_stat_number_label.place(x=85, y=221)

        self.speed_progress_bar = customtkinter.CTkProgressBar(self.stats_frame,
                                                               width=200,
                                                               determinate_speed=1,
                                                               progress_color="green")

        self.config_speed_progress_bar_color()
        self.speed_progress_bar.place(x=115, y=232)
        self.speed_progress_bar.set(self.selected_pokemon_speed / 500)

        self.speed_ev_var.trace_add("write", self.speed_entry_change)
        self.speed_ev_entry = customtkinter.CTkEntry(self.stats_frame, width=40, font=("Arial", 15), textvariable=self.speed_ev_var)
        self.speed_ev_entry.place(x=330, y=222)

        self.speed_slider = customtkinter.CTkSlider(self.stats_frame,
                                                    from_=0,
                                                    to=min(252, max(self.remaining_ev, 0)),
                                                    orientation=customtkinter.HORIZONTAL,
                                                    width=200,
                                                    command=self.speed_slider_change,
                                                    number_of_steps=63)
        self.speed_slider.set(0)
        self.speed_slider.place(x=375, y=228)

        self.total_speed_label = customtkinter.CTkLabel(self.stats_frame, text=self.selected_pokemon.speed_stat, font=("Arial", 15))
        self.total_speed_label.place(x=585, y=222)

    def hp_slider_change(self, value):
        # Convert the value to an integer
        value = int(value)

        # If the remaining EVs are 0 and the new value is greater than the current EV, return
        if self.remaining_ev <= 0 and value > int(self.hp_ev_var.get()):
            self.hp_slider.set(int(self.hp_ev_var.get()))
            return

        self.hp_ev_var.set(str(value))
        self.hp_slider.set(value)

        # Update the progress bar
        self.hp_progress_bar.set(self.selected_pokemon_hp / 500)
        self.check_remaining_ev()

    def hp_entry_change(self, *args):
        value = self.hp_ev_var.get()
        self.config_hp_progress_bar_color()

        if self.remaining_ev > 0:
            if value == '':
                value = '0'
                self.hp_ev_var.set('')

        self.hp_slider_change(int(value))
        self.total_hp_label.configure(text=self.selected_pokemon_hp)

    def config_hp_progress_bar_color(self):
        if self.selected_pokemon_hp < 100:
            self.hp_progress_bar.configure(progress_color="red")
        elif self.selected_pokemon_hp < 150:
            self.hp_progress_bar.configure(progress_color="orange")
        elif self.selected_pokemon_hp < 200:
            self.hp_progress_bar.configure(progress_color="yellow")
        elif self.selected_pokemon_hp < 300:
            self.hp_progress_bar.configure(progress_color="green")
        elif self.selected_pokemon_hp > 500:
            self.hp_progress_bar.configure(progress_color="cyan")

    def attack_slider_change(self, value):
        value = int(value)
        if self.remaining_ev <= 0 and value > int(self.attack_ev_var.get()):
            self.attack_slider.set(int(self.attack_ev_var.get()))
            return

        self.attack_ev_var.set(str(value))
        self.attack_slider.set(value)

        self.attack_progress_bar.set(self.selected_pokemon_attack / 500)
        self.check_remaining_ev()

    def attack_entry_change(self, *args):
        value = self.attack_ev_var.get()
        self.config_attack_progress_bar_color()

        if self.remaining_ev > 0:
            if value == '':
                value = '0'
                self.attack_ev_var.set('')

        self.attack_slider_change(int(value))
        self.total_attack_label.configure(text=self.selected_pokemon_attack)

    def config_attack_progress_bar_color(self):
        if self.selected_pokemon_attack < 100:
            self.attack_progress_bar.configure(progress_color="red")
        elif self.selected_pokemon_attack < 150:
            self.attack_progress_bar.configure(progress_color="orange")
        elif self.selected_pokemon_attack < 200:
            self.attack_progress_bar.configure(progress_color="yellow")
        elif self.selected_pokemon_attack < 300:
            self.attack_progress_bar.configure(progress_color="green")
        elif self.selected_pokemon_attack > 500:
            self.attack_progress_bar.configure(progress_color="cyan")

    def defense_slider_change(self, value):
        value = int(value)
        if self.remaining_ev <= 0 and value > int(self.defense_ev_var.get()):
            self.defense_slider.set(int(self.defense_ev_var.get()))
            return
        self.defense_ev_var.set(str(value))
        self.defense_slider.set(value)

        self.defense_progress_bar.set(self.selected_pokemon_defense / 500)
        self.check_remaining_ev()

    def defense_entry_change(self, *args):
        value = self.defense_ev_var.get()
        self.config_defense_progress_bar_color()

        if self.remaining_ev > 0:
            if value == '':
                value = '0'
                self.defense_ev_var.set('')

        self.defense_slider_change(int(value))
        self.total_defense_label.configure(text=self.selected_pokemon_defense)

    def config_defense_progress_bar_color(self):
        if self.selected_pokemon_defense < 100:
            self.defense_progress_bar.configure(progress_color="red")
        elif self.selected_pokemon_defense < 150:
            self.defense_progress_bar.configure(progress_color="orange")
        elif self.selected_pokemon_defense < 200:
            self.defense_progress_bar.configure(progress_color="yellow")
        elif self.selected_pokemon_defense < 300:
            self.defense_progress_bar.configure(progress_color="green")
        elif self.selected_pokemon_defense > 500:
            self.defense_progress_bar.configure(progress_color="cyan")

    def spe_attack_slider_change(self, value):
        value = int(value)
        if self.remaining_ev <= 0 and value > int(self.spe_attack_ev_var.get()):
            self.spe_attack_slider.set(int(self.spe_attack_ev_var.get()))
            return
        self.spe_attack_ev_var.set(str(value))
        self.spe_attack_slider.set(value)

        self.spe_attack_progress_bar.set(self.selected_pokemon_spe_attack / 500)
        self.check_remaining_ev()

    def spe_attack_entry_change(self, *args):
        value = self.spe_attack_ev_var.get()
        self.config_spe_attack_progress_bar_color()

        if self.remaining_ev > 0:
            if value == '':
                value = '0'
                self.spe_attack_ev_var.set('')

        self.spe_attack_slider_change(int(value))
        self.total_spe_attack_label.configure(text=self.selected_pokemon.spe_attack + int(value) // 4)

    def config_spe_attack_progress_bar_color(self):
        if self.selected_pokemon_spe_attack < 100:
            self.spe_attack_progress_bar.configure(progress_color="red")
        elif self.selected_pokemon_spe_attack < 150:
            self.spe_attack_progress_bar.configure(progress_color="orange")
        elif self.selected_pokemon_spe_attack < 200:
            self.spe_attack_progress_bar.configure(progress_color="yellow")
        elif self.selected_pokemon_spe_attack < 300:
            self.spe_attack_progress_bar.configure(progress_color="green")
        elif self.selected_pokemon_spe_attack > 500:
            self.spe_attack_progress_bar.configure(progress_color="cyan")

    def spe_defense_slider_change(self, value):
        value = int(value)
        if self.remaining_ev <= 0 and value > int(self.spe_defense_ev_var.get()):
            self.spe_defense_slider.set(int(self.spe_defense_ev_var.get()))
            return
        self.spe_defense_ev_var.set(str(value))
        self.spe_defense_slider.set(value)

        self.spe_defense_progress_bar.set(self.selected_pokemon_spe_defense / 500)
        self.check_remaining_ev()

    def spe_defense_entry_change(self, *args):
        value = self.spe_defense_ev_var.get()
        self.config_spe_defense_progress_bar_color()

        if self.remaining_ev > 0:
            if value == '':
                value = '0'
                self.spe_defense_ev_var.set('')

        self.spe_defense_slider_change(int(value))
        self.total_spe_defense_label.configure(text=self.selected_pokemon.spe_defense + int(value) // 4)

    def config_spe_defense_progress_bar_color(self):
        if self.selected_pokemon_spe_defense < 100:
            self.spe_defense_progress_bar.configure(progress_color="red")
        elif self.selected_pokemon_spe_defense < 150:
            self.spe_defense_progress_bar.configure(progress_color="orange")
        elif self.selected_pokemon_spe_defense < 200:
            self.spe_defense_progress_bar.configure(progress_color="yellow")
        elif self.selected_pokemon_spe_defense < 300:
            self.spe_defense_progress_bar.configure(progress_color="green")
        elif self.selected_pokemon_spe_defense > 500:
            self.spe_defense_progress_bar.configure(progress_color="cyan")

    def speed_slider_change(self, value):
        value = int(value)
        if self.remaining_ev <= 0 and value > int(self.speed_ev_var.get()):
            self.speed_slider.set(int(self.speed_ev_var.get()))
            return
        self.speed_ev_var.set(str(value))
        self.speed_slider.set(value)

        self.speed_progress_bar.set(self.selected_pokemon_speed / 500)
        self.check_remaining_ev()

    def speed_entry_change(self, *args):
        value = self.speed_ev_var.get()
        self.config_speed_progress_bar_color()

        if self.remaining_ev > 0:
            if value == '':
                value = '0'
                self.speed_ev_var.set('')

        self.speed_slider_change(int(value))
        self.total_speed_label.configure(text=self.selected_pokemon.speed_stat + int(value) // 4)

    def config_speed_progress_bar_color(self):
        if self.selected_pokemon_speed < 100:
            self.speed_progress_bar.configure(progress_color="red")
        elif self.selected_pokemon_speed < 150:
            self.speed_progress_bar.configure(progress_color="orange")
        elif self.selected_pokemon_speed < 200:
            self.speed_progress_bar.configure(progress_color="yellow")
        elif self.selected_pokemon_speed < 300:
            self.speed_progress_bar.configure(progress_color="green")
        elif self.selected_pokemon_speed > 500:
            self.speed_progress_bar.configure(progress_color="cyan")

    def check_remaining_ev(self):
        if self.remaining_ev < 0:
            self.evs_max_reached_label.lower()
            self.evs_max_exceeded_label.lift()  # Show the label
        elif self.remaining_ev == 0:
            self.evs_max_exceeded_label.lower()
            self.evs_max_reached_label.lift()
        else:
            self.evs_max_reached_label.lower()
            self.evs_max_exceeded_label.lower()  # Hide the label


def main():
    t = TeambuilderInterface()
    t.mainloop()


if __name__ == "__main__":
    main()
