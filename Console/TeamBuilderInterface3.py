from PIL import Image
import customtkinter

from PokemonListConsole import AVAILABLE_POKEMONS, POKEMONS
from ItemConsole import Item, ITEM_LIST
from CTkSeparator import CTkSeparator

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
        super().__init__(master, corner_radius=20, width=20, height=30)
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
                                                          state="readonly",
                                                          variable=self.pokemon_var,
                                                          command=self.on_pokemon_change)

    def place_widgets(self):
        # Layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.pokemon_frame_title.place(x=37, y=10)
        self.label.place(x=33, y=70)
        self.pokemon_selector.place(x=22, y=200)

    def on_pokemon_change(self, choice: str):
        self.selected_pokemon = POKEMONS[choice]
        self.update_pokemon_frame()
        self.pokemonTab.update_frames()

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

    def create_moves_widgets(self):
        self.moves_title = customtkinter.CTkLabel(self, text="Moves", font=("Arial", 20, "bold"), corner_radius=35)
        self.move_category_text_label = customtkinter.CTkLabel(self, text="Class", font=("Arial", 12, "italic"))
        self.move_type_text_label = customtkinter.CTkLabel(self, text="Type", font=("Arial", 12, "italic"))
        self.move_lines = [MoveLine(self, self.pokemon_tab, 80 + i * 40, i + 1) for i in range(4)]

    def create_utilities_widgets(self):
        self.utilities_title = customtkinter.CTkLabel(self, text="Utilities", font=("Arial", 20, "bold"), corner_radius=35)

        self.vertical_separator = CTkSeparator(self, orient="vertical")
        self.horizontal_separator = CTkSeparator(self, orient="horizontal")

        self.item_image = customtkinter.CTkImage(Image.open("../Images/Item_sprites/poke-ball.png"), size=(50, 50))
        self.item_image_label = customtkinter.CTkLabel(self, text="", image=self.item_image)
        self.item_image_label.image = self.item_image

        self.item_label = customtkinter.CTkLabel(self, text="Select an item :", font=("Arial", 12, "italic"))
        mega_stone = self.get_mega_stone(self.pokemon_tab.selected_pokemon.name)
        if mega_stone:
            print(mega_stone.value)
            full_item_list = ITEM_LIST + [mega_stone.value]
        else:
            print("No mega stone", self.pokemon_tab.selected_pokemon.name, self.get_mega_stone(self.pokemon_tab.selected_pokemon.name))
            full_item_list = ITEM_LIST

        self.item_selector = customtkinter.CTkComboBox(self, values=full_item_list, corner_radius=10, state="readonly", command=self.on_item_change)

        self.ability_label = customtkinter.CTkLabel(self, text="Select an ability :", font=("Arial", 12, "italic"))
        self.ability_selector = customtkinter.CTkComboBox(self, values=[ability.name.capitalize().replace('_', ' ') for ability in self.pokemon_tab.selected_pokemon.ability_pool],
                                                          corner_radius=10, state="readonly")

    def place_widgets(self):
        self.moves_title.place(x=120, y=10)
        self.utilities_title.place(x=380, y=10)

        self.move_category_text_label.place(x=235, y=50)
        self.move_type_text_label.place(x=290, y=50)

        self.vertical_separator.place(x=340, y=30, relheight=0.8)
        self.horizontal_separator.place(x=355, y=175, relwidth=0.3)

        self.item_image_label.place(x=405, y=50)
        self.item_label.place(x=390, y=105)
        self.item_selector.place(x=365, y=130)

        self.ability_label.place(x=380, y=185)
        self.ability_selector.place(x=365, y=210)

    def on_item_change(self, choice: str):
        self.pokemon_tab.selected_pokemon.item = Item[choice.upper().replace(' ', '_')]
        self.update_utilities()

    def get_mega_stone(self, pokemon_name: str):
        mega_stone_name = pokemon_name.upper() + "ITE"
        if mega_stone_name in Item.__members__:
            return Item[mega_stone_name]
        elif mega_stone_name + "_X" in Item.__members__:
            return Item[mega_stone_name + "_X"]
        elif mega_stone_name + "_Y" in Item.__members__:
            return Item[mega_stone_name + "_Y"]
        else:
            return None

    def update_utilities(self):
        self.item_image = customtkinter.CTkImage(Image.open(f"../Images/Item_sprites/{self.pokemon_tab.selected_pokemon.item.name.lower().replace(' ', '-')}.png"), size=(50, 50))
        self.item_image_label.configure(image=self.item_image)
        self.item_image_label.image = self.item_image

    def destroy_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()
    def update_moves_frame(self):
        self.destroy_widgets()
        self.create_moves_widgets()
        self.create_utilities_widgets()
        self.place_widgets()


class MoveLine:
    def __init__(self, master, pokemon_tab: PokemonTab, y_position: int, index: int):
        self.master = master
        self.pokemon_tab = pokemon_tab
        self.y_position = y_position
        self.index = index

        self.create_move_line()
        self.place_widgets()

    def create_move_line(self):
        self.move_name_label = customtkinter.CTkLabel(self.master, text=f"Move {self.index} : ", font=("Arial", 15), anchor="e", width=80)

        self.move_selector = customtkinter.CTkComboBox(self.master, values=[move.name for move in self.pokemon_tab.selected_pokemon.move_pool],
                                                       corner_radius=10, state="readonly", command=self.on_move_change)

        self.category_image = customtkinter.CTkImage(Image.open("../Images/Misc/none.png"), size=(30, 15))
        self.move_category_label = customtkinter.CTkLabel(self.master, text="", image=self.category_image)

        self.type_image = customtkinter.CTkImage(Image.open("../Images/Misc/none.png"), size=(40, 15))
        self.move_type_image_label = customtkinter.CTkLabel(self.master, text="", image=self.type_image)

    def place_widgets(self):
        self.move_name_label.place(x=0, y=self.y_position)
        self.move_selector.place(x=80, y=self.y_position)
        self.move_category_label.place(x=232, y=self.y_position)
        self.move_type_image_label.place(x=280, y=self.y_position)

    def on_move_change(self, choice: str):
        move = [move for move in self.pokemon_tab.selected_pokemon.move_pool if move.name == choice][0]
        self.move_category_label.configure(image=customtkinter.CTkImage(Image.open(f"../Images/Misc/move-{move.category.name.lower()}.png"), size=(35, 17)))
        self.move_type_image_label.configure(image=customtkinter.CTkImage(Image.open(f"../Images/Types/{move.type.name.lower()}.png"), size=(46, 17)))


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
            self.remaining_ev_counter_label.configure(text=f"Remaining EVs: {remaining_ev}", text_color="white")
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
            self.configure(border_width=0)
            self.remaining_ev_counter_label.lift()
        else:
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
        self.remaining_ev_counter_label.lower()

    def destroy_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    def update_ev_vars(self):
        self.hp_ev_var = customtkinter.StringVar(value="0")
        self.attack_ev_var = customtkinter.StringVar(value="0")
        self.defense_ev_var = customtkinter.StringVar(value="0")
        self.spe_attack_ev_var = customtkinter.StringVar(value="0")
        self.spe_defense_ev_var = customtkinter.StringVar(value="0")
        self.speed_ev_var = customtkinter.StringVar(value="0")

    def update_stats_frame(self):
        self.destroy_widgets()
        self.update_ev_vars()
        self.create_widgets()
        self.place_widgets()
        self.check_remaining_ev()


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
