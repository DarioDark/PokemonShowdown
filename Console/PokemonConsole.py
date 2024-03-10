from math import floor

from OffensiveCapacityConsole import *
from StatusCapacityConsole import *

from StatusConsole import PrimeStatus, SubStatus
from EnvironmentConsole import EnvironmentElements, EnvironmentClass


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
        self.attack_stat: int = attack
        self.special_attack_stat: int = special_attack
        self.defense_stat: int = defense
        self.special_defense_stat: int = special_defense
        self.speed_stat: int = speed

        self.attack_boosts: int = 0
        self.defense_boosts: int = 0
        self.special_attack_boosts: int = 0
        self.special_defense_boosts: int = 0
        self.speed_boosts: int = 0

        # Types
        self.types: list[Type] = types
        self.immunities: list[Type] = self.get_types_immunities()
        self.weaknesses: list[Type] = self.calculate_weaknesses()
        self.resistances: list[Type] = self.calculate_resistances()
        # Status
        self.status: PrimeStatus = PrimeStatus.NORMAL
        self.sub_status: list[SubStatus] = []
        self.nbr_turn_severe_poison: int = 0
        
        self.moves: list = moves
    
    def __getstate__(self):
        return {
            'name': self.name,
            'lvl': self.lvl,
            'current_hp': self.current_hp,
            'max_hp': self.max_hp,
            'attack_stat': self.attack_stat,
            'special_attack_stat': self.special_attack_stat,
            'defense_stat': self.defense_stat,
            'special_defense_stat': self.special_defense_stat,
            'speed_stat': self.speed_stat,
            'attack_boosts': self.attack_boosts,
            'defense_boosts': self.defense_boosts,
            'special_attack_boosts': self.special_attack_boosts,
            'special_defense_boosts': self.special_defense_boosts,
            'speed_boosts': self.speed_boosts,
            'types': [pokemon_type.name for pokemon_type in self.types],
            'immunities': [pokemon_type.name for pokemon_type in self.immunities],
            'weaknesses': [pokemon_type.name for pokemon_type in self.weaknesses],
            'resistances': [type.name for type in self.resistances],
            'status': self.status,
            'sub_status': [status.name for status in self.sub_status],
            'moves': [attack.__getstate__() for attack in self.moves],
            'nbr_turn_severe_poison': self.nbr_turn_severe_poison
        }
        
    def __setstate__(self, state):
        self.name = state['name']
        self.lvl = state['lvl']
        self.current_hp = state['current_hp']
        self.max_hp = state['max_hp']
        self.attack_stat = state['attack_stat']
        self.special_attack_stat = state['special_attack_stat']
        self.defense_stat = state['defense_stat']
        self.special_defense_stat = state['special_defense_stat']
        self.speed_stat = state['speed_stat']
        self.attack_boosts = state['attack_boosts']
        self.defense_boosts = state['defense_boosts']
        self.special_attack_boosts = state['special_attack_boosts']
        self.special_defense_boosts = state['special_defense_boosts']
        self.speed_boosts = state['speed_boosts']
        self.types = [Type[type_name.upper()] for type_name in state['types']]
        self.immunities = [Type[type_name.upper()] for type_name in state['immunities']]
        self.weaknesses = [Type[type_name.upper()] for type_name in state['weaknesses']]
        self.resistances = [Type[type_name.upper()] for type_name in state['resistances']]
        self.status = state['status']
        self.sub_status = [SubStatus[status_name.upper()] for status_name in state['sub_status']]
        self.nbr_turn_severe_poison = state['nbr_turn_severe_poison']
        self.moves = []
        for attack_state in state['moves']:
            if attack_state['category'] == 'PHYSICAL' or attack_state['category'] == 'SPECIAL':
                attack = OffensiveCapacity()
                attack.__setstate__(attack_state)
            else:
                attack = StatusCapacity()
                attack.__setstate__(attack_state)
            self.moves.append(attack)

    def __repr__(self) -> str:
        # Return the pokemon's name, its current HP and its types greyed out if it's fainted
        if self.current_hp <= 0:
            for pokemon_type in self.types:
                pokemon_type.value.color = "dark_grey"
            types_str = colored(" / ", 'dark_grey').join([str(type.value) for type in self.types]) # Affiche les deux types séparés par une barre oblique
            full_str = colored(f"{self.name} : {types_str} ~ ", 'dark_grey') + colored(f"{self.current_hp}", 'red') + colored(f"/{self.max_hp}", 'dark_grey') + colored("HP", 'dark_grey')
            for pokemon_type in self.types:
                pokemon_type.value.color = pokemon_type.value.default_color
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

    @property
    def attack(self) -> int:
        return self.attack_stat + (self.attack_boosts * self.attack_stat // 2)

    @property
    def special_attack(self) -> int:
        return self.special_attack_stat + (self.special_attack_boosts * self.special_attack_stat // 2)

    @property
    def defense(self) -> int:
        return self.defense_stat + (self.defense_boosts * self.defense_stat // 2)

    @property
    def special_defense(self) -> int:
        return self.special_defense_stat + (self.special_defense_boosts * self.special_defense_stat // 2)

    def convert_hp_to_percentage(self, hp: int) -> float:
        """Converts the HP to a percentage of the max HP.

        :param hp: The amount of HP to convert
        :return: The percentage of the max HP
        """
        return (hp / self.max_hp) * 100

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
        resistances = []
        for pokemon_type in self.types:
            resistances.extend(pokemon_type.value.resistances)
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
        """Prints the attacks of the pokemon with their indices.
        """
        for i, attack in enumerate(self.moves):
            print(f"{i + 1}. {attack}")
            
    def print_attacks_without_indices(self) -> None:
        """Prints the attacks of the pokemon without their indices.
        """
        for attack in self.moves:
            print(f"    {attack}")
            
    def heal(self, amount: int) -> None:
        """Heals the pokemon by a certain amount.
        """
        self.current_hp += max(amount, 0)
        print(f"{self.name} was healed by {round(self.convert_hp_to_percentage(amount), 1)} HP!")
            
    def attack_target(self, move: int, is_secondary_effect_applied: bool, target: 'Pokemon or Player', damage=-1) -> None:  # The target can be a the opposing pokemon, the opposing player or the player itself
        """The pokemon attacks the target with a move.

        :param move: The index of the move to use
        :param is_secondary_effect_applied: Whether the secondary effect is applied
        :param target: The target of the attack
        :param damage: The damage to apply to the target
        """
        capacity = self.moves[move]
        if capacity.current_pp > 0:
            capacity.current_pp -= 1
            if isinstance(capacity, OffensiveCapacity):
                target.receive_damage(damage)
            if not target.is_dead():
                if is_secondary_effect_applied:
                    capacity.apply_secondary_effect(target)
        else:
            print(f"{self.name} has no PP left!")

    def receive_damage(self, damage: int) -> None:
        """The pokemon receives damage.

        :param damage: The amount of damage to receive
        """
        if damage == 0:
            return
        self.current_hp -= damage
        self.current_hp = max(self.current_hp, 0)
        print(f"{self.name} lost {min(round(self.convert_hp_to_percentage(damage), 1), 100)}% HP!")
        self.is_dead(True)
        
    def receive_secondary_effect(self, move: Capacity) -> None:
        """The pokemon receives the secondary effect of a move.

        :param move: The move that has a secondary effect
        """
        if move.secondary_effect:
            move.secondary_effect.apply(self)

    def get_stab_multiplier(self, attacker: 'Pokemon', attack_type: Type) -> bool:
        """Returns whether the move has STAB or not.

        :param attacker: The pokemon that uses the move
        :param attack_type: The type of the move
        :return: Whether the move has STAB or not
        """
        if attack_type in attacker.types:
            return True
        return False

    def get_critical_multiplier(self, move: Capacity) -> bool:
        """Returns whether the move has a critical hit or not.

        :param move: The move used
        :return: Whether the move has a critical hit or not
        """
        if isinstance(move, OffensiveCapacity):
            critical_hit_chance = 4.17
            if randint(1, 100) <= critical_hit_chance:
                print("Critical hit!")
                return True
        return False

    def get_types_multiplier(self, attack_type: Type) -> float:
        """Returns the type effectiveness multiplier of the move.

        :param attack_type: The type of the move
        :return: The type effectiveness multiplier of the move
        """
        multiplier = 1
        print("attack type", attack_type, attack_type.value)
        print("weaknesses", self.weaknesses)
        print("resistances", self.resistances)
        print("immunities", self.immunities)
        if attack_type in self.immunities:
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

    def get_multipliers(self, move: Capacity, attacker: 'Pokemon') -> tuple[bool, bool, float]:
        """Returns the multipliers of the move.

        :param move: The move used
        :param attacker: The pokemon that uses the move
        :return: The multipliers of the move
        """
        move_type = move.type
        # STAB
        stab_multiplier: bool = self.get_stab_multiplier(attacker, move_type)
        # Critical hit
        crit_multiplier: bool = self.get_critical_multiplier(move)
        # Type effectiveness
        type_multiplier: float = self.get_types_multiplier(move_type)

        return stab_multiplier, crit_multiplier, type_multiplier

    def compute_multipliers(self, multipliers: tuple[bool, bool, int]) -> float:
        """Computes the multiplier of the move.

        :param multipliers: The multipliers of the move
        :return: The total multiplier of the move
        """
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
        """Calculates the damage of the move.

        :param attack: The move used
        :param attacker: The pokemon that uses the move
        :param multipliers: The multipliers of the move
        :return: The damage of the move
        """
        if multipliers[2] == 0.0:
            return 0
        # Physical or Special
        if attack.category == CapacityCategory.PHYSICAL:
            attack_stat = attacker.attack
            defense_stat = self.defense
        else:
            attack_stat = attacker.special_attack
            defense_stat = self.special_defense
        multiplier = self.compute_multipliers(multipliers)
        damage = (floor(floor(attacker.lvl * 2 / 5 + 2) * attack.power * attack_stat / defense_stat) / 50) + 2 # Calculate the raw damage
        damage *= multiplier  # Apply the modifiers
        damage = floor(damage * randint(85, 100) / 100)  # Apply the random factor
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

    def switch_in_stealth_rock(self, environment: 'EnvironmentClass'):
        if EnvironmentElements.STEALTH_ROCK in environment.elements:
            stealth_rock_damage = 12.5  # Percentage of max HP
            for pokemon_type in self.types:
                if Type.ROCK in pokemon_type.value.weaknesses:
                    stealth_rock_damage *= 2
                elif Type.ROCK in pokemon_type.value.resistances:
                    stealth_rock_damage /= 2
            stealth_rock_damage = floor(self.max_hp * (stealth_rock_damage / 100))
            self.current_hp = max(self.current_hp - stealth_rock_damage, 0)
            print(self.current_hp, self.max_hp)
            print(f"{self.name} is hurt by stealth rock!")
            # print(f"{self.name} lost {self.convert_hp_to_percentage(stealth_rock_damage)}% HP!")
            self.is_dead(True)

    def switch_in_spikes(self, environment: 'EnvironmentClass'):
        if Type.FLYING in self.types:
            return
        elif EnvironmentElements.SPIKES in environment.elements:
            spikes_count = environment.elements.count(EnvironmentElements.SPIKES)
            spikes_damage = 0
            if spikes_count == 1:
                spikes_damage = floor(self.max_hp / 8)
            elif spikes_count == 2:
                spikes_damage = floor(self.max_hp / 6)
            elif spikes_count >= 3:
                spikes_damage = floor(self.max_hp / 4)
            self.current_hp = max(self.current_hp - spikes_damage, 0)
            print(f"{self.name} is hurt by spikes!")
            self.is_dead(True)
            
    def switch_in_toxic_spikes(self, environment: 'EnvironmentClass') -> None:
        if Type.FLYING in self.types:
            return
        elif EnvironmentElements.TOXIC_SPIKES in environment.elements:
            if Type.POISON in self.types:
                environment.remove_toxic_spikes()
                print(f"{self.name} absorbed the toxic spikes!")
                print(environment.elements)
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