import json

from PokemonListConsole import BasePokemonList, Pokemon
from MoveListConsole import BaseMoveList, Move
from AbilityConsole import Ability
from ItemConsole import Item


class JsonDeserializer:
    def __init__(self, json_file: str):
        self.pokemons: list[Pokemon] = []
        # Load the json file
        with open(json_file, 'r') as f:
            self.team: list[dict[str: int]] = json.load(f)

    def deserialize(self) -> None:
        """Deserialize the json file to get the pokemons and their moves, ability, item, evs."""
        for pokemon_data in self.team:
            pokemon: Pokemon = BasePokemonList[pokemon_data['pokemon'].upper()].value
            pokemon.moves = [BaseMoveList[move.upper().replace(" ", "_")].value for move in pokemon_data['moves']]
            pokemon.ability = Ability[pokemon_data['ability'].upper().replace(" ", "_")]
            pokemon.item = Item[pokemon_data['item'].upper().replace(" ", "_")]
            pokemon.hp_evs = pokemon_data['evs']['hp']
            pokemon.attack_evs = pokemon_data['evs']['attack']
            pokemon.defense_evs = pokemon_data['evs']['defense']
            pokemon.special_attack_evs = pokemon_data['evs']['special_attack']
            pokemon.special_defense_evs = pokemon_data['evs']['special_defense']
            pokemon.speed_evs = pokemon_data['evs']['speed']
            self.pokemons.append(pokemon)

    def get_pokemons(self) -> list[Pokemon]:
        """Return the list of pokemons."""
        return self.pokemons


if __name__ == '__main__':
    j = JsonDeserializer('team.json')
    j.deserialize()
    team = j.get_pokemons()
    for pokemon in team:
        print(pokemon, pokemon.item, type(pokemon.ability), pokemon.moves, pokemon.hp_evs, pokemon.attack_evs, pokemon.defense_evs, pokemon.special_attack_evs, pokemon.special_defense_evs, pokemon.speed_evs)
