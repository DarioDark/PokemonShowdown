from PIL import Image
import customtkinter as ctk
import json

from PokemonListConsole import AVAILABLE_POKEMONS, Pokemon, BasePokemonList
from ItemConsole import Item, ITEM_LIST
from CTkSeparator import CTkSeparator
from CTkMessagebox import CTkMessagebox
from AbilityConsole import Ability
from MoveConsole import Move


class TeambuilderInterface:
    def __init__(self, master: ctk.CTk | ctk.CTkToplevel):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.master: ctk.CTk = master

        self.master.title("Teambuilder")
        self.master.resizable(False, False)
        self.master.update_idletasks()  # Update window geometry

        width = 1000
        height = 750

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.master.geometry(f"{width}x{height}+{x}+{y}")

        self.master.attributes('-topmost', 1)

        self.mainframe = ctk.CTkFrame(self.master)
        self.mainframe.pack(fill=ctk.BOTH, expand=True)

        self.create_tabs()

    def create_tabs(self):
        self.tabs = ctk.CTkTabview(self.mainframe, height=700, width=800, corner_radius=20)
        self.tabs.pack(pady=10)
        self.tabs_objects = [PokemonTab(self.tabs, self, i) for i in range(6)]


class PokemonTab:
    def __init__(self, master, app, index: int):
        self.master = master
        self.app = app
        self.index = index
        self.tab = self.master.add(f"  Pokemon {index + 1}  ")

        self.create_frames()
        self.place_frames()

    @property
    def selected_pokemon(self) -> Pokemon:
        return self.pokemon_frame.selected_pokemon

    @property
    def selected_moves(self) -> list[Move]:
        return self.moves_frame.selected_moves

    @property
    def selected_item(self) -> Item:
        return self.moves_frame.selected_item

    @property
    def selected_ability(self) -> Ability:
        return self.moves_frame.selected_ability

    def create_frames(self) -> None:
        self.pokemon_frame = PokemonFrame(self.tab, self)
        self.moves_frame = MovesFrame(self.tab, self)
        self.stats_frame = StatsFrame(self.tab, self)

    def place_frames(self) -> None:
        # Layout
        self.tab.grid_rowconfigure(0, weight=1)
        self.tab.grid_rowconfigure(1, weight=2)
        self.tab.grid_columnconfigure(0, weight=1)
        self.tab.grid_columnconfigure(1, weight=2)

        self.pokemon_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.moves_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.stats_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

    def update_frames(self) -> None:
        self.stats_frame.update_stats_frame()
        self.moves_frame.update_moves_frame()

    def create_moves_frame(self) -> None:
        self.moves_frame = ctk.CTkFrame(self.tab, corner_radius=20)
        self.moves_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.moves_frame.grid_propagate(False)

    def check_validity(self) -> bool:
        if not self.selected_pokemon:
            print(self.index, "No pokemon selected")
            return False
        if self.stats_frame.remaining_ev < 0:
            print(self.index, "Remaining EVs are negative")
            return False
        if len(self.selected_moves) != 4:
            print(self.index, "Not enough moves selected")
            return False
        if self.selected_item == Item.NONE:
            print(self.index, "No item selected")
            return False
        if self.selected_ability == Ability.NONE:
            print(self.index, "No ability selected")
            return False
        return True


class PokemonFrame(ctk.CTkFrame):
    def __init__(self, master, pokemon_tab: PokemonTab):
        super().__init__(master, corner_radius=20, width=20, height=30)
        self.master = master
        self.pokemonTab: PokemonTab = pokemon_tab

        self.selected_pokemon = None

        self.create_widgets()
        self.place_widgets()

    def create_widgets(self) -> None:
        self.pokemon_frame_title = ctk.CTkLabel(self, text="Pokemon", font=("Arial", 20, "bold"), corner_radius=35)
        self.image = ctk.CTkImage(dark_image=Image.open("../Images/Static_sprites/empty-sprite.png"), size=(124, 124))
        self.pokemon_label = ctk.CTkLabel(self, text="", image=self.image)
        self.pokemon_label.image = self.image

        self.pokemon_var = ctk.StringVar(value="None")
        self.pokemon_selector = ctk.CTkComboBox(self,
                                                values=AVAILABLE_POKEMONS,
                                                corner_radius=10,
                                                state="readonly",
                                                variable=self.pokemon_var,
                                                command=self.on_pokemon_change)

    def place_widgets(self) -> None:
        # Layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.pokemon_frame_title.place(x=37, y=10)
        self.pokemon_label.place(x=33, y=50)
        self.pokemon_selector.place(x=22, y=210)

    def on_pokemon_change(self, choice: str) -> None:
        self.selected_pokemon = BasePokemonList[choice.upper()].value
        self.update_pokemon_frame()
        self.pokemonTab.update_frames()
        #self.pokemonTab.app.team_recap_tab.update_pokemon_frame(choice, self.pokemonTab.index)

        # Reset the EVs
        self.hp_ev_var = ctk.StringVar(value="0")
        self.attack_ev_var = ctk.StringVar(value="0")
        self.defense_ev_var = ctk.StringVar(value="0")
        self.spe_attack_ev_var = ctk.StringVar(value="0")
        self.spe_defense_ev_var = ctk.StringVar(value="0")
        self.speed_ev_var = ctk.StringVar(value="0")

    def update_pokemon_frame(self) -> None:
        image_path = f"../Images/Static_Sprites/{self.selected_pokemon.name.lower()}.png"
        self.image = ctk.CTkImage(Image.open(image_path), size=(124, 124))
        self.pokemon_label.configure(image=self.image)
        self.pokemon_label.image = self.image

class TeamRecapLine:
    def __init__(self, master, pokemon_tab: PokemonTab, y_position: int):
        self.master = master
        self.pokemon_tab = pokemon_tab
        self.y_position = y_position

        self.create_recap_line()
        self.place_widgets()

    def create_recap_line(self):
        self.pokemon_name_label = ctk.CTkLabel(self.master, text=self.pokemon_tab.selected_pokemon.name, font=("Arial", 15), anchor="e", width=80)
        self.pokemon_level_label = ctk.CTkLabel(self.master, text="Level 50", font=("Arial", 15))
        self.pokemon_item_label = ctk.CTkLabel(self.master, text=self.pokemon_tab.selected_item.name, font=("Arial", 15))
        self.pokemon_ability_label = ctk.CTkLabel(self.master, text=self.pokemon_tab.selected_ability.name, font=("Arial", 15))

    def place_widgets(self):
        self.pokemon_name_label.place(x=0, y=self.y_position)
        self.pokemon_level_label.place(x=80, y=self.y_position)
        self.pokemon_item_label.place(x=160, y=self.y_position)
        self.pokemon_ability_label.place(x=240, y=self.y_position)


class MovesFrame(ctk.CTkFrame):
    def __init__(self, master, pokemon_tab: PokemonTab):
        super().__init__(master, corner_radius=20)
        self.master = master
        self.pokemon_tab: PokemonTab = pokemon_tab

        self.selected_item: Item = Item.NONE
        self.selected_ability: Ability = Ability.NONE

    @property
    def selected_moves(self) -> list[Move]:
        if not self.move_lines:
            return []
        return [move_line.selected_move for move_line in self.move_lines if move_line.selected_move is not None]

    def create_moves_widgets(self) -> None:
        self.moves_title = ctk.CTkLabel(self, text="Moves", font=("Arial", 20, "bold"), corner_radius=35)
        self.move_category_text_label = ctk.CTkLabel(self, text="Class", font=("Arial", 12, "italic"))
        self.move_type_text_label = ctk.CTkLabel(self, text="Type", font=("Arial", 12, "italic"))
        self.move_lines = [MoveLine(self, self.pokemon_tab, 80 + i * 40, i + 1) for i in range(4)]

    def create_utilities_widgets(self) -> None:
        self.utilities_title = ctk.CTkLabel(self, text="Utilities", font=("Arial", 20, "bold"), corner_radius=35)

        self.vertical_separator = CTkSeparator(self, orient="vertical", fg_color="#1A1A1A", length=3)
        self.horizontal_separator = CTkSeparator(self, orient="horizontal", fg_color="#1A1A1A", length=3)

        self.item_image = ctk.CTkImage(Image.open("../Images/Item_sprites/poke-ball.png"), size=(50, 50))
        self.item_image_label = ctk.CTkLabel(self, text="", image=self.item_image)
        self.item_image_label.image = self.item_image

        self.item_label = ctk.CTkLabel(self, text="Select an item :", font=("Arial", 12, "italic"))
        mega_stones: list[Item] = self.get_mega_stone(self.pokemon_tab.selected_pokemon.name)
        full_item_list = ITEM_LIST + mega_stones

        self.item_selector = ctk.CTkComboBox(self, values=full_item_list, corner_radius=10, state="readonly", command=self.on_item_change)

        self.ability_label = ctk.CTkLabel(self, text="Select an ability :", font=("Arial", 12, "italic"))
        self.ability_selector = ctk.CTkComboBox(self, values=[ability.name.capitalize().replace('_', ' ') for ability in self.pokemon_tab.selected_pokemon.ability_pool],
                                                corner_radius=10, state="readonly", command=self.on_ability_change)

    def place_widgets(self) -> None:
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

    def on_item_change(self, choice: str) -> None:
        self.pokemon_tab.selected_pokemon.item = Item[choice.upper().replace(' ', '_')]
        self.update_utilities()
        self.selected_item = Item[choice.upper().replace(' ', '_')]

    def get_mega_stone(self, pokemon_name: str) -> list[Item]:
        if pokemon_name == "Gengar":
            mega_stones = [Item.GENGARITE.value]
        elif pokemon_name == "Alakazam":
            mega_stones = [Item.ALAKAZITE.value]
        elif pokemon_name == "Charizard":
            mega_stones = [Item.CHARIZARDITE_X.value, Item.CHARIZARDITE_Y.value]
        elif pokemon_name == "Swampert":
            mega_stones = [Item.SWAMPERTITE.value]
        elif pokemon_name == "Salamence":
            mega_stones = [Item.SALAMENCITE.value]
        elif pokemon_name == "Garchomp":
            mega_stones = [Item.GARCHOMPITE.value]
        elif pokemon_name == "Mawile":
            mega_stones = [Item.MAWILITE.value]
        elif pokemon_name == "Lopunny":
            mega_stones = [Item.LOPUNNITE.value]
        elif pokemon_name == "Blaziken":
            mega_stones = [Item.BLAZIKENITE.value]
        elif pokemon_name == "Diancie":
            mega_stones = [Item.DIANCITE.value]
        elif pokemon_name == "Pinsir":
            mega_stones = [Item.PINSIRITE.value]
        elif pokemon_name == "Scizor":
            mega_stones = [Item.SCIZORITE.value]
        elif pokemon_name == "Tyranitar":
            mega_stones = [Item.TYRANITARITE.value]
        else:
            mega_stones = []
        return mega_stones

    def on_ability_change(self, choice: str) -> None:
        self.selected_ability: Ability = Ability[choice.upper().replace(' ', '_')]

    def update_utilities(self) -> None:
        self.item_image = ctk.CTkImage(Image.open(f"../Images/Item_sprites/{self.pokemon_tab.selected_pokemon.item.name.lower().replace(' ', '-')}.png"), size=(50, 50))
        self.item_image_label.configure(image=self.item_image)
        self.item_image_label.image = self.item_image

    def destroy_widgets(self) -> None:
        for widget in self.winfo_children():
            widget.destroy()

    def update_moves_frame(self) -> None:
        self.destroy_widgets()
        self.create_moves_widgets()
        self.create_utilities_widgets()
        self.place_widgets()


class MoveLine:
    def __init__(self, master: MovesFrame, pokemon_tab: PokemonTab, y_position: int, index: int):
        self.master: MovesFrame = master
        self.pokemon_tab: PokemonTab = pokemon_tab
        self.y_position: int = y_position
        self.index: int = index

        self.selected_move: Move | None = None

        self.create_move_line()
        self.place_widgets()

    def create_move_line(self) -> None:
        self.move_name_label = ctk.CTkLabel(self.master, text=f"Move {self.index} : ", font=("Arial", 15), anchor="e", width=80)

        self.move_selector = ctk.CTkComboBox(self.master, values=[move.name for move in self.pokemon_tab.selected_pokemon.move_pool],
                                             corner_radius=10, state="readonly", command=self.on_move_change)

        self.category_image = ctk.CTkImage(Image.open("../Images/Misc/none.png"), size=(30, 15))
        self.move_category_label = ctk.CTkLabel(self.master, text="", image=self.category_image)

        self.type_image = ctk.CTkImage(Image.open("../Images/Misc/none.png"), size=(40, 15))
        self.move_type_image_label = ctk.CTkLabel(self.master, text="", image=self.type_image)

    def place_widgets(self) -> None:
        self.move_name_label.place(x=0, y=self.y_position)
        self.move_selector.place(x=80, y=self.y_position)
        self.move_category_label.place(x=232, y=self.y_position)
        self.move_type_image_label.place(x=280, y=self.y_position)

    def on_move_change(self, choice: str) -> None:
        move = [move for move in self.pokemon_tab.selected_pokemon.move_pool if move.name == choice][0]
        self.move_category_label.configure(image=ctk.CTkImage(Image.open(f"../Images/Misc/move-{move.category.name.lower()}.png"), size=(35, 17)))
        self.move_type_image_label.configure(image=ctk.CTkImage(Image.open(f"../Images/Types/{move.type.name.lower()}.png"), size=(46, 17)))
        self.selected_move = move


class StatsFrame(ctk.CTkFrame):
    def __init__(self, master: TeambuilderInterface, pokemon_tab: PokemonTab):
        super().__init__(master, corner_radius=20)
        self.master: TeambuilderInterface = master
        self.pokemon_tab: PokemonTab = pokemon_tab

        self.update_ev_vars()

    @property
    def remaining_ev(self) -> int:
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
        return remaining_ev

    @property
    def selected_pokemon_hp(self) -> int:
        if self.hp_ev_var.get() == '':
            self.hp_ev_var.set('0')
        if self.pokemon_tab.selected_pokemon:
            return self.pokemon_tab.selected_pokemon.max_hp + int(self.hp_ev_var.get()) // 4

    @property
    def selected_pokemon_attack(self) -> int:
        if self.attack_ev_var.get() == '':
            self.attack_ev_var.set('0')
        if self.pokemon_tab.selected_pokemon:
            return self.pokemon_tab.selected_pokemon.attack_stat + int(self.attack_ev_var.get()) // 4

    @property
    def selected_pokemon_defense(self) -> int:
        if self.defense_ev_var.get() == '':
            self.defense_ev_var.set('0')
        if self.pokemon_tab.selected_pokemon:
            return self.pokemon_tab.selected_pokemon.defense_stat + int(self.defense_ev_var.get()) // 4

    @property
    def selected_pokemon_spe_attack(self) -> int:
        if self.spe_attack_ev_var.get() == '':
            self.spe_attack_ev_var.set('0')
        if self.pokemon_tab.selected_pokemon:
            return self.pokemon_tab.selected_pokemon.special_attack_stat + int(self.spe_attack_ev_var.get()) // 4

    @property
    def selected_pokemon_spe_defense(self) -> int:
        if self.spe_defense_ev_var.get() == '':
            self.spe_defense_ev_var.set('0')
        if self.pokemon_tab.selected_pokemon:
            return self.pokemon_tab.selected_pokemon.special_defense_stat + int(self.spe_defense_ev_var.get()) // 4

    @property
    def selected_pokemon_speed(self) -> int:
        if self.speed_ev_var.get() == '':
            self.speed_ev_var.set('0')
        if self.pokemon_tab.selected_pokemon:
            return self.pokemon_tab.selected_pokemon.speed_stat + int(self.speed_ev_var.get()) // 4

    def check_remaining_ev(self) -> None:
        if self.remaining_ev < 0:
            self.remaining_ev_counter_label.lower()
            self.evs_max_exceeded_label.lift()  # Show the label
            self.configure(border_color="red", border_width=2)
        elif self.remaining_ev == 0:
            self.remaining_ev_counter_label.configure(text="EVs maximum reached!", text_color="green")
            self.configure(border_width=0)
            self.remaining_ev_counter_label.lift()
        else:
            self.remaining_ev_counter_label.configure(text=f"Remaining EVs: {self.remaining_ev}", text_color="white")
            self.remaining_ev_counter_label.lift()
            self.evs_max_exceeded_label.lower()  # Hide the label
            self.configure(border_width=0)

    def create_stat_lines(self) -> None:
        self.stat_lines = [StatLine(self, self.pokemon_tab, "HP", self.pokemon_tab.selected_pokemon.max_hp, self.hp_ev_var, 90),
                           StatLine(self, self.pokemon_tab, "Attack", self.pokemon_tab.selected_pokemon.attack_stat, self.attack_ev_var, 120),
                           StatLine(self, self.pokemon_tab, "Defense", self.pokemon_tab.selected_pokemon.defense_stat, self.defense_ev_var, 150),
                           StatLine(self, self.pokemon_tab, "Sp. Atk.", self.pokemon_tab.selected_pokemon.special_attack_stat, self.spe_attack_ev_var, 180),
                           StatLine(self, self.pokemon_tab, "Sp. Def.", self.pokemon_tab.selected_pokemon.special_defense_stat, self.spe_defense_ev_var, 210),
                           StatLine(self, self.pokemon_tab, "Speed", self.pokemon_tab.selected_pokemon.speed_stat, self.speed_ev_var, 240)]

    def create_widgets(self) -> None:
        self.stats_frame_title = ctk.CTkLabel(self, text="Stats", font=("Arial", 20, "bold"), corner_radius=35)
        self.base_label = ctk.CTkLabel(self, text="Base", font=("Arial", 13, "italic"))
        self.ev_label = ctk.CTkLabel(self, text="EVs", font=("Arial", 12, "italic"))
        self.total_label = ctk.CTkLabel(self, text="Total", font=("Arial", 13, "italic"))

        # Stats alert labels
        self.remaining_ev_counter_label = ctk.CTkLabel(self, text=f"Remaining EVs: 508", font=("Arial", 10, "bold", "italic"),
                                                       text_color="white")

        self.evs_max_exceeded_label = ctk.CTkLabel(self, text="EVs maximum exceeded!", font=("Arial", 10, "bold", "italic"), text_color="red",
                                                   compound="left", corner_radius=30, padx=5,
                                                   image=ctk.CTkImage(Image.open("../Images/red-warning-icon.png"), size=(20, 20)))

        self.create_stat_lines()

    def place_widgets(self) -> None:
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

    def destroy_widgets(self) -> None:
        for widget in self.winfo_children():
            widget.destroy()

    def update_ev_vars(self) -> None:
        self.hp_ev_var = ctk.StringVar(value="0")
        self.attack_ev_var = ctk.StringVar(value="0")
        self.defense_ev_var = ctk.StringVar(value="0")
        self.spe_attack_ev_var = ctk.StringVar(value="0")
        self.spe_defense_ev_var = ctk.StringVar(value="0")
        self.speed_ev_var = ctk.StringVar(value="0")

    def update_stats_frame(self) -> None:
        self.destroy_widgets()
        self.update_ev_vars()
        self.create_widgets()
        self.place_widgets()
        self.check_remaining_ev()


class StatLine:

    stat_to_method: dict[str: str] = {
        "HP": "selected_pokemon_hp",
        "Attack": "selected_pokemon_attack",
        "Defense": "selected_pokemon_defense",
        "Sp. Atk.": "selected_pokemon_spe_attack",
        "Sp. Def.": "selected_pokemon_spe_defense",
        "Speed": "selected_pokemon_speed"
    }

    def __init__(self, master: StatsFrame, pokemon_tab: PokemonTab, stat_name: str, base_stat: int, ev_var: ctk.StringVar, y_position: int):
        self.master: StatsFrame = master
        self.pokemon_tab: PokemonTab = pokemon_tab
        self.stat_name: str = stat_name
        self.base_stat: int = base_stat
        self.ev_var: ctk.StringVar = ev_var
        self.y_position: int = y_position

        self.create_stat_line()
        self.place_widgets()

    @property
    def selected_pokemon_stat(self) -> int:
        return getattr(self.master, self.stat_to_method[self.stat_name])

    def create_stat_line(self) -> None:
        self.stat_name_label = ctk.CTkLabel(self.master, text=self.stat_name, font=("Arial", 15), anchor="e", width=80)

        self.base_stat_number_label = ctk.CTkLabel(self.master, text=str(self.base_stat), font=("Arial", 15))

        self.progress_bar = ctk.CTkProgressBar(self.master,
                                               width=200,
                                               determinate_speed=1,
                                               progress_color="green")
        self.progress_bar.set(self.base_stat / 500)
        self.config_progress_bar_color()

        self.ev_var.trace_add("write", self.entry_change)
        self.ev_entry = ctk.CTkEntry(self.master, width=40, font=("Arial", 15), textvariable=self.ev_var)

        self.slider = ctk.CTkSlider(self.master,
                                    from_=0,
                                    to=min(252, max(self.master.remaining_ev, 0)),
                                    orientation=ctk.HORIZONTAL,
                                    width=200,
                                    command=self.slider_change,
                                    number_of_steps=63)
        self.slider.set(0)

        self.total_label = ctk.CTkLabel(self.master, text=str(self.base_stat), font=("Arial", 15))

    def place_widgets(self) -> None:
        self.stat_name_label.place(x=25, y=self.y_position)
        self.base_stat_number_label.place(x=125, y=self.y_position)
        self.progress_bar.place(x=155, y=self.y_position + 10)
        self.ev_entry.place(x=370, y=self.y_position)
        self.slider.place(x=415, y=self.y_position + 5)
        self.total_label.place(x=625, y=self.y_position)

    def slider_change(self, value) -> None:
        value = int(value)
        if self.master.remaining_ev <= 0 and value > int(self.ev_var.get()):
            self.slider.set(int(self.ev_var.get()))
            return

        self.ev_var.set(str(value))
        self.slider.set(value)

        self.progress_bar.set(self.selected_pokemon_stat / 500)
        self.master.check_remaining_ev()

    def entry_change(self, *args) -> None:
        value = self.ev_var.get()
        self.config_progress_bar_color()

        if self.master.remaining_ev > 0:
            if value == '':
                value = '0'
                self.ev_var.set('')

        self.slider_change(int(value))
        self.total_label.configure(text=self.selected_pokemon_stat)

    def config_progress_bar_color(self) -> None:
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


class TeamRecapTab:
    def __init__(self, master: ctk.CTkTabview, app: TeambuilderInterface):
        self.master: ctk.CTkTabview = master
        self.app: TeambuilderInterface = app
        self.tab: ctk.CTkFrame = self.master.add("  Team Recap  ")

        self.create_widgets()
        self.place_widgets()

    def create_widgets(self) -> None:
        self.team_recap_title = ctk.CTkLabel(self.tab, text="Team Recap", font=("Arial", 20, "bold"), corner_radius=35)
        self.pokemon_recap_frames: list[PokemonRecapFrame] = [PokemonRecapFrame(self.tab, self, 40 + i * 240, 80, 1 + i) for i in range(3)]
        self.pokemon_recap_frames.extend([PokemonRecapFrame(self.tab, self, 40 + i * 240, 340, 4 + i) for i in range(3)])
        self.validate_team_button = ctk.CTkButton(self.tab, text="Validate Team", corner_radius=20, command=self.validate_team, font=("Arial", 15))

    def place_widgets(self) -> None:
        self.team_recap_title.place(x=310, y=10)
        self.validate_team_button.place(x=190, y=585)

    def update_pokemon_frame(self, choice: str, tab_index: int) -> None:
        self.pokemon_recap_frames[tab_index].update_image(choice)

    def total_validity(self) -> bool:
        return sum([pokemon_tab.check_validity() for pokemon_tab in self.app.tabs_objects]) == 6

    def validate_team(self) -> None:
        if self.total_validity():
            invalid_pokemons = ", ".join([f"Pokemon {pokemon_tab.index + 1}" for pokemon_tab in self.app.tabs_objects if not pokemon_tab.check_validity()])
            self.validate_team_message_box = CTkMessagebox(self.tab, title="Team Validation", message=f"These Pokemons are not valid : {invalid_pokemons}", icon="cancel", corner_radius=20)
        else:
            self.validate_team_message_box = CTkMessagebox(self.tab, title="Team Validation", message="Your team is valid!", icon="check", corner_radius=20, option_1="Ok", option_2="Save team")
            if self.validate_team_message_box.get() == "Save team":
                self.save_team()

    def save_team(self) -> None:
        self.erase_json_file()
        team = []
        for tab in self.app.tabs_objects:
            if tab.selected_pokemon:
                team.append({
                    "pokemon": tab.selected_pokemon.name,
                    "moves": [move.name for move in tab.selected_moves],
                    "item": tab.selected_item.name,
                    "ability": tab.selected_ability.name,
                    "evs": {
                        "hp": int(tab.stats_frame.hp_ev_var.get()),
                        "attack": int(tab.stats_frame.attack_ev_var.get()),
                        "defense": int(tab.stats_frame.defense_ev_var.get()),
                        "special_attack": int(tab.stats_frame.spe_attack_ev_var.get()),
                        "special_defense": int(tab.stats_frame.spe_defense_ev_var.get()),
                        "speed": int(tab.stats_frame.speed_ev_var.get())
                    }
                })
        with open("team.json", "w") as f:
            json.dump(team, f)

    @staticmethod
    def erase_json_file() -> None:
        with open("team.json", "w") as f:
            pass


class CurrentTeamRecapLine(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkFrame, recap_tab: TeamRecapTab, x_position: int, y_position: int, index: int):
        super().__init__(master, corner_radius=20, width=200, height=220)
        self.master: ctk.CTkFrame = master
        self.recap_tab: TeamRecapTab = recap_tab
        self.x_position: int = x_position
        self.y_position: int = y_position
        self.index: int = index

        self.place(x=x_position, y=y_position)
        self.create_widgets()
        self.place_widgets()

    def create_widgets(self) -> None:
        self.pokemon_frame_title = ctk.CTkLabel(self, text=f"Pokemon {self.index}", font=("Arial", 20, "bold"), corner_radius=35)
        self.pokemon_image = ctk.CTkImage(Image.open("../Images/Static_sprites/empty-sprite.png"), size=(124, 124))
        self.pokemon_image_label = ctk.CTkLabel(self, text="", image=self.pokemon_image)

    def place_widgets(self) -> None:
        self.pokemon_frame_title.place(x=37, y=10)
        self.pokemon_image_label.place(x=33, y=70)

    def update_image(self, choice: str) -> None:
        self.pokemon_image = ctk.CTkImage(Image.open(f"../Images/Static_sprites/{choice.lower()}.png"), size=(124, 124))
        self.pokemon_image_label.configure(image=self.pokemon_image)
        self.pokemon_image_label.image = self.pokemon_image

    def destroy_widgets(self) -> None:
        for widget in self.winfo_children():
            widget.destroy()

    def update_pokemon_frame(self, choice: str) -> None:
        self.destroy_widgets()
        self.create_widgets()
        self.update_image(choice)
        self.place_widgets()


class PokemonRecapImage:
    pass
    

def main():
    app = ctk.CTk()
    t = TeambuilderInterface(app)
    t.master.mainloop()


if __name__ == "__main__":
    main()
