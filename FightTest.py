import time
import os

from Client import Client
from PlayerTest import *
from PokemonTest import Pokemon
from Status import SubStatus


class Fight:
    def __init__(self, player1: Player) -> None:
        self.players = [player1]
        self.turn: int = 1
        self.client = Client(self.players[0])

        self.start()
        self.run()

    def __repr__(self) -> str:
        return f"Turn {self.turn} | {self.players}"

    @property
    def player1(self) -> Player:
        return self.players[0]

    @property
    def player2(self) -> Player:
        if len(self.players) > 1:
            return self.players[1]

    def start(self) -> None:
        """Start the fight by sending the player to the server and waiting for the second player to connect.
        """
        self.client.send_info(self.player1)
        self.client.enemy_player = self.client.get_enemy_player()
        self.client.send_info(self.player1)
        print("Waiting for the second player...")
        self.players.append(self.client.enemy_player)
        print("prout ?")

        os.system('cls')
        print("Both players are ready !")
        time.sleep(2)
        self.select_player_lead()

    def select_player_lead(self) -> None:
        """Select the team lead of both players.
        """
        self.client.reset_last_info()
        self.player1.current_pokemon = self.player1.select_lead()
        self.client.send_info(self.player1.current_pokemon)
        print("Waiting for the second player to select their lead...")
        while True:
            self.client.send_info(self.player1.current_pokemon)
            time.sleep(1)
            self.player2.current_pokemon = self.client.get_last_info()
            time.sleep(1)
            if self.player2.current_pokemon is not None:
                break

        print(f"{self.player1.current_pokemon.name}, go !")
        print(f"{self.player2.name} sent {self.player2.current_pokemon.name} in battle !")

    def get_players_actions(self) -> tuple:
        """Get the actions of both players.

        :return: A tuple containing the first player action and the second player action.
        :rtype: tuple
        """
        player1_action = self.player1.choose_action(self.player2)
        self.client.send_action(player1_action)
        player2_action = self.client.get_enemy_info()
        return player1_action, player2_action

    def get_player_order(self) -> tuple:
        """Get the order of the players based on their actions and speed.

        :return: A tuple containing the first player, the second player, the first player action and the second player action.
        :rtype: tuple
        """
        player1_action, player2_action = self.get_players_actions()
        # Determine the order of the players
        if player1_action[0] == 1 and player2_action[0] == 2:
            first_player = self.player1
            second_player = self.player2
        elif player1_action[0] == 2 and player2_action[0] == 1:
            first_player = self.player2
            second_player = self.player1
        else:
            # Vérifier qui est le plus rapide
            if self.player1.current_pokemon.speed > self.player2.current_pokemon.speed:
                first_player = self.player1
                second_player = self.player2
            elif self.player1.current_pokemon.speed < self.player2.current_pokemon.speed:
                first_player = self.player2
                second_player = self.player1
            else:
                # Si les deux pokemons ont la même vitesse, choisir aléatoirement
                first_player = self.players[randint(0, 1)]
                second_player = self.players[1 - self.players.index(first_player)]

        if self.player1 == first_player:
            first_player_action = player1_action
            second_player_action = player2_action
        else:
            first_player_action = player2_action
            second_player_action = player1_action
        return first_player, second_player, first_player_action, second_player_action

    def apply_end_turn_primary_status(self):
        """Apply the end turn primary status to both players.
        """
        self.player1.current_pokemon.apply_end_turn_primary_status()
        self.player2.current_pokemon.apply_end_turn_primary_status()

    def apply_end_turn_secondary_status(self):
        """Apply the end turn secondary status to both players.
        """
        for player in self.players:
            self.define_end_turn_secondary_status(player, self.players[1 - self.players.index(player)])

    def define_end_turn_secondary_status(self, player1: Player, player2: Player) -> None:
        """Apply the end turn secondary status to the player.

        :param player1: The client-side player.
        :param player2: The imported player.
        :return: None
        """
        if SubStatus.LEECH_SEED in player1.current_pokemon.sub_status:
            hp_drained = player1.current_pokemon.apply_leech_seed(player2.current_pokemon)
            player2.current_pokemon.heal(hp_drained)

    def player_use_action(self, player: Player, target: Player, action: tuple) -> None:
        if player == self.player1:  # If the player is the client
            if action[0] == 1:  # Switch
                pokemon: Pokemon = action[1]
                player.switch_pokemon(pokemon)
            elif action[0] == 2:  # Move
                if len(action) == 2:
                    print(f"{player.current_pokemon.name} missed!")
                else:
                    print(f"{player.current_pokemon.name} used {action[1].name}!")
                    result = []
                    damage: int = action[4]
                    target.current_pokemon.receive_damage(damage)
                    result.append(damage)
                    if action[3] == True:
                        secondary_effect_applied: bool = pokemon.is_secondary_effect_applied()
                        result.append(secondary_effect_applied)
                        if secondary_effect_applied:
                            target.current_pokemon.receive_secondary_effect(action[1])
                    else:
                        result.append(False)
                    self.client.send_damage(result)  # result = [damage: int, secondary_effect_applied: bool]

        else:  # If the player is the imported player
            if action[0] == 1:  # Switch
                pokemon: Pokemon = action[1]
                player.switch_pokemon(pokemon)

            elif action[0] == 2:  # Move
                if len(action) == 2:
                    print(f"{player.current_pokemon.name} missed!")
                else:
                    print(f"{player.current_pokemon.name} used {action[1].name}!")
                    result = self.client.get_enemy_info()
                    damage: int = result[0]
                    target.current_pokemon.receive_damage(damage)
                    if result[1] == True:
                        target.current_pokemon.receive_secondary_effect(result[0])

    def play_turn(self):
        first_player, second_player, first_player_action, second_player_action = self.get_player_order()

        # Effectuer les mouvements dans l'ordre
        self.player_use_action(first_player, second_player, first_player_action)

        if self.end_game():
            return
        elif first_player.current_pokemon.is_dead():
            first_player.switch_pokemon(first_player.select_switch())
        elif second_player.current_pokemon.is_dead():
            second_player.switch_pokemon(second_player.select_switch())
        else:
            self.player_use_action(second_player, first_player, second_player_action)

        if self.end_game():
            return
        elif first_player.current_pokemon.is_dead():
            first_player.switch_pokemon(first_player.select_switch())
        elif second_player.current_pokemon.is_dead():
            second_player.switch_pokemon(second_player.select_switch())

        # Apply end turn status
        self.apply_end_turn_primary_status()
        if self.end_game():
            return
        self.apply_end_turn_secondary_status()
        if self.end_game():
            return
        self.turn += 1

    def check_looser(self) -> Player:
        if self.player1.has_lost():
            return self.player1
        if self.player2.has_lost():
            return self.player2

    def end_game(self) -> bool:
        looser = self.check_looser()
        if looser:
            print(f"{looser.name} has lost !")
            return True
        return False

    def run(self) -> None:
        while True:
            self.play_turn()
            if self.end_game():
                break
            input("Press enter to continue...")


from random import randint


def main():
    rand = randint(0, 10)
    P = Player([Blastoise, Venusaur, Charizard], f"Player {rand}")
    F = Fight(P)
    print("Game over !")


if __name__ == "__main__":
    main()
