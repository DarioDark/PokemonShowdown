from os import system
from PokemonConsole import *


class Player:
    def __init__(self, team: 'list[Pokemon]', name: str) -> None:
        self.team: list[Pokemon] = team
        self.name: str = name
        self.current_pokemon: Pokemon = None
        self.z_crystal_used: bool = False
        self.mega_evolution_used: bool = False
        self.environment: EnvironmentClass = EnvironmentClass()
        for pokemon in self.team:
            pokemon.environment = self.environment

    def __eq__(self, other: 'Player') -> bool:
        return self.name == other.name
    
    def __getstate__(self) -> dict:
        return {
            'team': [pokemon for pokemon in self.team],
            'name': self.name,
            'current_pokemon': self.current_pokemon,
            'z_crystal_used': self.z_crystal_used,
            'mega_evolution_used': self.mega_evolution_used,
            'environment': self.environment
        }
        
    def __setstate__(self, state):
        self.team = state['team']
        self.name = state['name']
        self.current_pokemon = state['current_pokemon']
        self.z_crystal_used = state['z_crystal_used']
        self.mega_evolution_used = state['mega_evolution_used']
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
       
    def select_switch(self) -> int:
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
        is_pokemon_dead: bool = self.current_pokemon.switch_in(enemy_player)
        if is_pokemon_dead:
            return False
        return True

    def select_move(self) -> int:
        print(f"{self.current_pokemon.name}, select your move:")
        self.current_pokemon.print_attacks()
        while True:
            try:
                move_index = int(input(">> ")) - 1
                if self.current_pokemon.item in (Item.CHOICE_BAND, Item.CHOICE_SPECS, Item.CHOICE_SCARF):
                    if self.current_pokemon.moves[move_index] != self.current_pokemon.last_used_move:
                        print(f"{self.current_pokemon.name} is locked by it's {self.current_pokemon.item.name} and can't switch move!")
                        continue
                if 0 <= move_index < len(self.current_pokemon.moves):
                    if self.current_pokemon.moves[move_index].current_pp > 0:
                        return move_index
                    else:
                        print("No PP left for this move!")
                else:
                    print("Invalid choice")
            except ValueError:
                print("Invalid choice")
                
    def use_move(self, move_index: int, is_secondary_effect_applied: bool, target: 'Player', damage: int = -1, nbr_hit: int = 1) -> bool:
        move = self.current_pokemon.moves[move_index]
        attack_successful: bool = False
        if move.category == MoveCategory.STATUS:
            if target.current_pokemon.ability == Ability.MAGIC_BOUNCE:
                print(f"Magic Bounce from {target.name} reflected the status move!")
                if move.target == "player":
                    attack_successful = self.current_pokemon.attack_target(move_index, is_secondary_effect_applied, self, damage, nbr_hit)
                elif move.target == "pokemon":
                    attack_successful = self.current_pokemon.attack_target(move_index, is_secondary_effect_applied, self.current_pokemon, damage, nbr_hit)
            else:
                if move.target == "player":
                    attack_successful = self.current_pokemon.attack_target(move_index, is_secondary_effect_applied, target, damage, nbr_hit)
                elif move.target == "pokemon":
                    attack_successful = self.current_pokemon.attack_target(move_index, is_secondary_effect_applied, target.current_pokemon, damage, nbr_hit)
        else:
            attack_successful = self.current_pokemon.attack_target(move_index, is_secondary_effect_applied, target.current_pokemon, damage, nbr_hit)
        return attack_successful

    def select_z_move(self) -> int:
        print(f"{self.current_pokemon.name}, select your Z-Move:")
        self.current_pokemon.print_z_moves()
        z_moves = self.current_pokemon.get_z_moves()
        while True:
            try:
                z_move_index = int(input(">> ")) - 1
                if 0 <= z_move_index < len(self.current_pokemon.moves):
                    if isinstance(z_moves[z_move_index], str):
                        print("This move can't be used as a Z-Move!")
                        continue
                    return z_move_index
                else:
                    print("Invalid choice")
            except ValueError:
                print("Invalid choice")

    def choose_action(self, target: 'Player') -> tuple[int, int, bool]:
        """Prints the available actions for the player and returns the choice of the player.

        :param target: The opposing player
        :return: A tuple containing the choice of the player, the index of the move or the pokemon and a boolean indicating if a bonus option is activated (Mega Evolution or Z-Move)
        """
        system("cls")
        bonus_option: bool = False
        while True:
            try:
                print(f"Your pokemon : {self.current_pokemon}\nOpposing pokemon : {target.current_pokemon}\n")
                print(f"{colored(self.name, attrs=['bold'])}, what will you do ?")
                print(f"1. {colored('Switch', 'cyan', attrs=['bold'])} pokemon")
                self.print_team_without_indices()

                print(f"2. {colored('Select a move', 'red', attrs=['bold'])} on your current pokemon : {colored(self.current_pokemon.name, attrs=['underline'])}")
                self.current_pokemon.print_attacks_without_indices()

                if self.current_pokemon.can_mega_evolve():
                    if not self.mega_evolution_used:
                        if bonus_option:
                            print(f"3. {colored('Mega Evolve (activated) : ' , 'green', attrs=['bold'])}{colored(self.current_pokemon.mega_name, 'white')}")
                        else:
                            print(f"3. {colored('Mega Evolve (not activated) : ', 'green', attrs=['bold'])}{colored(self.current_pokemon.mega_name, 'dark_grey')}")
                elif self.current_pokemon.can_z_move():
                    if not self.z_crystal_used:
                        print(f"3. {colored('Use Z-Move', 'green', attrs=['bold'])}")
                        self.current_pokemon.print_z_moves_without_indices()

                choice = int(input(">> "))
                if choice == 1:
                    if target.current_pokemon:
                        if target.current_pokemon.ability == Ability.MAGNET_PULL and Type.STEEL in self.current_pokemon.types:
                            print("You are trapped by a magnetic field. You can't switch out this pokemon!")
                            continue
                        elif SubStatus.MAGMA_STORM in self.current_pokemon.sub_status:
                            print("You are trapped by a magma storm. You can't switch out this pokemon!")
                            continue
                    pokemon_index: int = self.select_switch()
                    return 1, pokemon_index, bonus_option
                elif choice == 2:
                    move_index: int = self.select_move()
                    return 2, move_index, bonus_option
                elif choice == 3:
                    if self.current_pokemon.can_mega_evolve():
                        system("cls")
                        if bonus_option:
                            bonus_option = False
                        else:
                            bonus_option = True

                    elif self.current_pokemon.can_z_move():
                        z_move_index: int = self.select_z_move()
                        return 2, z_move_index, True
                else:
                    print("Invalid choice")
            except ValueError:
                print("Invalid choice")

    def has_lost(self) -> bool:
        return all(pokemon.current_hp <= 0 for pokemon in self.team)
