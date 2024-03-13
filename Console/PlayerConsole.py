from os import system
from PokemonConsole import *


class Player:
    def __init__(self, team: 'list[Pokemon]', name: str) -> None:
        self.team: list[Pokemon] = team
        self.name: str = name
        self.current_pokemon: Pokemon = None
        self.environment: EnvironmentClass = EnvironmentClass()
        for pokemon in self.team:
            pokemon.environment = self.environment

    def __eq__(self, other: 'Player') -> bool:
        return self.name == other.name
    
    def __getstate__(self):
        return {
            'team': [pokemon for pokemon in self.team],
            'name': self.name,
            'current_pokemon': self.current_pokemon,
            'environment': self.environment
        }
        
    def __setstate__(self, state):
        self.team = state['team']
        self.name = state['name']
        self.current_pokemon = state['current_pokemon']
        self.environment = state['environment'] 
    
    def select_lead(self, enemy_team: list[Pokemon]) -> int:
        enemy_team_string = '- ' + '\n- '.join(str(pokemon) for pokemon in enemy_team)
        print(f"Enemy team :\n{enemy_team_string}\n")

        print(f"{colored(self.name, attrs=['bold'])}, select your lead:")
        self.print_team()
        while True:
            try:
                lead_index = int(input(">> ")) - 1
                if 0 <= lead_index < len(self.team):
                    # print(f"{self.team[lead].name} is going first !")
                    return lead_index
                else:
                    print("Invalid choice")
            except ValueError:
                print("Invalid choice")

    def print_team(self) -> None:
        for i, pokemon in enumerate(self.team):
            print(f"{i + 1}. {pokemon} {pokemon.print_moves()}")
            
    def print_team_without_indices(self) -> None:
        for pokemon in self.team:
            print(f"    {pokemon} {pokemon.print_moves()}")
       
    def select_switch(self, enemy_current_pokemon: Pokemon = None) -> int:
        print(f"{self.name}, select your next pokemon:")
        self.print_team()
        while True:
            try:
                switch: int = int(input(">> ")) - 1
                if 0 <= switch < len(self.team):
                    if self.team[switch].current_hp > 0:
                        if self.team[switch] != self.current_pokemon:
                            return switch
                        else:
                            print("This pokemon is already in battle !")
                    else:
                        print("This pokemon is fainted !")
                else:
                    print("Invalid choice")
            except ValueError:
                print("Invalid choice")
            
    def switch_pokemon(self, pokemon_index: int, enemy_player) -> bool:
        print(f"{self.current_pokemon.name}, come back!")
        pokemon: Pokemon = self.team[pokemon_index]
        self.current_pokemon.switch_out()
        self.current_pokemon = pokemon
        print(f"{pokemon.name}, go!")
        if self.current_pokemon.ability == Ability.INTIMIDATE:
            print(f"{self.current_pokemon.name} intimidates the opposing pokemon!")
            enemy_player.current_pokemon.lower_attack(1)
        self.current_pokemon.switch_in(enemy_player)
        if self.current_pokemon.is_dead():
            return False
        return True

    def select_move(self) -> int:
        print(f"{self.current_pokemon.name}, select your move:")
        self.current_pokemon.print_attacks()
        while True:
            try:
                move = int(input(">> ")) - 1
                if self.current_pokemon.object in (PokeObject.CHOICE_BAND, PokeObject.CHOICE_SPECS, PokeObject.CHOICE_SCARF):
                    if self.current_pokemon.moves[move] != self.current_pokemon.last_used_move:
                        print(f"{self.current_pokemon.name} is locked by it's {self.current_pokemon.object.name} and can't switch move!")
                        continue
                if 0 <= move < len(self.current_pokemon.moves):
                    if self.current_pokemon.moves[move].current_pp > 0:
                        return move
                    else:
                        print("No PP left for this move!")
                else:
                    print("Invalid choice")
            except ValueError:
                print("Invalid choice")
                
    def use_move(self, move: int, is_secondary_effect_applied: bool, target: 'Player', damage: int = -1) -> None:
        capacity = self.current_pokemon.moves[move]
        if isinstance(capacity, StatusCapacity):
            if target.current_pokemon.ability == Ability.MAGIC_BOUNCE:
                print(f"Magic Bounce from {target.name} reflected the status move!")
                if capacity.target == "enemy_player":
                    self.current_pokemon.attack_target(move, is_secondary_effect_applied, self, damage)
                elif capacity.target == "enemy_pokemon":
                    self.current_pokemon.attack_target(move, is_secondary_effect_applied, self.current_pokemon, damage)
            else:
                if capacity.target == "enemy_player":
                    self.current_pokemon.attack_target(move, is_secondary_effect_applied, target, damage)
                elif capacity.target == "self_player":
                    self.current_pokemon.attack_target(move, is_secondary_effect_applied, self, damage)
                elif capacity.target == "self_pokemon":
                    self.current_pokemon.attack_target(move, is_secondary_effect_applied, self.current_pokemon, damage)
                elif capacity.target == "enemy_pokemon":
                    self.current_pokemon.attack_target(move, is_secondary_effect_applied, target.current_pokemon, damage)
        else:
            self.current_pokemon.attack_target(move, is_secondary_effect_applied, target.current_pokemon, damage)

    def choose_action(self, target: 'Player') -> tuple[int, 'Capacity / int']:
        system("cls")
        print(f"Your pokemon : {self.current_pokemon}\nOpposing pokemon : {target.current_pokemon}\n")
        while True:
            try:
                print(f"{colored(self.name, attrs=['bold'])}, what will you do ?")
                print(f"1. {colored('Switch', 'cyan', attrs=['bold'])} pokemon")
                self.print_team_without_indices()
                print(f"2. {colored('Select a move', 'red', attrs=['bold'])} on your current pokemon : {colored(self.current_pokemon.name, attrs=['underline'])}")
                self.current_pokemon.print_attacks_without_indices()
                choice = int(input(">> "))
                if choice == 1:
                    if target.current_pokemon:
                        if target.current_pokemon.ability == Ability.MAGNET_PULL and Type.STEEL in self.current_pokemon.types:
                            print("You are trapped by a magnetic field. You can't switch out this pokemon!")
                            continue
                    pokemon_index: int = self.select_switch(target.current_pokemon)
                    return 1, pokemon_index
                elif choice == 2:
                    move_index: int = self.select_move()
                    return 2, move_index
                else:
                    print("Invalid choice")
            except ValueError:
                print("Invalid choice")

    def has_lost(self) -> bool:
        return all(pokemon.current_hp <= 0 for pokemon in self.team)
