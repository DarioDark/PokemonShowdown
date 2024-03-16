from PokemonConsole import *


# Create some pokemons
CHARIZARD = Pokemon("Charizard", 297, 204, 192, 254, 206, 236, [Type.FIRE, Type.FLYING], [FlameThrower, Earthquake, IceBeam, ToxicSpikes], Ability.NONE, Item.CHARIZARDITE_X,[(296, 258, 296, 206, 236, Ability.TOUGH_CLAWS, [Type.FIRE, Type.DRAGON]), (244, 192, 354, 266, 236, Ability.DROUGHT, [Type.FIRE, Type.FLYING])])
ALAKAZAM = Pokemon("Alakazam", 251, 136, 126, 306, 226, 276, [Type.PSYCHIC], [], Ability.MAGIC_GUARD, Item.NONE, [(136, 166, 386, 246, 336, Ability.TRACE, [Type.PSYCHIC])])
BLAZIKEN = Pokemon("Blaziken", 301, 276, 176, 256, 176, 196, [Type.FIRE, Type.FIGHT], [], Ability.SPEED_BOOST, Item.NONE, [(356, 196, 296, 196, 236, Ability.SPEED_BOOST, [Type.FIRE, Type.FIGHT])])
GARCHOMP = Pokemon("Garchomp", 357, 296, 226, 196, 206, 240, [Type.DRAGON, Type.GROUND], [], Ability.ROUGH_SKIN, Item.NONE, [(376, 266, 276, 226, 220, Ability.SAND_FORCE, [Type.DRAGON, Type.GROUND])])
CHARMINA = Pokemon("Charmina", 261, 156, 186, 156, 186, 196, [Type.FIGHT, Type.PSYCHIC], [], Ability.PURE_POWER, Item.NONE, [(236, 206, 196, 206, 236, Ability.PURE_POWER, [Type.FIGHT, Type.PSYCHIC])])
SCIZOR = Pokemon("Scizor", 281, 296, 236, 146, 196, 166, [Type.BUG, Type.STEEL], [], Ability.TECHNICIAN, Item.NONE, [(336, 316, 166, 236, 186, Ability.TECHNICIAN, [Type.BUG, Type.STEEL])])
BEEDRILL = Pokemon("Beedrill", 271, 216, 116, 126, 196, 186, [Type.BUG, Type.POISON], [], Ability.SWARM, Item.NONE, [(336, 116, 66, 196, 326, Ability.ADAPTABILITY, [Type.BUG, Type.POISON])])
DIANCIE = Pokemon("Diancie", 241, 236, 336, 236, 336, 136, [Type.ROCK, Type.FAIRY], [], Ability.CLEAR_BODY, Item.NONE, [(356, 256, 356, 256, 256, Ability.MAGIC_BOUNCE, [Type.ROCK, Type.FAIRY])])
SALAMENCE = Pokemon("Salamence", 331, 306, 196, 256, 196, 236, [Type.DRAGON, Type.FLYING], [], Ability.INTIMIDATE, Item.NONE, [(326, 296, 276, 216, 276, Ability.AERILATE, [Type.DRAGON, Type.FLYING])])
MANECTRIC = Pokemon("Manectric", 281, 186, 156, 246, 156, 246, [Type.ELECTRIC], [], Ability.LIGHTNING_ROD, Item.NONE, [(186, 196, 306, 196, 306, Ability.INTIMIDATE, [Type.ELECTRIC])])
SWAMPERT = Pokemon("Swampert", 341, 256, 216, 206, 216, 156, [Type.WATER, Type.GROUND], [], Ability.TORRENT, Item.NONE, [(336, 256, 226, 256, 176, Ability.SWIFT_SWIM, [Type.WATER, Type.GROUND])])
LOPUNNY = Pokemon("Lopunny", 271, 188, 204, 144, 228, 246, [Type.NORMAL, Type.FIGHT], [], Ability.LIMBER, Item.NONE, [(308, 224, 144, 228, 306, Ability.SCRAPPY, [Type.NORMAL, Type.FIGHT])])
METAGROSS = Pokemon("Metagross", 301, 306, 296, 226, 216, 176, [Type.STEEL, Type.PSYCHIC], [], Ability.CLEAR_BODY, Item.NONE, [(326, 336, 246, 256, 256, Ability.TOUGH_CLAWS, [Type.STEEL, Type.PSYCHIC])])
MAWILE = Pokemon("Mawile", 241, 206, 206, 146, 146, 136, [Type.STEEL, Type.FAIRY], [], Ability.INTIMIDATE, Item.NONE, [(246, 286, 146, 226, 136, Ability.HUGE_POWER, [Type.STEEL, Type.FAIRY])])
PIDGEOT = Pokemon("Pidgeot", 241, 196, 186, 176, 176, 238, [Type.NORMAL, Type.FLYING], [], Ability.BIG_PECKS, Item.NONE, [(196, 196, 306, 196, 278, Ability.NO_GUARD, [Type.NORMAL, Type.FLYING])])
PINSIR = Pokemon("Pinsir", 271, 286, 236, 146, 176, 206, [Type.BUG], [], Ability.MOXIE, Item.NONE, [(346, 276, 166, 216, 246, Ability.AERILATE, [Type.BUG, Type.FLYING])])
TYRANITAR = Pokemon("Tyranitar", 341, 304, 256, 226, 236, 158, [Type.ROCK, Type.DARK], [], Ability.SAND_STREAM, Item.NONE, [(364, 336, 226, 276, 178, Ability.SAND_STREAM, [Type.ROCK, Type.DARK])])
VENUSAUR = Pokemon("Venusaur", 301, 200, 202, 236, 236, 196, [Type.GRASS, Type.POISON], [QuickAttack, Thunder, Surf, SkullBash], Ability.NONE, Item.NONE, [(236, 282, 280, 276, 196, Ability.THICK_FAT, [Type.GRASS, Type.POISON])])


Blastoise = Pokemon("Blastoise", 79, 83, 100, 85, 105, 78, [Type.WATER], [HydroPump, IceBeam, Earthquake, AquaTail], Ability.NONE, Item.WATERIUM_Z)
Mew = Pokemon("Mew", 100, 100, 100, 100, 100, 100, [Type.PSYCHIC], [QuickAttack, CloseCombat, Surf, StealthRock], Ability.SCRAPPY, Item.ROCKIUM_Z)
Landorus_Therian = Pokemon("Landorus-Therian", 89, 145, 90, 105, 80, 91, [Type.GROUND, Type.FLYING], [QuickAttack, Thunder, Surf, SkullBash], Ability.NONE, Item.NONE)
Ferrothorn = Pokemon("Ferrothorn", 74, 94, 131, 54, 116, 20, [Type.GRASS, Type.STEEL], [StealthRock, QuickAttack, CloseCombat, LeechSeed], Ability.IRON_BARBS, Item.NONE)
Greninja = Pokemon("Greninja", 72, 95, 67, 103, 71, 122, [Type.WATER, Type.DARK], [QuickAttack, Thunder, Surf, SkullBash], Ability.NONE, Item.NONE)
Magnezone = Pokemon("Magnezone", 70, 70, 115, 130, 90, 60, [Type.ELECTRIC, Type.STEEL], [QuickAttack, Thunder, Surf, SkullBash], Ability.MAGNET_PULL, Item.NONE)
Blacephalon = Pokemon("Blacephalon", 53, 127, 53, 151, 79, 107, [Type.FIRE, Type.GHOST], [QuickAttack, Thunder, Surf, SkullBash], Ability.NONE, Item.NONE)

AVAILABLE_POKEMONS = [CHARIZARD, ALAKAZAM, BLAZIKEN, GARCHOMP, CHARMINA, SCIZOR, BEEDRILL, DIANCIE, SALAMENCE, MANECTRIC, SWAMPERT, LOPUNNY, METAGROSS, MAWILE, PIDGEOT, PINSIR, TYRANITAR, VENUSAUR, Blastoise, Mew, Landorus_Therian, Ferrothorn, Greninja, Magnezone, Blacephalon]