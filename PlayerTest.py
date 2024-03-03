from PokemonTest import *
from OffensiveCapacityCopy import *
from random import randint
from Environment import EnvironmentClass, EnvironmentElements

class Player:
    def __init__(self, team: 'list[Pokemon]', name: str) -> None:
        self.team: list[Pokemon] = team
        self.name: str = name
        self.current_pokemon: Pokemon = None
        self.environment: EnvironmentClass = EnvironmentClass()
        
    # def __repr__(self) -> str:
    #     return f"{self.name} has {colored(self.current_pokemon.name, attrs=['underline'])} in battle"    
        
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
    
    def select_lead(self) -> Pokemon:
        print(f"{self.name}, select your lead:")
        self.print_team()
        while True:
            try:
                lead = int(input(">> ")) - 1
                if 0 <= lead < len(self.team):
                    # print(f"{self.team[lead].name} is going first !")
                    return self.team[lead]
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
       
    def select_switch(self) -> Pokemon:
        print(f"{self.name}, select your next pokemon:")
        self.print_team()
        while True:
            try:
                switch = int(input(">> ")) - 1
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
            
    def switch_pokemon(self, switch: Pokemon) -> None:
        print(f"{self.current_pokemon.name}, come back!")
        self.current_pokemon.switch_out()
        self.current_pokemon = self.team[switch]
        print(f"{self.team[switch].name}, go!")
        self.current_pokemon.switch_in(self.environment)
         
    def select_move(self) -> None:
        print(f"{self.current_pokemon.name}, select your move:")
        self.current_pokemon.print_attacks()
        while True:
            try:
                move = int(input(">> ")) - 1
                if 0 <= move < len(self.current_pokemon.moves):
                    if self.current_pokemon.moves[move].current_pp > 0:
                        return self.current_pokemon.moves[move]
                    else:
                        print("No PP left for this move!")
                else:
                    print("Invalid choice")
            except ValueError:
                print("Invalid choice")
                
    def use_move(self, move: Capacity, target: 'Player', move_success: bool) -> tuple:
        if move_success:
            if isinstance(move, StatusCapacity):
                if move.target == "player":
                    return self.current_pokemon.attack_target(move, target)
                elif move.target == "self":
                    return self.current_pokemon.attack_target(move, self)
            return self.current_pokemon.attack_target(move, target.current_pokemon) 
        else:
            print(f"{self.current_pokemon.name} missed!")
            return None
                
    def choose_action(self, target: 'Player') -> tuple:
        system("cls")
        print(self)
        print(target)
        while True:
            try:
                print(f"{colored(self.name, attrs=['bold'])}, what will you do ?")
                print(f"1. {colored('Switch', 'cyan', attrs=['bold'])} pokemon")
                self.print_team_without_indices()
                print(f"2. {colored('Select a move', 'red', attrs=['bold'])} on your current pokemon : {colored(self.current_pokemon.name, attrs=['underline'])}")
                self.current_pokemon.print_attacks_without_indices()
                choice = int(input(">> "))
                if choice == 1:
                    pokemon: Pokemon = self.select_switch()
                    return 1, pokemon
                elif choice == 2:
                    result = [2]  # result = [action, move, move_success: bool, secondary_effect: bool, damage: int]
                    move: Capacity = self.select_move()
                    if randint(1, 100) <= move.accuracy:
                        result.append(move)
                        result.append(True)
                        if move.is_secondary_effect_applied():
                            result.append(True)
                        else:
                            result.append(False)
                        if isinstance(move, OffensiveCapacity):
                            damage: int = self.current_pokemon.calculate_damage(move, target.current_pokemon)
                            result.append(damage)
                            return tuple(result)
                        else:
                            return tuple(result)
                    else:  # result = [action, move]
                        result.append(move)
                        return tuple(result)
                    
                else:
                    print("Invalid choice")
            except ValueError:
                print("Invalid choice")

    def has_lost(self) -> bool:
        return all(pokemon.current_hp <= 0 for pokemon in self.team)





def main():
    system("cls")  
    Player1 = Player([Charizard, ], "Red")
    Player2 = Player([Charizard], "Blue")
    system("cls")
    Player1.choose_action(Player2)
    
if __name__ == "__main__":
    main()