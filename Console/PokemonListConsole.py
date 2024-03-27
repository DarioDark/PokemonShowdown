from enum import Enum
from PokemonConsole import *
from MoveListConsole import *

# Create the base pokemons
Charizard = Pokemon("Charizard", 297, 204, 192, 254, 206, 236, [Type.FIRE, Type.FLYING], [FlameThrower, Psychic, Fire_Blast, Air_Slash, Hurricane], [Ability.BLAZE], [(296, 258, 296, 206, 236, Ability.TOUGH_CLAWS, [Type.FIRE, Type.DRAGON]), (244, 192, 354, 266, 236, Ability.DROUGHT, [Type.FIRE, Type.FLYING])])
Alakazam = Pokemon("Alakazam", 251, 136, 126, 306, 226, 276, [Type.PSYCHIC], [], [Ability.MAGIC_GUARD, Ability.INNER_FOCUS], [(136, 166, 386, 246, 336, Ability.TRACE, [Type.PSYCHIC])])
Blaziken = Pokemon("Blaziken", 301, 276, 176, 256, 176, 196, [Type.FIRE, Type.FIGHT], [], [Ability.SPEED_BOOST], [(356, 196, 296, 196, 236, Ability.SPEED_BOOST, [Type.FIRE, Type.FIGHT])])
Garchomp = Pokemon("Garchomp", 357, 296, 226, 196, 206, 240, [Type.DRAGON, Type.GROUND], [], [Ability.ROUGH_SKIN], [(376, 266, 276, 226, 220, Ability.SAND_FORCE, [Type.DRAGON, Type.GROUND])])
Medicham = Pokemon("Medicham", 261, 156, 186, 156, 186, 196, [Type.FIGHT, Type.PSYCHIC], [], [Ability.PURE_POWER], [(236, 206, 196, 206, 236, Ability.PURE_POWER, [Type.FIGHT, Type.PSYCHIC])])
Scizor = Pokemon("Scizor", 281, 296, 236, 146, 196, 166, [Type.BUG, Type.STEEL], [], [Ability.TECHNICIAN], [(336, 316, 166, 236, 186, Ability.TECHNICIAN, [Type.BUG, Type.STEEL])])
Diancie = Pokemon("Diancie", 241, 236, 336, 236, 336, 136, [Type.ROCK, Type.FAIRY], [], [Ability.CLEAR_BODY], [(356, 256, 356, 256, 256, Ability.MAGIC_BOUNCE, [Type.ROCK, Type.FAIRY])])
Salamence = Pokemon("Salamence", 331, 306, 196, 256, 196, 236, [Type.DRAGON, Type.FLYING], [], [Ability.INTIMIDATE], [(326, 296, 276, 216, 276, Ability.AERILATE, [Type.DRAGON, Type.FLYING])])
Swampert = Pokemon("Swampert", 341, 256, 216, 206, 216, 156, [Type.WATER, Type.GROUND], [], [Ability.TORRENT], [(336, 256, 226, 256, 176, Ability.SWIFT_SWIM, [Type.WATER, Type.GROUND])])
Lopunny = Pokemon("Lopunny", 271, 188, 204, 144, 228, 246, [Type.NORMAL, Type.FIGHT], [], [Ability.LIMBER], [(308, 224, 144, 228, 306, Ability.SCRAPPY, [Type.NORMAL, Type.FIGHT])])
Mawile = Pokemon("Mawile", 241, 206, 206, 146, 146, 136, [Type.STEEL, Type.FAIRY], [], [Ability.INTIMIDATE], [(246, 286, 146, 226, 136, Ability.HUGE_POWER, [Type.STEEL, Type.FAIRY])])
Pinsir = Pokemon("Pinsir", 271, 286, 236, 146, 176, 206, [Type.BUG], [], [Ability.MOXIE], [(346, 276, 166, 216, 246, Ability.AERILATE, [Type.BUG, Type.FLYING])])
Tyranitar = Pokemon("Tyranitar", 341, 304, 256, 226, 236, 158, [Type.ROCK, Type.DARK], [], [Ability.SAND_STREAM], [(364, 336, 226, 276, 178, Ability.SAND_STREAM, [Type.ROCK, Type.DARK])])
Azumarill = Pokemon("Azumarill", 341, 136, 196, 156, 196, 136, [Type.WATER, Type.FAIRY], [], [Ability.HUGE_POWER, Ability.THICK_FAT, Ability.SAP_SIPPER])
Greninja = Pokemon("Greninja", 285, 226, 170, 242, 178, 280, [Type.WATER, Type.DARK], [Water_Shuriken, Hydro_Pump, Surf, Dark_Pulse, Spikes], [Ability.PROTEAN, Ability.TORRENT, Ability.BATTLE_BOND], [(236, 186, 306, 216, 186, Ability.BATTLE_BOND, [Type.WATER, Type.DARK])])


class BasePokemonList(Enum):
    CHARIZARD = Charizard
    ALAKAZAM = Alakazam
    BLAZIKEN = Blaziken
    GARCHOMP = Garchomp
    MEDICHAM = Medicham
    SCIZOR = Scizor
    DIANCIE = Diancie
    SALAMENCE = Salamence
    SWAMPERT = Swampert
    LOPUNNY = Lopunny
    MAWILE = Mawile
    PINSIR = Pinsir
    TYRANITAR = Tyranitar
    AZUMARILL = Azumarill
    GRENINJA = Greninja


POKEMONS = [Charizard, Alakazam, Blaziken, Garchomp, Medicham, Scizor, Diancie, Salamence, Swampert, Lopunny, Mawile, Pinsir, Tyranitar, Azumarill, Greninja]
AVAILABLE_POKEMONS = {pokemon.name: pokemon for pokemon in POKEMONS}
