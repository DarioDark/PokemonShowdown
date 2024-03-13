import time
from PokemonListConsole import *
from ClientConsole import Client
from PlayerConsole import *
from StatusConsole import SubStatus


class Fight:
    def __init__(self, player1: Player) -> None:
        self.players = [player1]
        self.turn: int = 1
        self.client = Client(self.player1)

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
        self.client.start()
        print("Waiting for the second player...")
        self.players.append(self.client.get_enemy_player())
        print("Both players are ready !")
        time.sleep(2)
        system("cls")
        self.select_player_lead()

    def select_player_lead(self) -> None:
        """Select the team lead of both players.
        """
        pokemon_index: int = self.player1.select_lead(self.player2.team)
        self.player1.current_pokemon = self.player1.team[pokemon_index]
        self.client.send_info(pokemon_index)

        print("Waiting for the second player to select their lead...")
        pokemon_index = self.client.get_last_info()
        self.player2.current_pokemon = self.player2.team[pokemon_index]

        print(f"{self.player1.current_pokemon.name}, go !")
        print(f"{self.player2.name} sent {self.player2.current_pokemon.name} in battle !")

    def get_players_actions(self) -> tuple:
        """Get the actions of both players.

        :return: A tuple containing the first player action and the second player action.
        :rtype: tuple
        """
        player1_action: tuple[int, int] = self.player1.choose_action(self.player2)
        self.client.send_info(player1_action)
        player2_action = self.client.get_last_info()
        return player1_action, player2_action

    def get_player_order(self) -> tuple:
        """Get the order of the players based on their actions and speed.

        :return: A tuple containing the first player, the second player, the first player action and the second player action.
        :rtype: tuple
        """
        # We get both actions: tuple[int, int]
        player1_action, player2_action = self.get_players_actions()
        player1_choice = player1_action[0]
        player2_choice = player2_action[0]

        # Determine the order of the players
        if player1_choice == 1 and player2_choice == 2:
            first_player = self.player1
            second_player = self.player2
        elif player1_choice == 2 and player2_choice == 1:
            first_player = self.player2
            second_player = self.player1
        else:
            # Checks who has the fastest pokemon
            if self.player1.current_pokemon.speed > self.player2.current_pokemon.speed:
                first_player = self.player1
                second_player = self.player2
            elif self.player1.current_pokemon.speed < self.player2.current_pokemon.speed:
                first_player = self.player2
                second_player = self.player1
            else:
                # If both pokemons are equally fast
                self.client.send_info("Speed tie")
                first_player_index = self.client.get_last_info()
                if first_player_index == -1:
                    first_player_index = 1
                first_player = self.players[first_player_index]
                second_player = self.players[1 - first_player_index]

        # Assignation of actions to player
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
            self.apply_end_turn_secondary_status_effects(player, self.players[1 - self.players.index(player)])

    def apply_end_turn_secondary_status_effects(self, player1: Player, player2: Player) -> None:
        """Apply the end turn secondary status to the player.

        :param player1: The client-side player.
        :param player2: The imported player.
        :return: None
        """
        if SubStatus.LEECH_SEED in player1.current_pokemon.sub_status:
            hp_drained = player1.current_pokemon.apply_leech_seed(player2.current_pokemon)
            player2.current_pokemon.heal(hp_drained)
            if player1.current_pokemon.is_dead(True):
                if player1 == self.player1:
                    switch = player1.select_switch(player2.current_pokemon)
                    final_switch = self.player_switch_in(player1, switch)
                    self.client.send_info(final_switch)
                else:
                    switch = self.client.get_last_info()
                    self.player_switch_in(player1, switch)

    def player_use_action(self, player: Player, target: Player, action: tuple) -> None:
        """Takes a player, a target, and tuple that contains a choice and the associated object.

        :param player: A Player object, the one that does the action.
        :param target: A Player object, the target of the action.
        :param action: A tuple with 1 or 2 as it's first value and a Pokemon or a Capacity object as the second value.
        """
        # If the player is the client
        if player == self.player1:
            # If the player selected a switch
            if action[0] == 1:
                pokemon: int = action[1]
                player.switch_pokemon(pokemon, self.player2)

            # If the player selected a move
            elif action[0] == 2:
                move_index: int = action[1]
                move: Capacity = player.current_pokemon.moves[move_index]
                print(f"{player.current_pokemon.name} used {move.name}!")

                # If the pokemon misses
                if randint(0, 100) > move.accuracy:
                    result: tuple[bool] = False,
                    print(f"{player.current_pokemon.name} missed!")
                    self.client.send_info(result)
                    return

                # Getting all the pieces of information of the move to send them and synchronize both clients
                if isinstance(move, OffensiveCapacity):
                    temp_move = deepcopy(move)
                    if player.current_pokemon.ability == Ability.AERILATE and temp_move.type == Type.NORMAL:
                        temp_move.type = Type.FLYING
                    multipliers: tuple[bool, bool, float] = target.current_pokemon.get_multipliers(move, player.current_pokemon)
                    damage: int = target.current_pokemon.calculate_damage(temp_move, player.current_pokemon, multipliers)
                else:
                    multipliers = (False, False, 1)
                    damage: int = -1
                secondary_effect_applied: bool = move.is_secondary_effect_applied(player.current_pokemon)

                # Sending the results to the server
                result: tuple[tuple[bool, bool, float], bool, int] = (multipliers, secondary_effect_applied, damage)
                self.client.send_info(result)

                # Applying the local results to the imported target
                player.use_move(move_index, secondary_effect_applied, target, damage)

        # If the player is the imported player
        elif player == self.player2:
            # If the player selected a switch
            if action[0] == 1:
                pokemon: int = action[1]
                player.switch_pokemon(pokemon, self.player1)

            # If the player selected a move
            elif action[0] == 2:
                move_index: int = action[1]
                result: tuple[tuple[bool, bool, int], bool, int] = self.client.get_last_info()
                # If the move missed
                if len(result) == 1:
                    print(f"{player.current_pokemon.name} missed!")

                # If the move didn't miss
                else:
                    move: Capacity = player.current_pokemon.moves[move_index]
                    print(f"{player.current_pokemon.name} used {move.name}!")

                    if isinstance(move, OffensiveCapacity):
                        multipliers: tuple[bool, bool, int] = result[0]

                        # Critical hit
                        if multipliers[1]:
                            print("Critical Hit!")

                        # Type effectiveness multiplier
                        type_multiplier = multipliers[2]
                        if type_multiplier == 0:
                            print("This has no effect")
                        elif type_multiplier < 1:
                            print("This is not very effective...")
                        elif type_multiplier > 1:
                            print("This is very effective!")

                    # Applying the imported results to the local target
                    secondary_effect_applied: bool = result[1]
                    damage = result[2]
                    player.use_move(move_index, secondary_effect_applied, target, damage)

    def player_switch_in(self, player: Player, pokemon_index: int) -> int:
        """Tries to switch in a pokemon for the player until it succeeds.

        :param player: A player object, the one that switches his pokemon.
        :param pokemon_index: An integer, the index of the pokemon to switch in.
        :return:
        """
        switch: int = pokemon_index
        if player == self.player1:
            target = self.player2
        else:
            target = self.player1
        while True:
            if player.switch_pokemon(switch, target):
                return switch
            self.end_game()
            if player.current_pokemon.is_dead():
                switch = player.select_switch(target.current_pokemon)

    def play_turn(self):
        """Handles the whole process of each player using their selected action and checking if one of the pokemon dies."""
        first_player, second_player, first_player_action, second_player_action = self.get_player_order()
        self.player_use_action(first_player, second_player, first_player_action)

        if self.end_game():
            return
        elif self.player1.current_pokemon.is_dead():
            self.player2.current_pokemon.opponent_died()
            switch: int = self.player1.select_switch(self.player2.current_pokemon)
            final_switch = self.player_switch_in(self.player1, switch)
            self.client.send_info(final_switch)
        elif self.player2.current_pokemon.is_dead():
            self.player1.current_pokemon.opponent_died()
            print("Waiting for the second player to select their next pokemon...")
            switch: int = self.client.get_last_info()
            self.player_switch_in(self.player2, switch)
        else:
            self.player_use_action(second_player, first_player, second_player_action)

        if self.end_game():
            return
        elif self.player1.current_pokemon.is_dead():
            self.player2.current_pokemon.opponent_died()
            switch: int = self.player1.select_switch(self.player2.current_pokemon)
            final_switch = self.player_switch_in(self.player1, switch)
            self.client.send_info(final_switch)
        elif self.player2.current_pokemon.is_dead():
            self.player1.current_pokemon.opponent_died()
            print("Waiting for the second player to select their next pokemon...")
            switch: int = self.client.get_last_info()
            self.player_switch_in(self.player2, switch)

        # Apply end turn status
        self.apply_end_turn_primary_status()
        if self.end_game():
            return
        self.apply_end_turn_secondary_status()
        if self.end_game():
            return

        self.turn += 1

    def check_looser(self) -> Player:
        """Checks if one of the players has his whole team fainted.

        :return: The player that has lost the game if there is one, else None.
        """
        if self.player1.has_lost():
            return self.player1
        if self.player2.has_lost():
            return self.player2

    def end_game(self) -> bool:
        """Checks if the game has ended.

        :return: True if the game has ended, else False.
        """
        looser = self.check_looser()
        if looser:
            print(f"{looser.name} has lost !")
            return True
        return False

    def run(self) -> None:
        """Runs the game until it ends.
        """
        while True:
            self.play_turn()
            if self.end_game():
                break
            input("Press enter to continue...")


def main():
    rand = randint(0, 1000)
    p = Player(team=[CHARIZARD, Blastoise, Blacephalon, Ferrothorn, Magnezone, Mew], name=f"Player {rand}")
    Fight(p)
    print("Game over !")


if __name__ == "__main__":
    main()
