from math import floor
from copy import deepcopy
from MoveConsole import *
from ZMoveConsole import ZMove
from StatusConsole import PrimeStatus, SubStatus
from EnvironmentConsole import EnvironmentElements, EnvironmentClass
from AbilityConsole import Ability
from ItemConsole import Item


class Pokemon:
    def __init__(self, name: str,
                 hp_stat: int,
                 attack_stat: int,
                 defense_stat: int,
                 special_attack_stat: int,
                 special_defense_stat: int,
                 speed_stat: int,
                 types: 'list[Type]',
                 move_pool: list[Move],
                 ability_pool: list[Ability],
                 mega_evolution_stats: list[tuple[int, int, int, int, int, Ability, list[Type]]] | None = None) -> None:

        self.name = name
        self.lvl = 100

        # Stats
        self.current_hp: int = hp_stat
        self.max_hp: int = hp_stat
        self.attack_stat: int = attack_stat
        self.special_attack_stat: int = special_attack_stat
        self.defense_stat: int = defense_stat
        self.special_defense_stat: int = special_defense_stat
        self.speed_stat: int = speed_stat

        # EVs
        self.hp_evs: int = 0
        self.attack_evs: int = 0
        self.defense_evs: int = 0
        self.special_attack_evs: int = 0
        self.special_defense_evs: int = 0
        self.speed_evs: int = 0

        # Stats Boosts
        self.attack_boosts: int = 0
        self.defense_boosts: int = 0
        self.special_attack_boosts: int = 0
        self.special_defense_boosts: int = 0
        self.speed_boosts: int = 0

        # Ability and item
        self.ability_pool: list[Ability] = ability_pool
        self.ability: Ability = Ability.NONE
        self.item: Item = Item.NONE

        # Types
        self.types: list[Type] = types
        self.immunities: list[Type] = self.get_types_immunities()
        self.weaknesses: list[Type] = self.calculate_weaknesses()
        self.resistances: list[Type] = self.calculate_resistances()

        # Status
        self.status: PrimeStatus = PrimeStatus.NORMAL
        self.sub_status: list[SubStatus] = []
        self.nbr_turn_severe_poison: int = 0
        self.sleep_turns: int = 0

        self.move_pool = move_pool
        self.moves: list[Move] = []
        if self.ability == Ability.NO_GUARD:
            for move in self.moves:
                move.accuracy = 100
        elif self.ability == Ability.VICTORY_STAR:
            for move in self.moves:
                move.accuracy = move.base_accuracy * 1.1
        self.last_used_move = None
        self.environment: EnvironmentClass | None = None
        self.mega_evolution_stats: list[tuple[int, int, int, int, int, Ability, list[Type]]] = mega_evolution_stats

    def __getstate__(self):
        return {
            'name': self.name,
            'max_hp': self.max_hp,
            'attack_stat': self.attack_stat,
            'special_attack_stat': self.special_attack_stat,
            'defense_stat': self.defense_stat,
            'special_defense_stat': self.special_defense_stat,
            'speed_stat': self.speed_stat,
            'hp_evs': self.hp_evs,
            'attack_evs': self.attack_evs,
            'defense_evs': self.defense_evs,
            'special_attack_evs': self.special_attack_evs,
            'special_defense_evs': self.special_defense_evs,
            'speed_evs': self.speed_evs,
            'ability': self.ability.name,
            'item': self.item.name,
            'types': [pokemon_type.name for pokemon_type in self.types],
            'moves': [move.__getstate__() for move in self.moves],
            'environment': self.environment,
            'mega_evolution_stats': None if self.mega_evolution_stats is None else [[stat if isinstance(stat, int) else stat.name if not isinstance(stat, list) else [item.name for item in stat] for stat in stats] for stats in self.mega_evolution_stats]
        }
        
    def __setstate__(self, state):
        self.name = state['name']
        self.lvl = 100
        self.current_hp = state['max_hp']
        self.max_hp = state['max_hp']
        self.attack_stat = state['attack_stat']
        self.special_attack_stat = state['special_attack_stat']
        self.defense_stat = state['defense_stat']
        self.special_defense_stat = state['special_defense_stat']
        self.speed_stat = state['speed_stat']
        self.hp_evs = state['hp_evs']
        self.attack_evs = state['attack_evs']
        self.defense_evs = state['defense_evs']
        self.special_attack_evs = state['special_attack_evs']
        self.special_defense_evs = state['special_defense_evs']
        self.speed_evs = state['speed_evs']
        self.attack_boosts = 0
        self.defense_boosts = 0
        self.special_attack_boosts = 0
        self.special_defense_boosts = 0
        self.speed_boosts = 0
        self.ability_pool = []
        self.ability = Ability[state['ability'].upper()]
        self.item = Item[state['item'].upper()]
        self.types = [Type[type_name.upper()] for type_name in state['types']]
        self.immunities = self.get_types_immunities()
        self.weaknesses = self.calculate_weaknesses()
        self.resistances = self.calculate_resistances()
        self.status = PrimeStatus.NORMAL
        self.sub_status = []
        self.nbr_turn_severe_poison = 0
        self.sleep_turns = 0
        self.move_pool = []
        self.moves = []
        for attack_state in state['moves']:
            attack = Move(
                name=attack_state['name'],
                move_type=Type[attack_state['type']],
                category=MoveCategory[attack_state['category']],
                power=attack_state['power'],
                base_accuracy=attack_state['base_accuracy'],
                max_pp=attack_state['max_pp'],
                secondary_effect=SecondaryEffects[attack_state['secondary_effect']].value,
                target=attack_state['target'],
                priority=attack_state['priority'],
                contact_move=attack_state['contact_move'],
                bullet_move=attack_state['bullet_move'],
                sound_move=attack_state['sound_move']
            )
            self.moves.append(attack)
        self.last_used_move = None
        self.environment = state['environment']
        if state['mega_evolution_stats'] is None:
            self.mega_evolution_stats = None
        else:
            print(state['mega_evolution_stats'])
            mega_evolution_stats = []
            for stat_list in state['mega_evolution_stats']:
                temp_stat_list = []
                for stat in stat_list:
                    if isinstance(stat, str):
                        stat = Ability[stat.upper()]
                    elif isinstance(stat, list):
                        stat = [Type[stat_name.upper()] for stat_name in stat]
                    temp_stat_list.append(stat)
                mega_evolution_stats.append(tuple(temp_stat_list))
            self.mega_evolution_stats = mega_evolution_stats

    def __repr__(self) -> str:
        """Returns a string representation of the pokemon, with its name, types, HP and current status, greyed out if the pokemon is fainted.

        :return: A string representation of the pokemon
        """
        # If the pokemon is fainted, grey out the text
        if self.current_hp <= 0:
            for pokemon_type in self.types:
                pokemon_type.value.color = "dark_grey"
            types_str = colored(" / ", 'dark_grey').join([str(pokemon_type.value) for pokemon_type in self.types])
            full_str = colored(f"{self.name} : {types_str} ~ ", 'dark_grey') + colored(f"{self.current_hp}", 'red') + colored(f"/{self.max_hp}", 'dark_grey') + colored("HP", 'dark_grey')
            for pokemon_type in self.types:
                pokemon_type.value.color = pokemon_type.value.default_color

            return full_str

        # If the pokemon is not fainted, color the text
        health_colors = {100: "green", 75: "light_green",  50: "yellow", 25: "light_red", 0: "red"}
        health_percentage = self.get_current_hp_percentage()
        for key in sorted(health_colors.keys(), reverse=True):
            if health_percentage >= key:
                color = health_colors[key]
                break
        types_str = " / ".join([str(pokemon_type.value) for pokemon_type in self.types])

        return f"{self.name} : {types_str} ~ {colored(self.current_hp, color)}/{self.max_hp} HP"

    @property
    def mega_name(self) -> str:
        if self.mega_evolution_stats:
            if self.name == "Charizard":
                if self.item == Item.CHARIZARDITE_X:
                    return f"Mega {self.name} X"
                elif self.item == Item.CHARIZARDITE_Y:
                    return f"Mega {self.name} Y"
            else:
                return f"Mega {self.name}"

    @property
    def attack(self) -> int:
        """Returns the attack of the pokemon, taking into account the attack boosts."""
        attack_stat = self.attack_stat
        # Ability
        if self.ability == Ability.HUGE_POWER or self.ability == Ability.PURE_POWER:
            attack_stat *= 2
        elif self.ability == Ability.GUTS and self.status != PrimeStatus.NORMAL:
            attack_stat *= 2
        # Object
        if self.item == Item.CHOICE_BAND:
            attack_stat *= 1.5
        # Boosts
        if self.attack_boosts > 0:
            return attack_stat + (self.attack_boosts * self.attack_stat // 2)
        elif self.attack_boosts < 0:
            return round(attack_stat * self.malus_to_percentage(self.attack_boosts))
        return attack_stat

    @property
    def special_attack(self) -> int:
        """Returns the special attack of the pokemon, taking into account the special attack boosts."""
        special_attack_stat = self.special_attack_stat
        # Object
        if self.item == Item.CHOICE_SPECS:
            special_attack_stat *= 1.5
        # Boosts
        if self.special_attack_boosts > 0:
            return special_attack_stat + (self.special_attack_boosts * self.special_attack_stat // 2)
        elif self.special_attack_boosts < 0:
            return round(special_attack_stat * self.malus_to_percentage(self.special_attack_boosts))
        return special_attack_stat

    @property
    def defense(self) -> int:
        """Returns the defense of the pokemon, taking into account the defense boosts."""
        defense_stat = self.defense_stat
        # Environment
        if self.environment:
            if EnvironmentElements.REFLECT in self.environment.elements or EnvironmentElements.AURORA_VEIL in self.environment.elements:
                defense_stat *= 2
        # Boosts
        if self.defense_boosts > 0:
            return defense_stat + (self.defense_boosts * self.defense_stat // 2)
        elif self.defense_boosts < 0:
            return round(defense_stat * self.malus_to_percentage(self.defense_boosts))
        return defense_stat

    @property
    def special_defense(self) -> int:
        """Returns the special defense of the pokemon, taking into account the special defense boosts."""
        special_defense_stat = self.special_defense_stat
        # Environment
        if self.environment:
            if EnvironmentElements.LIGHT_SCREEN in self.environment.elements or EnvironmentElements.AURORA_VEIL in self.environment.elements:
                special_defense_stat *= 2
            if EnvironmentElements.SAND in self.environment.elements and Type.ROCK in self.types:
                special_defense_stat *= 1.5
        # Boosts
        if self.special_defense_boosts > 0:
            return special_defense_stat + (self.special_defense_boosts * self.special_defense_stat // 2)
        elif self.special_defense_boosts < 0:
            round(special_defense_stat * self.malus_to_percentage(self.special_defense_boosts))
        return special_defense_stat

    @property
    def speed(self) -> int:
        """Returns the speed of the pokemon, taking into account the speed boosts."""
        speed_stat = self.speed_stat
        # Ability
        if SubStatus.UNBURDEN in self.sub_status:
            speed_stat *= 2
        # Environment
        if self.environment:
            if EnvironmentElements.TAILWIND in self.environment.elements:
                speed_stat *= 2
            if EnvironmentElements.SAND in self.environment.elements and self.ability == Ability.SAND_RUSH:
                speed_stat *= 2
            if EnvironmentElements.RAIN in self.environment.elements and self.ability == Ability.SWIFT_SWIM:
                speed_stat *= 2
        # Object
        if self.item == Item.CHOICE_SCARF:
            speed_stat *= 1.5
        # Status
        if self.status == PrimeStatus.PARALYSIS:
            speed_stat //= 2
        # Boosts
        if self.speed_boosts > 0:
            return speed_stat + (self.speed_boosts * self.speed_stat // 2)
        elif self.speed_boosts < 0:
            return round(speed_stat * self.malus_to_percentage(self.speed_boosts))
        return speed_stat

    @staticmethod
    def malus_to_percentage(malus_level: int) -> float:
        """Converts a malus level to a percentage of the stat.

        :param malus_level: The amount of malus to convert
        :return: The percentage of the stat
        """
        level_to_percentage = {
            -1: 0.67,
            -2: 0.50,
            -3: 0.40,
            -4: 0.33,
            -5: 0.29,
            -6: 0.25
        }
        return level_to_percentage[malus_level]

    def get_highest_stat(self) -> str:
        stats = {
            'HP': self.max_hp,
            'Attack': self.attack,
            'Defense': self.defense,
            'Special Attack': self.special_attack,
            'Special Defense': self.special_defense,
            'Speed': self.speed
        }
        highest_stat = max(stats, key=stats.get)
        return highest_stat

    def boost_highest_stat(self):
        highest_stat = self.get_highest_stat()

        if highest_stat == 'Attack':
            self.boost_attack(1)
        elif highest_stat == 'Defense':
            self.boost_defense(1)
        elif highest_stat == 'Special Attack':
            self.boost_special_attack(1)
        elif highest_stat == 'Special Defense':
            self.boost_special_defense(1)
        elif highest_stat == 'Speed':
            self.boost_speed(1)

    def boost_attack(self, boost: int) -> None:
        """Boosts the attack of the pokemon by a certain amount.

        :param boost: The amount of the boost
        """
        if self.attack_boosts < 6:
            if self.ability == Ability.CONTRARY:
                self.attack_boosts -= boost
            else:
                self.attack_boosts += boost
                print(f"{self.name}'s attack rose by {boost} stages !")
        else:
            print(f"{self.name}'s attack can't go any higher!")

    def boost_defense(self, boost: int) -> None:
        """Boosts the defense of the pokemon by a certain amount.

        :param boost: The amount of the boost
        """
        if self.defense_boosts < 6:
            if self.ability == Ability.CONTRARY:
                self.attack_boosts -= boost
            else:
                self.defense_boosts += boost
                print(f"{self.name}'s defense rose by {boost} stages !")
        else:
            print(f"{self.name}'s defense can't go any higher!")

    def boost_special_attack(self, boost: int) -> None:
        """Boosts the special attack of the pokemon by a certain amount.

        :param boost: The amount of the boost
        """
        if self.special_attack_boosts < 6:
            if self.ability == Ability.CONTRARY:
                self.attack_boosts -= boost
                print(f"{self.name}'s special attack fell by {boost} stages !")
            else:
                self.special_attack_boosts += boost
                print(f"{self.name}'s special attack rose by {boost} stages !")
        else:
            print(f"{self.name}'s special attack can't go any higher!")

    def boost_special_defense(self, boost: int) -> None:
        """Boosts the special defense of the pokemon by a certain amount.

        :param boost: The amount of the boost
        """
        if self.special_defense_boosts < 6:
            if self.ability == Ability.CONTRARY:
                self.attack_boosts -= boost
            else:
                self.special_defense_boosts += boost
        else:
            print(f"{self.name}'s special defense can't go any higher!")

    def boost_speed(self, boost: int) -> None:
        """Boosts the speed of the pokemon by a certain amount.

        :param boost: The amount of the boost
        """
        if self.speed_boosts < 6:
            if self.ability == Ability.CONTRARY:
                self.attack_boosts -= boost
            else:
                self.speed_boosts += boost
        else:
            print(f"{self.name}'s speed can't go any higher!")

    def lower_attack(self, malus: int) -> None:
        """Lowers the attack of the pokemon by a certain amount.

        :param malus: The amount of the malus
        """
        if self.ability == Ability.CLEAR_BODY:
            print(f"{self.name}'s Clear Body : stats can't be lowered!")
            return
        if self.attack_boosts > -6:
            if self.ability == Ability.CONTRARY:
                self.attack_boosts += malus
                print(f"{self.name}'s attack rose by {malus} stages !")
            else:
                self.attack_boosts -= malus
                print(f"{self.name}'s attack fell by {malus} stages !")
        else:
            print(f"{self.name}'s attack can't go any lower!")

    def lower_defense(self, malus: int) -> None:
        """Lowers the defense of the pokemon by a certain amount.

        :param malus: The amount of the malus
        """
        if self.ability == Ability.CLEAR_BODY:
            print(f"{self.name}'s Clear Body : stats can't be lowered!")
            return
        elif self.ability == Ability.BIG_PECKS:
            print(f"{self.name}'s Big Pecks : stats can't be lowered!")
            return
        if self.defense_boosts > -6:
            if self.ability == Ability.CONTRARY:
                self.attack_boosts += malus
                print(f"{self.name}'s defense rose by {malus} stages !")
            else:
                self.defense_boosts -= malus
                print(f"{self.name}'s defense fell by {malus} stages !")
        else:
            print(f"{self.name}'s defense can't go any lower!")

    def lower_special_attack(self, malus: int) -> None:
        """Lowers the special attack of the pokemon by a certain amount.

        :param malus: The amount of the malus
        """
        if self.ability == Ability.CLEAR_BODY:
            print(f"{self.name}'s Clear Body : stats can't be lowered!")
            return
        if self.special_attack_boosts > -6:
            if self.ability == Ability.CONTRARY:
                self.attack_boosts += malus
                print(f"{self.name}'s special attack rose by {malus} stages !")
            else:
                self.special_attack_boosts -= malus
                print(f"{self.name}'s special attack fell by {malus} stages !")
        else:
            print(f"{self.name}'s special attack can't go any lower!")

    def lower_special_defense(self, malus: int) -> None:
        """Lowers the special defense of the pokemon by a certain amount.

        :param malus: The amount of the malus
        """
        if self.ability == Ability.CLEAR_BODY:
            print(f"{self.name}'s Clear Body : stats can't be lowered!")
            return
        if self.special_defense_boosts > -6:
            if self.ability == Ability.CONTRARY:
                self.attack_boosts += malus
                print(f"{self.name}'s special defense rose by {malus} stages !")
            else:
                self.special_defense_boosts -= malus
                print(f"{self.name}'s special defense fell by {malus} stages !")
        else:
            print(f"{self.name}'s special defense can't go any lower!")

    def lower_speed(self, malus: int) -> None:
        """Lowers the speed of the pokemon by a certain amount.

        :param malus: The amount of the malus
        """
        if self.ability == Ability.CLEAR_BODY:
            print(f"{self.name}'s Clear Body : stats can't be lowered!")
            return
        if self.speed_boosts > -6:
            if self.ability == Ability.CONTRARY:
                self.attack_boosts += malus
                print(f"{self.name}'s speed rose by {malus} stages !")
            else:
                self.speed_boosts -= malus
                print(f"{self.name}'s speed fell by {malus} stages !")
        else:
            print(f"{self.name}'s speed can't go any lower!")

    def convert_hp_to_percentage(self, hp: int) -> float:
        """Converts the HP to a percentage of the max HP.

        :param hp: The amount of HP to convert
        :return: The percentage of the max HP
        """
        computed_hp = max(self.current_hp, hp)
        return round((computed_hp / self.max_hp) * 100, 1)

    def get_current_hp_percentage(self) -> float:
        """Returns the current HP as a percentage of the max HP.

        :return: The percentage of the max HP
        """
        percentage = (self.current_hp / self.max_hp) * 100
        return round(percentage * 2) / 2
    
    def calculate_weaknesses(self) -> 'list[Type]':
        """Calculates the weaknesses of the pokemon.

        :return: The weaknesses of the pokemon
        """
        weaknesses = self.get_types_weaknesses()
        resistances = self.get_types_resistances()
        for pokemon_type in resistances:
            if pokemon_type in weaknesses:
                weaknesses.remove(pokemon_type)
        if len(self.immunities) > 0:
            for pokemon_type in self.immunities:
                if pokemon_type in weaknesses:
                    weaknesses.remove(pokemon_type)
        return weaknesses

    def calculate_resistances(self) -> 'list[Type]':
        """Calculates the resistances of the pokemon.

        :return: The resistances of the pokemon
        """
        weaknesses: list[Type] = self.get_types_weaknesses()
        resistances: list[Type] = self.get_types_resistances()
        for pokemon_type in weaknesses:
            if pokemon_type in resistances:
                resistances.remove(pokemon_type)
        if len(self.immunities) > 0:
            for pokemon_type in self.immunities:
                if pokemon_type in resistances:
                    resistances.remove(pokemon_type)
        return resistances
    
    def get_types_weaknesses(self) -> 'list[Type]':
        """Returns the weaknesses of the pokemon.

        :return: The weaknesses of the pokemon
        """
        weaknesses = []
        for pokemon_type in self.types:
            weaknesses.extend(pokemon_type.value.weaknesses)
        return weaknesses
    
    def get_types_resistances(self) -> 'list[Type]':
        """Returns the resistances of the pokemon.

        :return: The resistances of the pokemon
        """
        resistances: list[Type] = []
        for pokemon_type in self.types:
            resistances.extend(pokemon_type.value.resistances)
        if self.ability == Ability.THICK_FAT:
            resistances.append(Type.FIRE)
            resistances.append(Type.ICE)
        return resistances
    
    def get_types_immunities(self) -> 'list[Type]':
        """Returns the immunities of the pokemon.

        :return: The immunities of the pokemon
        """
        immunities = []
        for pokemon_type in self.types:
            immunities.extend(pokemon_type.value.immunities)
        return immunities
    
    def print_attacks(self) -> None:
        """Prints the attacks of the pokemon with their indices."""
        for i, attack in enumerate(self.moves):
            print(f"{i + 1}. {attack}")
            
    def print_attacks_without_indices(self) -> None:
        """Prints the attacks of the pokemon without their indices."""
        for attack in self.moves:
            print(f"    {attack}")

    def can_z_move(self):
        if self.item in (Item.NORMALIUM_Z,
                         Item.FIGHTINIUM_Z,
                         Item.FLYINIUM_Z,
                         Item.POISONIUM_Z,
                         Item.GROUNDIUM_Z,
                         Item.ROCKIUM_Z,
                         Item.BUGINIUM_Z,
                         Item.GHOSTIUM_Z,
                         Item.STEELIUM_Z,
                         Item.FAIRIUM_Z,
                         Item.WATERIUM_Z,
                         Item.FIRIUM_Z,
                         Item.GRASSIUM_Z,
                         Item.ELECTRIUM_Z,
                         Item.PSYCHIUM_Z,
                         Item.ICINIUM_Z,
                         Item.DRAGONIUM_Z,
                         Item.DARKINIUM_Z):
            return True
        return False

    def get_z_moves(self) -> 'list[ZMove]':
        if self.item == Item.NORMALIUM_Z:
            z_type = Type.NORMAL
        elif self.item == Item.FIGHTINIUM_Z:
            z_type = Type.FIGHT
        elif self.item == Item.FLYINIUM_Z:
            z_type = Type.FLYING
        elif self.item == Item.POISONIUM_Z:
            z_type = Type.POISON
        elif self.item == Item.GROUNDIUM_Z:
            z_type = Type.GROUND
        elif self.item == Item.ROCKIUM_Z:
            z_type = Type.ROCK
        elif self.item == Item.BUGINIUM_Z:
            z_type = Type.BUG
        elif self.item == Item.GHOSTIUM_Z:
            z_type = Type.GHOST
        elif self.item == Item.STEELIUM_Z:
            z_type = Type.STEEL
        elif self.item == Item.FAIRIUM_Z:
            z_type = Type.FAIRY
        elif self.item == Item.WATERIUM_Z:
            z_type = Type.WATER
        elif self.item == Item.FIRIUM_Z:
            z_type = Type.FIRE
        elif self.item == Item.GRASSIUM_Z:
            z_type = Type.GRASS
        elif self.item == Item.ELECTRIUM_Z:
            z_type = Type.ELECTRIC
        elif self.item == Item.PSYCHIUM_Z:
            z_type = Type.PSYCHIC
        elif self.item == Item.ICINIUM_Z:
            z_type = Type.ICE
        elif self.item == Item.DRAGONIUM_Z:
            z_type = Type.DRAGON
        else:
            z_type = Type.DARK
        z_moves = []
        for attack in self.moves:
            if attack.type == z_type:
                z_moves.append(ZMove(attack))
            else:
                z_moves.append(colored("- - - - - - -", 'dark_grey'))
        return z_moves

    def print_z_moves(self) -> None:
        """Prints the Z-Moves of the pokemon with their indices."""
        z_moves = self.get_z_moves()
        for i, z_move in enumerate(z_moves):
            print(f"{i + 1}. {z_move}")

    def print_z_moves_without_indices(self) -> None:
        """Prints the Z-Moves of the pokemon without their indices."""
        z_moves = self.get_z_moves()
        for z_move in z_moves:
            print(f"    {z_move}")

    def heal(self, amount: int) -> None:
        """Heals the pokemon by a certain amount."""
        self.current_hp += max(amount, 0)
        print(f"{self.name} was healed by {self.convert_hp_to_percentage(amount)} HP!")
            
    def attack_target(self, move_index: int, is_secondary_effect_applied: bool, target: 'Pokemon | Player', damage, nbr_hit: int) -> bool:
        """The pokemon attacks the target with a move.

        :param move_index: The index of the move to use
        :param is_secondary_effect_applied: Whether the secondary effect is applied
        :param target: The target of the attack
        :param damage: The damage to apply to the target
        :param nbr_hit: The number of hits of the move
        """
        move = self.moves[move_index]
        self.last_used_move = move
        base_types = self.types

        if move.current_pp > 0:
            if isinstance(target, Pokemon) and target != self:
                if target.ability == Ability.PRESSURE:
                    move.current_pp -= 2
                else:
                    move.current_pp -= 1
            else:
                if target.current_pokemon.ability == Ability.PRESSURE and target.current_pokemon != self:
                    move.current_pp -= 2
                else:
                    move.current_pp -= 1

            if self.ability == Ability.PROTEAN:
                if move.type not in self.types:
                    self.types = [move.type]
                    print(f"Protean from {self.name} : He changed its type to {move.type.name}!")

            if move.category != MoveCategory.STATUS:
                attack_successful = target.receive_damage(damage, nbr_hit)

                # If the attack was successful, apply the secondary effect of abilities
                if attack_successful:
                    if move.attributes['contact'] is True:
                        if target.ability == Ability.IRON_BARBS or target.ability == Ability.ROUGH_SKIN:
                            print(f"{target.ability.name} from {target.name}")
                            self.receive_damage(self.max_hp // 8)
                        elif target.ability == Ability.STATIC:
                            if self.status == PrimeStatus.NORMAL:
                                if randint(1, 100) <= 30:
                                    print(f"{target.ability.name} from {target.name}")
                                    print(f"{self.name} is paralyzed!")
                                    self.status = PrimeStatus.PARALYSIS
                        elif target.ability == Ability.FLAME_BODY:
                            if self.status == PrimeStatus.NORMAL:
                                if randint(1, 100) <= 30:
                                    print(f"{target.ability.name} from {target.name}")
                                    print(f"{self.name} is burned!")
                                    self.status = PrimeStatus.BURN
            else:
                attack_successful = True

            if attack_successful:
                # If the target is a Pokemon, apply the secondary effect of the move
                if isinstance(target, Pokemon):
                    if not target.is_dead():
                        if is_secondary_effect_applied:
                            move.apply_secondary_effect(target, self)
                else:
                    # If the target is a player, apply the secondary effect of the move
                    if is_secondary_effect_applied:
                        move.apply_secondary_effect(target, self)
                return True
            self.types = base_types
        else:
            print(f"{self.name} has no PP left!")
            return False

    def receive_damage(self, damage: int, nbr_hit: int = 1) -> bool:
        """The pokemon receives damage.

        :param damage: The amount of damage to receive
        :param nbr_hit: The number of hits of the move
        :return: Whether the pokemon was hit or not
        """
        # If the Pokemon is immune thanks to its type
        if damage == 0:
            return False
        # If the Pokemon is immune thanks to its ability (volt absorb, water absorb, etc...)
        elif damage < 0:
            self.heal(-damage)
            return False

        if self.ability == Ability.STURDY and self.current_hp == self.max_hp:
            damage = min(damage, self.current_hp - 1)
        elif self.item == Item.FOCUS_SASH and self.current_hp == self.max_hp:
            damage = min(damage, self.current_hp - 1)
            self.drop_object()

        for _ in range(nbr_hit):
            self.current_hp -= damage
            self.current_hp = max(self.current_hp, 0)

            self.is_dead(True)

        if nbr_hit > 1:
            print(f"Hit {nbr_hit} times!")
        print(f"{self.name} lost {min(self.convert_hp_to_percentage(damage * nbr_hit), 100)}% HP!")

        return True

    @staticmethod
    def get_stab_multiplier(attacker: 'Pokemon', attack_type: Type) -> bool:
        """Returns whether the move has STAB or not.

        :param attacker: The pokemon that uses the move
        :param attack_type: The type of the move
        :return: Whether the move has STAB or not
        """
        if attack_type in attacker.types:
            return True
        return False

    @staticmethod
    def get_critical_multiplier() -> bool:
        """Returns whether the move has a critical hit or not.

        :return: Whether the move has a critical hit or not
        """
        critical_hit_chance = 4.17
        if randint(1, 100) <= critical_hit_chance:
            print("Critical hit!")
            return True
        return False

    def get_types_multiplier(self, attack_type: Type, attacker: 'Pokemon') -> float:
        """Returns the type effectiveness multiplier of the move.

        :param attack_type: The type of the move
        :param attacker: The pokemon that uses the move
        :return: The type effectiveness multiplier of the move
        """
        temp_immunities = deepcopy(self.immunities)
        if self.ability == Ability.LEVITATE:
            temp_immunities.append(Type.GROUND)
        if attacker.ability == Ability.SCRAPPY:
            if Type.GHOST in self.types:
                temp_immunities.remove(Type.FIGHT)
                temp_immunities.remove(Type.NORMAL)

        multiplier = 1
        if attack_type in temp_immunities:
            print("This has no effect...")
            return 0.0
        if attack_type in self.weaknesses:
            print("This is very effective!")
            count = self.weaknesses.count(attack_type)
            for _ in range(count):
                multiplier *= 2
        if attack_type in self.resistances:
            print("This is not very effective...")
            count = self.resistances.count(attack_type)
            for _ in range(count):
                multiplier *= 0.5
        return multiplier

    def get_multipliers(self, move: Move, attacker: 'Pokemon') -> tuple[bool, bool, float]:
        """Returns the multipliers of the move.

        :param move: The move used
        :param attacker: The pokemon that uses the move
        :return: The multipliers of the move
        """
        move_type = move.type
        # STAB
        stab_multiplier: bool = self.get_stab_multiplier(attacker, move_type)
        # Critical hit
        crit_multiplier: bool = self.get_critical_multiplier()
        # Type effectiveness
        type_multiplier: float = self.get_types_multiplier(move.type, attacker)

        return stab_multiplier, crit_multiplier, type_multiplier

    def compute_multipliers(self, multipliers: tuple[bool, bool, int]) -> float:
        """Computes the multiplier of the move.

        :param multipliers: The multipliers of the move
        :return: The total multiplier of the move
        """
        multiplier = 1
        # STAB
        if multipliers[0]:
            if self.ability == Ability.ADAPTABILITY:
                multiplier *= 2
            else:
                multiplier *= 1.5
        # Critical hit
        if multipliers[1]:
            multiplier *= 1.5
        # Type effectiveness
        multiplier *= multipliers[2]
        return multiplier

    def calculate_damage(self, move: Move, attacker: 'Pokemon', multipliers) -> int:
        """Calculates the damage value of the move.

        :param move: A Move or ZMove object, the move used
        :param attacker: The pokemon that uses the move
        :param multipliers: The multipliers of the move
        :return: The damage value of the move
        """
        # Protect
        if SubStatus.PROTECT in self.sub_status:
            print(f"{self.name} protected itself!")
            return 0

        # If the pokemon is immune to the move thanks to its ability
        if self.ability == Ability.FLASH_FIRE and move.type == Type.FIRE:
            return 0
        elif self.ability == Ability.JUSTIFIED and move.type == Type.DARK:
            self.boost_attack(1)
        elif self.ability == Ability.WATER_ABSORB and move.type == Type.WATER:
            return -(self.max_hp // 4)
        elif self.ability == Ability.VOLT_ABSORB and move.type == Type.ELECTRIC:
            return -(self.max_hp // 4)
        elif self.ability == Ability.SAP_SIPPER:
            self.boost_attack(1)
            return 0
        elif self.ability == Ability.STORM_DRAIN and move.type == Type.WATER:
            print(f"Storm Drain from {self.name} !")
            self.boost_special_attack(1)
            return 0
        elif self.ability == Ability.FLASH_FIRE and move.type == Type.FIRE:
            print(f"Flash Fire from {self.name} !")
            print("The power of {self.name}'s fire move were increased!")
            self.sub_status.append(SubStatus.FLASH_FIRE)
            return 0
        elif self.ability == Ability.LEVITATE and attacker.ability != Ability.MOLD_BREAKER and attacker.ability != Ability.TERA_VOLTAGE and move.type == Type.GROUND:
            return 0
        elif self.ability == Ability.BULLET_PROOF and move.attributes['bullet'] is True:
            return 0
        elif self.ability == Ability.SOUNDPROOF and move.attributes['sound'] is True:
            return 0
        elif self.ability == Ability.LIGHTNING_ROD and move.type == Type.ELECTRIC:
            print(f"Lightning Rod from {self.name} !")
            self.boost_special_attack(1)
            return 0

        # If the pokemon is immune to the move thanks to its type
        if multipliers[2] == 0.0:
            return 0

        # Physical or Special

        if move.category == MoveCategory.PHYSICAL:
            if self.ability == Ability.UNAWARE:
                attack_stat: int = attacker.attack_stat
            else:
                attack_stat: int = attacker.attack
            if attacker.ability == Ability.UNAWARE or move.name == "Sacred Sword":
                defense_stat: int = self.defense_stat
            else:
                defense_stat: int = self.defense
        else:
            if self.ability == Ability.UNAWARE:
                attack_stat: int = attacker.special_attack_stat
            else:
                attack_stat: int = attacker.special_attack
            if attacker.ability == Ability.UNAWARE:
                if move.name == "Psyshok":
                    defense_stat: int = self.defense_stat
                else:
                    defense_stat: int = self.special_defense_stat
            else:
                if move.name == "Psyshok":
                    defense_stat: int = self.defense
                else:
                    defense_stat: int = self.special_defense

        # Acrobatics
        move_power = move.power
        if move.name == "Acrobatics" and attacker.item == Item.NONE:
            move_power = 110

        # Abilities that modify the power of the move
        if attacker.ability == Ability.TECHNICIAN and move_power <= 60:
            move_power *= 1.5
        elif attacker.ability == Ability.SAND_FORCE and EnvironmentElements.SAND in self.environment.elements and move.type in [Type.ROCK, Type.STEEL, Type.GROUND]:
            move_power *= 1.3
        elif attacker.ability == Ability.TOUGH_CLAWS and move.attributes['contact'] is True:
            move_power *= 1.3
        elif SubStatus.FLASH_FIRE in attacker.sub_status and move.type == Type.FIRE:
            move_power *= 1.5
        elif attacker.ability == Ability.TORRENT and move.type == Type.WATER and attacker.current_hp <= attacker.max_hp / 3:
            move_power *= 1.5
        elif attacker.ability == Ability.SWARM and move.type == Type.BUG and attacker.current_hp <= attacker.max_hp / 3:
            move_power *= 1.5
        elif attacker.ability == Ability.BLAZE and move.type == Type.FIRE and attacker.current_hp <= attacker.max_hp / 3:
            move_power *= 1.5
        elif attacker.ability == Ability.OVERGROW and move.type == Type.GRASS and attacker.current_hp <= attacker.max_hp / 3:
            move_power *= 1.5

        # Prime status
        if attacker.status == PrimeStatus.BURN and move.category == MoveCategory.PHYSICAL and attacker.ability != Ability.GUTS:
            move_power //= 2

        # Multipliers
        multiplier = self.compute_multipliers(multipliers)
        damage = (floor(floor(attacker.lvl * 2 / 5 + 2) * move_power * attack_stat / defense_stat) / 50) + 2  # Calculate the raw damage
        damage *= multiplier  # Apply the modifiers
        damage = floor(damage * randint(85, 100) / 100)  # Apply the random factor

        # Weather multipliers
        if EnvironmentElements.SUN in self.environment.elements and move.type == Type.FIRE:
            damage *= 1.5
        elif EnvironmentElements.SUN in self.environment.elements and move.type == Type.WATER:
            damage *= 0.5
        elif EnvironmentElements.RAIN in self.environment.elements and move.type == Type.WATER:
            damage *= 1.5
        elif EnvironmentElements.RAIN in self.environment.elements and move.type == Type.FIRE:
            damage *= 0.5

        # Abilities that modify the damage directly
        if self.ability == Ability.MULTISCALE and self.current_hp == self.max_hp:
            damage *= 0.5

        return max(int(damage), 1)
    
    def is_dead(self, print_message: bool = False) -> bool:
        """Returns whether the pokemon is dead or not.

        :param print_message: Whether to print a message or not
        :return: Whether the pokemon is dead or not
        """
        if self.current_hp <= 0:
            if print_message:
                print(f"{self.name} fainted !")
            return True
        
    def print_moves(self) -> str:
        """Prints the moves of the pokemon with their indices, greyed out if the pokemon is fainted.

        :return: The moves of the pokemon with their indices
        """
        if self.current_hp <= 0:
            attacks_str = colored("| Moves : ", 'dark_grey') + colored(" - ", 'dark_grey').join([colored(f"{attack.name} ({attack.print_greyed_out_pp()})", 'dark_grey') for attack in self.moves])
        else:
            attacks_str = f"| Moves : " + " - ".join([f"{attack.name} ({attack.print_colored_pp()})" for attack in self.moves])
        return attacks_str
    
    # Status
    def apply_end_turn_primary_status(self) -> None:
        """Applies the end of turn effects of the primary status of the pokemon."""
        if self.ability == Ability.MAGIC_GUARD:
            return
        if self.status == PrimeStatus.BURN:
            self.current_hp = max(self.current_hp - floor(self.max_hp / 16), 0)
            print(f"{self.name} is hurt by its burn!")
        elif self.status == PrimeStatus.POISON:
            if self.ability == Ability.POISON_HEAL:
                self.heal(floor(self.max_hp / 8))
            else:
                self.current_hp = max(self.current_hp - floor(self.max_hp / 8), 0)
                print(f"{self.name} is hurt by poison!")
        elif self.status == PrimeStatus.SEVERE_POISON:
            if self.ability == Ability.POISON_HEAL:
                self.heal(floor(self.max_hp / 8))
            else:
                poison_damage = floor(self.max_hp / 16) * self.nbr_turn_severe_poison
                self.current_hp = max(self.current_hp - poison_damage, 0)
                print(f"{self.name} is hurt by poison!")
                self.nbr_turn_severe_poison += 1

    def apply_end_turn_secondary_status(self):
        """Applies the end of turn effects of the secondary status of the pokemon."""


    def apply_leech_seed(self, target: 'Pokemon') -> int:
        """Applies the leech seed effect on the target.

        :param target: The target of the leech seed
        :return: The amount of HP drained
        """
        if SubStatus.LEECH_SEED in self.sub_status:
            if self.ability == Ability.MAGIC_GUARD:
                hp_drained = 0
            else:
                hp_drained = floor(self.max_hp / 8)
            self.receive_damage(hp_drained)
            print(f"{target.name} is draining the energy of {self.name}!")
            return hp_drained

    def opponent_died(self) -> None:
        if self.ability == Ability.BEAST_BOOST:
            self.boost_highest_stat()
        elif self.ability == Ability.BATTLE_BOND and self.name == "Greninja":
            self.attack_stat += 50
            self.special_attack_stat += 50
            self.speed_stat += 10
            print("Greninja's Battle Bond : Greninja became Ash-Greninja!")
        elif self.ability == Ability.SOUL_HEART:
            self.boost_special_attack(1)
        elif self.ability == Ability.MOXIE:
            self.boost_attack(1)

    def drop_object(self) -> Item:
        item = self.item
        self.item = Item.NONE
        if self.ability == Ability.UNBURDEN:
            self.sub_status.append(SubStatus.UNBURDEN)
        return item

    def switch_out(self):
        """Resets the status of the pokemon when it switches out."""
        self.nbr_turn_severe_poison = 0
        self.sub_status = []
        self.attack_boosts = 0
        self.defense_boosts = 0
        self.special_attack_boosts = 0
        self.special_defense_boosts = 0
        self.speed_boosts = 0

        if self.ability == Ability.NATURAL_CURE:
            self.status = PrimeStatus.NORMAL
            print(f"{self.name} healed its status!")
        elif self.ability == Ability.REGENERATOR:
            self.heal(floor(self.max_hp / 3))
        
    def switch_in(self, enemy_player: 'Player') -> bool:
        """Applies the effects of the environment when the pokemon switches in."""
        # Entry hazards
        self.switch_in_stealth_rock()
        if self.is_dead(True):
            return True
        self.switch_in_spikes()
        if self.is_dead(True):
            return True
        self.switch_in_toxic_spikes()

        enemy_pokemon = enemy_player.current_pokemon
        if self.ability == Ability.TRACE:
            self.ability = enemy_pokemon.ability

        enemy_environment = enemy_player.environment
        # Weather
        weather_turns = 5
        if self.item == Item.HOT_ROCK:
            weather_turns = 8
        elif self.item == Item.DAMP_ROCK:
            weather_turns = 8
        elif self.item == Item.SMOOTH_ROCK:
            weather_turns = 8
        elif self.item == Item.ICY_ROCK:
            weather_turns = 8

        if self.ability == Ability.DROUGHT:
            self.environment.add_element(EnvironmentElements.SUN, weather_turns)
            enemy_environment.add_element(EnvironmentElements.SUN, weather_turns)
        elif self.ability == Ability.DRIZZLE:
            self.environment.add_element(EnvironmentElements.RAIN, weather_turns)
            enemy_environment.add_element(EnvironmentElements.RAIN, weather_turns)
        elif self.ability == Ability.SAND_STREAM:
            self.environment.add_element(EnvironmentElements.SAND, weather_turns)
            enemy_environment.add_element(EnvironmentElements.SAND, weather_turns)
        elif self.ability == Ability.SNOW_WARNING:
            self.environment.add_element(EnvironmentElements.SNOW, weather_turns)
            enemy_environment.add_element(EnvironmentElements.SNOW, weather_turns)

        # Terrains
        terrain_turns = 5
        if self.item == Item.TERRAIN_EXTENDER:
            terrain_turns = 8
        elif self.ability == Ability.GRASSY_SURGE:
            self.environment.add_element(EnvironmentElements.GRASSY_TERRAIN, terrain_turns)
            enemy_environment.add_element(EnvironmentElements.GRASSY_TERRAIN, terrain_turns)
        elif self.ability == Ability.MISTY_SURGE:
            self.environment.add_element(EnvironmentElements.MISTY_TERRAIN, terrain_turns)
            enemy_environment.add_element(EnvironmentElements.MISTY_TERRAIN, terrain_turns)
        elif self.ability == Ability.ELECTRIC_SURGE:
            self.environment.add_element(EnvironmentElements.ELECTRIC_TERRAIN, terrain_turns)
            enemy_environment.add_element(EnvironmentElements.ELECTRIC_TERRAIN, terrain_turns)
        elif self.ability == Ability.PSYCHIC_SURGE:
            self.environment.add_element(EnvironmentElements.PSYCHIC_TERRAIN, terrain_turns)
            enemy_environment.add_element(EnvironmentElements.PSYCHIC_TERRAIN, terrain_turns)

        # Objects
        if self.item == Item.GRASSY_SEED and EnvironmentElements.GRASSY_TERRAIN in self.environment.elements:
            self.boost_defense(1)
            self.drop_object()
        elif self.item == Item.MISTY_SEED and EnvironmentElements.MISTY_TERRAIN in self.environment.elements:
            self.boost_special_defense(1)
            self.drop_object()
        elif self.item == Item.ELECTRIC_SEED and EnvironmentElements.ELECTRIC_TERRAIN in self.environment.elements:
            self.boost_defense(1)
            self.drop_object()
        elif self.item == Item.PSYCHIC_SEED and EnvironmentElements.PSYCHIC_TERRAIN in self.environment.elements:
            self.boost_special_defense(1)
            self.drop_object()

    def switch_in_stealth_rock(self):
        """Applies the effects of stealth rock when the pokemon switches in."""
        if self.ability == Ability.MAGIC_GUARD:
            return
        if EnvironmentElements.STEALTH_ROCK in self.environment.elements:
            stealth_rock_damage = 12.5  # Percentage of max HP
            for pokemon_type in self.types:
                if Type.ROCK in pokemon_type.value.weaknesses:
                    stealth_rock_damage *= 2
                elif Type.ROCK in pokemon_type.value.resistances:
                    stealth_rock_damage /= 2
            stealth_rock_damage = floor(self.max_hp * (stealth_rock_damage / 100))
            self.current_hp = max(self.current_hp - stealth_rock_damage, 0)
            print(f"{self.name} is hurt by stealth rock!")

    def switch_in_spikes(self):
        """Applies the effects of spikes when the pokemon switches in."""
        if Type.FLYING in self.types or self.ability == Ability.LEVITATE or self.ability == Ability.MAGIC_GUARD:
            return
        elif EnvironmentElements.SPIKES in self.environment.elements:
            spikes_count = self.environment.elements.count(EnvironmentElements.SPIKES)
            spikes_damage = 0
            if spikes_count == 1:
                spikes_damage = floor(self.max_hp / 8)
            elif spikes_count == 2:
                spikes_damage = floor(self.max_hp / 6)
            elif spikes_count >= 3:
                spikes_damage = floor(self.max_hp / 4)
            self.current_hp = max(self.current_hp - spikes_damage, 0)
            print(f"{self.name} is hurt by spikes!")
            
    def switch_in_toxic_spikes(self) -> None:
        """Applies the effects of toxic spikes when the pokemon switches in."""
        if Type.FLYING in self.types or self.ability == Ability.LEVITATE:
            return
        elif EnvironmentElements.TOXIC_SPIKES in self.environment.elements:
            toxic_spikes_count = self.environment.elements.count(EnvironmentElements.TOXIC_SPIKES)
            if Type.POISON in self.types:
                self.environment.remove_toxic_spikes()
                print(f"{self.name} absorbed the toxic spikes!")
            elif toxic_spikes_count == 1:
                if PrimeStatus == PrimeStatus.NORMAL:
                    self.status = PrimeStatus.POISON
                    print(f"{self.name} is poisoned by toxic spikes!")
            elif toxic_spikes_count == 2:
                if PrimeStatus == PrimeStatus.NORMAL:
                    self.status = PrimeStatus.SEVERE_POISON
                    print(f"{self.name} is badly poisoned by toxic spikes!")

    def apply_end_turn_ability(self) -> None:
        if self.ability == Ability.ICE_BODY and EnvironmentElements.SNOW in self.environment.elements:
            self.heal(floor(self.max_hp / 16))
            print(f"{self.name} is healed by Ice Body!")
        elif self.ability == Ability.RAIN_DISH and EnvironmentElements.RAIN in self.environment.elements:
            self.heal(floor(self.max_hp / 16))
            print(f"{self.name} is healed by Rain Dish!")
        elif self.ability == Ability.HYDRATION and EnvironmentElements.RAIN in self.environment.elements:
            self.status = PrimeStatus.NORMAL
            print(f"{self.name} healed its status!")
        elif self.ability == Ability.SPEED_BOOST:
            self.boost_speed(1)

    def apply_end_turn_object(self):
        if self.item == Item.LEFTOVERS:
            print(f"{self.name} recovered a bit of hp thanks to its leftovers!")
            self.heal(self.max_hp//16)
        elif self.item == Item.BLACK_SLUDGE:
            if Type.POISON in self.types:
                print(f"{self.name} recovered a bit of hp thanks to its black sludge!")
                self.heal(self.max_hp // 16)
            else:
                print(f"{self.name} was hurt by its black sludge!")
                self.receive_damage(self.max_hp // 8)
        elif self.item == Item.TOXIC_ORB:
            if self.status == PrimeStatus.NORMAL:
                print(f"{self.name} was badly poisoned")
                self.status = PrimeStatus.SEVERE_POISON
        elif self.item == Item.FLAME_ORB:
            if self.status == PrimeStatus.NORMAL:
                print(f"{self.name} was burned")
                self.status = PrimeStatus.BURN

    def apply_end_turn_weather(self) -> None:
        """Applies the end of turn effects of the weather."""
        if self.environment:
            if self.ability == Ability.OVERCOAT:
                return
            if EnvironmentElements.SAND in self.environment.elements and Type.ROCK not in self.types and Type.STEEL not in self.types and Type.GROUND not in self.types and self.ability != Ability.SAND_FORCE:
                self.current_hp = max(self.current_hp - floor(self.max_hp / 16), 0)
                print(f"{self.name} is hurt by the sandstorm!")
            elif EnvironmentElements.SNOW in self.environment.elements and self.ability != Ability.ICE_BODY:
                self.current_hp = max(self.current_hp - floor(self.max_hp / 16), 0)
                print(f"{self.name} is hurt by the hail!")

    def end_turn(self) -> None:
        """Applies the end of turn effects of the pokemon."""
        self.apply_end_turn_primary_status()
        self.apply_end_turn_secondary_status()
        self.apply_end_turn_ability()
        self.apply_end_turn_weather()
        self.environment.pass_turn()

    def can_mega_evolve(self) -> bool:
        if not self.mega_evolution_stats:
            return False
        if self.item == Item.ALAKAZAMITE and self.name == "Alakazam":
            return True
        elif self.item == Item.BLAZIKENITE and self.name == "Blaziken":
            return True
        elif self.item == Item.GARCHOMPITE and self.name == "Garchomp":
            return True
        elif self.item == Item.CHARMINITE and self.name == "Charmina":
            return True
        elif self.item == Item.SCIZORITE and self.name == "Scizor":
            return True
        elif self.item == Item.BEEDRILLITE and self.name == "Beedrill":
            return True
        elif self.item == Item.DIANCITE and self.name == "Diancie":
            return True
        elif self.item == Item.CHARIZARDITE_X and self.name == "Charizard":
            return True
        elif self.item == Item.CHARIZARDITE_Y and self.name == "Charizard":
            return True
        elif self.item == Item.SALAMENCITE and self.name == "Salamence":
            return True
        elif self.item == Item.MANECTITE and self.name == "Manectric":
            return True
        elif self.item == Item.SWAMPERTITE and self.name == "Swampert":
            return True
        elif self.item == Item.LOPUNNITE and self.name == "Lopunny":
            return True
        elif self.item == Item.METAGROSSITE and self.name == "Metagross":
            return True
        elif self.item == Item.MAWILITE and self.name == "Mawile":
            return True
        elif self.item == Item.PIDGEOTITE and self.name == "Pidgeot":
            return True
        elif self.item == Item.PINSIRITE and self.name == "Pinsir":
            return True
        elif self.item == Item.TYRANITARITE and self.name == "Tyraniytar":
            return True
        elif self.item == Item.VENUSAURITE and self.name == "Venusaur":
            return True
        return False

    def mega_evolve(self) -> None:
        if self.name == "Charizard":
            if self.item == Item.CHARIZARDITE_X:
                self.attack_stat, self.defense_stat, self.special_attack_stat, self.special_defense_stat, self.speed_stat, self.ability, self.types = self.mega_evolution_stats[0]
                self.name = "Mega " + self.name + " X"
            elif self.item == Item.CHARIZARDITE_Y:
                self.attack_stat, self.defense_stat, self.special_attack_stat, self.special_defense_stat, self.speed_stat, self.ability, self.types = self.mega_evolution_stats[1]
                self.name = "Mega " + self.name + " Y"
        else:
            self.attack_stat, self.defense_stat, self.special_attack_stat, self.special_defense_stat, self.speed_stat, self.ability, self.types = self.mega_evolution_stats[0]
            self.name = "Mega " + self.name
