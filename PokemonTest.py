from Types import Type, TypeClass
from OffensiveCapacityCopy import *
from StatusCapacityCopy import *
from Status import PrimeStatus, SubStatus
from Environment import EnvironmentElements
from termcolor import colored
from os import system
from random import randint
from math import floor


class Pokemon:
    def __init__(self, name: str, 
                 lvl: int,
                 hp: int,
                 attack: int,
                 special_attack: int,
                 defense: int,
                 special_defense: int,
                 speed: int,
                 types: 'list[Type]', 
                 moves: 'list') -> None:
        self.name = name
        self.lvl = lvl
        # Stats
        self.current_hp: int = hp
        self.max_hp: int = hp
        self.attack: int = attack
        self.special_attack: int = special_attack
        self.defense: int = defense
        self.special_defense: int = special_defense
        self.speed: int = speed
        # Types
        self.types: list[Type] = types
        self.immunities: list[TypeClass] = self.get_types_immunities()
        self.weaknesses: list[TypeClass] = self.calculate_weaknesses()
        self.resistances: list[TypeClass] = self.calculate_resistances()
        # Status
        self.status: PrimeStatus = PrimeStatus.NORMAL
        self.sub_status: SubStatus = []
        
        self.moves: list = moves
    
    def __getstate__(self):
        return {
            'name': self.name,
            'lvl': self.lvl,
            'current_hp': self.current_hp,
            'max_hp': self.max_hp,
            'attack': self.attack,
            'special_attack': self.special_attack,
            'defense': self.defense,
            'special_defense': self.special_defense,
            'speed': self.speed,
            'types': [type.name for type in self.types],
            'immunities': [type.name for type in self.immunities],
            'weaknesses': [type.name for type in self.weaknesses],
            'resistances': [type.name for type in self.resistances],
            'status': self.status,
            'sub_status': [status.name for status in self.sub_status],
            'moves': [attack.__getstate__() for attack in self.moves]
        }
        
    def __setstate__(self, state):
        self.name = state['name']
        self.lvl = state['lvl']
        self.current_hp = state['current_hp']
        self.max_hp = state['max_hp']
        self.attack = state['attack']
        self.special_attack = state['special_attack']
        self.defense = state['defense']
        self.special_defense = state['special_defense']
        self.speed = state['speed']
        self.types = [Type[type_name.upper()] for type_name in state['types']]
        self.immunities = [Type[type_name.upper()].value for type_name in state['immunities']]
        self.weaknesses = [Type[type_name.upper()].value for type_name in state['weaknesses']]
        self.resistances = [Type[type_name.upper()].value for type_name in state['resistances']]
        self.status = state['status']
        self.sub_status = [SubStatus[status_name.upper()] for status_name in state['sub_status']]
        self.moves = [OffensiveCapacity(attack['name'], attack['type'], attack['category'], attack['power'], attack['accuracy'], attack['pp'], attack['secondary_effect']) if isinstance(attack, OffensiveCapacity) 
                      else StatusCapacity(attack['name'], attack['type'], attack['accuracy'], attack['max_pp'], attack['secondary_effect']) for attack in state['moves']]


    def __repr__(self) -> str:
        # Return the pokemon's name, its current HP and its types greyed out if it's fainted
        if self.current_hp <= 0:
            for pokemontype in self.types:
                    pokemontype.value.color = "dark_grey"
            types_str = colored(" / ", 'dark_grey').join([str(type.value) for type in self.types]) # Affiche les deux types séparés par une barre oblique
            full_str = colored(f"{self.name} : {types_str} ~ ", 'dark_grey') + colored(f"{self.current_hp}", 'red') + colored(f"/{self.max_hp}", 'dark_grey') + colored("HP", 'dark_grey')
            for pokemontype in self.types:
                    pokemontype.value.color = pokemontype.value.default_color
            return full_str
        health_colors = {100: "green", 75: "light_green",  50: "yellow", 25: "light_red", 0: "red"}
        
        health_percentage = self.get_current_hp_percentage()
        for key in sorted(health_colors.keys(), reverse=True):
            if health_percentage >= key:
                color = health_colors[key]
                break
            
        types_str = " / ".join([str(type.value) for type in self.types])
        return f"{self.name} : {types_str} ~ {colored(self.current_hp, color)}/{self.max_hp} HP"
    
    # def __repr__(self) -> str:
    #     health_colors = {100: "green", 75: "light_green",  50: "yellow", 25: "light_red", 0: "red"}
    #     health_percentage = self.get_current_hp_percentage()
    #     for key in sorted(health_colors.keys(), reverse=True):
    #         if health_percentage >= key:
    #             color = health_colors[key]
    #             break
            
    #     types_str = " / ".join([str(type.value) for type in self.types]) # Affiche les deux types séparés par une barre oblique
    #     attacks_str = "\n".join([str(attack) for attack in self.attacks]) # Ajout d'un saut de ligne entre chaque attaque
    #     return (f"{self.name} ~ {colored(self.current_hp, color)}/{self.max_hp} HP ~ {types_str} ~ " + 
    #         f"Weaknesses: {self.weaknesses} ~ Resistances: {self.resistances} ~ Immunities: {self.immunities} ~ \n" +
    #         f"Status: {self.status.name} ~ {colored('Attack',attrs=['bold'])}: {colored(self.attack, 'red')} ~ {colored('Special Attack',attrs=['bold'])}: {colored(self.special_attack, 'cyan')} ~ {colored('Defense',attrs=['bold'])}: {colored(self.defense, 'yellow')} ~ {colored('Special Defense',attrs=['bold'])}: {colored(self.special_defense, 'green')} ~ {colored('Speed',attrs=['bold'])}: {colored(self.speed, 'blue')} ~ " +
    #         f"Attacks: \n{attacks_str}") # Ajout d'un saut de ligne avant les attaques

    def convert_hp_to_percentage(self, hp: int) -> float:
        return (hp / self.max_hp) * 100

    def get_current_hp_percentage(self) -> float:
        percentage = (self.current_hp / self.max_hp) * 100
        return round(percentage * 2) / 2
    
    def calculate_weaknesses(self) -> 'list[TypeClass]':
        weaknesses = self.get_types_weaknesses()
        resistances = self.get_types_resistances()
        for type in resistances:
            if type in weaknesses:
                weaknesses.remove(type)
        if len(self.immunities) > 0:
            for type in self.immunities:
                if type in weaknesses:
                    weaknesses.remove(type)
        return weaknesses

    def calculate_resistances(self) -> 'list[TypeClass]':
        weaknesses = self.get_types_weaknesses()
        resistances = self.get_types_resistances()
        for type in weaknesses:
            if type in resistances:
                resistances.remove(type)
        if len(self.immunities) > 0:
            for type in self.immunities:
                if type in resistances:
                    resistances.remove(type)
        return resistances
    
    def get_types_weaknesses(self) -> 'list[TypeClass]':
        weaknesses = []
        for type in self.types:
            weaknesses.extend(type.value.weaknesses)
        return weaknesses
    
    def get_types_resistances(self) -> 'list[TypeClass]':
        resistances = []
        for pokemontype in self.types:
            resistances.extend(pokemontype.value.resistances)
        return resistances
    
    def get_types_immunities(self) -> 'list[TypeClass]':
        immunities = []
        for type in self.types:
            immunities.extend(type.value.immunities)
        return immunities
    
    def print_attacks(self) -> None:
        for i, attack in enumerate(self.moves):
            print(f"{i + 1}. {attack}")
            
    def print_attacks_without_indices(self) -> None:
        for attack in self.moves:
            print(f"    {attack}")
            
    def heal(self, amount: int) -> None:
        self.current_hp += max(amount, 0)
        print(f"{self.name} was healed by {self.convert_hp_to_percentage(amount)} HP!")
            
    def attack_target(self, move: Capacity, is_secondary_effect_applied: bool, target, damage=-1) -> None:  # The target can be a the opposing pokemon, the opposing player or the player itself
        if move.current_pp > 0:
            move.current_pp -= 1
            print(f"{self.name} used {move.name}!")
            if isinstance(move, OffensiveCapacity):
                target.receive_damage(move, damage)
            if is_secondary_effect_applied:
                move.apply_secondary_effect(target)
        else:
            print(f"{self.name} has no PP left!")

    def receive_damage(self, damage: int) -> None:
        self.current_hp -= damage
        self.current_hp = max(self.current_hp, 0)
        print(f"{self.name} lost {round(self.convert_hp_to_percentage(damage), 1)}% HP!")
        self.is_dead(True)
        
    def receive_secondary_effect(self, move: Capacity) -> None:
        if move.secondary_effect:
            move.secondary_effect.apply(self)

    def get_stab_multiplier(self, attacker: 'Pokemon', attack_type: Type) -> float:
        if attack_type in attacker.types:
            return True
        return False

    def get_critical_multiplier(self) -> float:
        critical_hit_chance = 4.17
        if randint(1, 100) <= critical_hit_chance:
            print("Critical hit!")
            return True
        return False

    def get_types_multiplier(self, attack_type: Type) -> float:
        multiplier = 1

        if attack_type.value in self.weaknesses:
            print("This is very effective!")
            count = self.weaknesses.count(attack_type.value)
            for _ in range(count):
                multiplier *= 2
        if attack_type.value in self.resistances:
            print("This is not very effective...")
            count = self.resistances.count(attack_type.value)
            for _ in range(count):
                multiplier *= 0.5
        if attack_type.value in self.immunities:
            print("This has no effect...")
            multiplier *= 0

        return multiplier

    def get_multipliers(self, attack_type: Type, attacker: 'Pokemon'):
        # STAB
        stab_multiplier: bool = self.get_stab_multiplier(attacker, attack_type)
        # Critical hit
        crit_multiplier: bool = self.get_critical_multiplier()
        # Type effectiveness
        type_multiplier: int = self.get_types_multiplier(attack_type)

        return stab_multiplier, crit_multiplier, type_multiplier

    def compute_multipliers(self, multipliers: tuple[bool, bool, int]) -> float:
        multiplier = 1
        # STAB
        if multipliers[0]:
            multiplier *= 1.5
        # Critical hit
        if multipliers[1]:
            multiplier *= 1.5
        # Type effectiveness
        multiplier *= multipliers[2]
        return multiplier

    def calculate_damage(self, attack: OffensiveCapacity, attacker: 'Pokemon', multipliers) -> int:
        # Physical or Special
        if attack.category == CapacityCategory.PHYSICAL:
            attack_stat = attacker.attack
            defense_stat = self.defense
        else:
            attack_stat = attacker.special_attack
            defense_stat = self.special_defense
        multiplier = self.compute_multipliers(multipliers)
        damage = (floor(floor(attacker.lvl * 2 / 5 + 2) * attack.power * attack_stat / defense_stat) / 50) + 2 # Calculate the raw damage
        damage *= multiplier # Apply the modifiers
        damage = floor(damage * randint(85, 100) / 100)  # Apply the random factor
        return max(int(damage), 1)
    
    def is_dead(self, print_message: bool = False) -> bool:
        if self.current_hp <= 0:
            if print_message:
                print(f"{self.name} fainted !")
            return True
        
    def print_moves(self) -> None:
        if self.current_hp <= 0:
            attacks_str = colored("| Moves : ", 'dark_grey') + colored(" - ", 'dark_grey').join([colored(f"{attack.name} ({attack.get_grey_pp_number()})", 'dark_grey') for attack in self.moves])
        else:
            attacks_str = f"| Moves : " + " - ".join([f"{attack.name} ({attack.get_colored_pp_number()})" for attack in self.moves])
        return attacks_str
    
    # Status
    def apply_end_turn_primary_status(self) -> None: # At the end of the turn, apply the status
        if self.status == PrimeStatus.BURN:
            self.current_hp = max(self.current_hp - floor(self.max_hp / 16), 0)
            print(f"{self.name} is hurt by its burn!")
        elif self.status == PrimeStatus.POISON:
            self.current_hp = max(self.current_hp - floor(self.max_hp / 8), 0)
            print(f"{self.name} is hurt by poison!")
        elif self.status == PrimeStatus.SEVERE_POISON:
            poison_damage = floor(self.max_hp / 16) * self.nbr_turn_severe_poison
            self.current_hp = max(self.current_hp - poison_damage, 0)
            print(f"{self.name} is hurt by poison!")
            self.nbr_turn_severe_poison += 1

    def apply_leech_seed(self, target: 'Pokemon') -> int:
        if SubStatus.LEECH_SEED in self.sub_status:
            hp_drained = floor(self.max_hp / 8)
            self.current_hp = min(self.current_hp + hp_drained, self.max_hp)
            print(f"{target.name} is draining the energy of {self.name}!")
            return hp_drained
        
    def switch_out(self):
        self.nbr_turn_severe_poison = 0
        self.sub_status = []
        
    def switch_in(self, environment: 'EnvironmentClass') -> None:
        # Spikes
        self.switch_in_spikes(environment)
        # Stealth Rock
        self.switch_in_stealth_rock(environment)
        # Toxic Spikes
        self.switch_in_toxic_spikes(environment)
            
    def switch_in_spikes(self, environment: 'EnvironmentClass'):
        if EnvironmentElements.SPIKES in environment.elements:
            spikes_count = environment.elements.count(EnvironmentElements.SPIKES)
            if spikes_count == 1:
                spikes_damage = floor(self.max_hp / 8)
            elif spikes_count == 2:
                spikes_damage = floor(self.max_hp / 6)
            elif spikes_count >= 3:
                spikes_damage = floor(self.max_hp / 4)
            self.current_hp = max(self.current_hp - spikes_damage, 0)
            print(f"{self.name} is hurt by spikes!")
            self.is_dead(True)        
    
    def switch_in_stealth_rock(self, environment: 'EnvironmentClass'):
        if EnvironmentElements.STEALTH_ROCK in environment.elements:
            stealth_rock_damage = 12.5 # Percentage of max HP
            for type in self.types:
                if Type.ROCK.value in type.value.weaknesses:
                    stealth_rock_damage *= 2
                elif Type.ROCK.value in type.value.resistances:
                    stealth_rock_damage /= 2
            stealth_rock_damage = floor(self.max_hp * (stealth_rock_damage / 100))
            self.current_hp = max(self.current_hp - stealth_rock_damage, 0)
            print(f"{self.name} is hurt by stealth rock!")
            # print(f"{self.name} lost {self.convert_hp_to_percentage(stealth_rock_damage)}% HP!")
            self.is_dead(True)
            
    def switch_in_toxic_spikes(self, environment: 'EnvironmentClass') -> None:
        if EnvironmentElements.TOXIC_SPIKES in environment.elements:
            if Type.POISON in self.types:
                environment.remove_toxic_spikes()
                print(f"{self.name} absorbed the toxic spikes!")
            elif environment.elements.count(EnvironmentElements.TOXIC_SPIKES) == 1:
                if PrimeStatus == PrimeStatus.NORMAL:
                    self.status = PrimeStatus.POISON
                    print(f"{self.name} is poisoned by toxic spikes!")
            elif environment.elements.count(EnvironmentElements.TOXIC_SPIKES) == 2:
                if PrimeStatus == PrimeStatus.NORMAL:
                    self.status = PrimeStatus.SEVERE_POISON
                    print(f"{self.name} is badly poisoned by toxic spikes!")
            self.is_dead(True)
            
            
# Create some pokemons
Charizard = Pokemon("Charizard", 100, 78, 84, 78, 109, 85, 100, [Type.FIRE, Type.FLYING], [Flamethrower, Thunderbolt, Earthquake, LeechSeed])
Blastoise = Pokemon("Tortank", 100, 79, 83, 100, 85, 105, 78, [Type.WATER], [HydroPump, IceBeam, Earthquake, AquaTail])
Venusaur = Pokemon("Venusaur", 100, 80, 82, 83, 100, 100, 80, [Type.PLANT, Type.POISON], [QuickAttack, Thunder, Surf, SkullBash])
Mew = Pokemon("Mew", 100, 100, 100, 100, 100, 100, 100, [Type.PSYCHIC], [QuickAttack, Thunder, Surf, SkullBash])
Landorus_Therian = Pokemon("Landorus-Therian", 100, 89, 145, 90, 105, 80, 91, [Type.GROUND, Type.FLYING], [QuickAttack, Thunder, Surf, SkullBash])
Ferrothorn = Pokemon("Ferrothorn", 100, 74, 94, 131, 54, 116, 20, [Type.PLANT, Type.STEEL], [StealthRock, Thunder, Surf, LeechSeed])
Greninja = Pokemon("Greninja", 100, 72, 95, 67, 103, 71, 122, [Type.WATER, Type.DARK], [QuickAttack, Thunder, Surf, SkullBash])
