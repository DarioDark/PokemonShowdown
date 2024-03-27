from enum import Enum
from MoveConsole import *

FlameThrower = Move("Flamethrower", Type.FIRE, MoveCategory.SPECIAL, 90, 100, 15, SecondaryEffects.COMMON_BURN.value, "pokemon")
Earthquake = Move("Earthquake", Type.GROUND, MoveCategory.PHYSICAL, 100, 100, 10, SecondaryEffects.NONE, "pokemon")
Ice_Beam = Move("Ice Beam", Type.ICE, MoveCategory.SPECIAL, 90, 100, 10, SecondaryEffects.RARE_FREEZE.value, "pokemon")
Water_Shuriken = Move("Water Shuriken", Type.WATER, MoveCategory.SPECIAL, 15, 100, 20, SecondaryEffects.NONE, "pokemon", priority=1)
Hydro_Pump = Move("Hydro Pump", Type.WATER, MoveCategory.SPECIAL, 110, 80, 5, SecondaryEffects.NONE, "pokemon")
Thunderbolt = Move("Thunderbolt", Type.ELECTRIC, MoveCategory.SPECIAL, 90, 100, 15, SecondaryEffects.RARE_PARALYSIS.value, "pokemon")
Thunder = Move("Thunder", Type.ELECTRIC, MoveCategory.SPECIAL, 110, 70, 10, SecondaryEffects.COMMON_PARALYSIS.value, "pokemon")
Surf = Move("Surf", Type.WATER, MoveCategory.SPECIAL, 90, 100, 15, SecondaryEffects.NONE, "pokemon")
Psychic = Move("Psychic", Type.PSYCHIC, MoveCategory.SPECIAL, 90, 100, 10, SecondaryEffects.RARE_SPECIAL_DEFENSE_DOWN.value, "pokemon")
Psyshok = Move("Psyshok", Type.PSYCHIC, MoveCategory.SPECIAL, 80, 100, 10, SecondaryEffects.NONE, "pokemon")
Aqua_Jet = Move("Aqua Jet", Type.WATER, MoveCategory.PHYSICAL, 40, 100, 20, SecondaryEffects.NONE, "pokemon", priority=1)
Air_Slash = Move("Air Slash", Type.FLYING, MoveCategory.SPECIAL, 75, 95, 15, SecondaryEffects.RARE_FLINCH.value, "pokemon")
Heavy_Slam = Move("Heavy Slam", Type.STEEL, MoveCategory.PHYSICAL, 80, 100, 10, SecondaryEffects.NONE, "pokemon")
Bullet_Punch = Move("Bullet Punch", Type.STEEL, MoveCategory.PHYSICAL, 40, 100, 30, SecondaryEffects.NONE, "pokemon", priority=1)
Close_Combat = Move("Close Combat", Type.FIGHT, MoveCategory.PHYSICAL, 120, 100, 5, SecondaryEffects.NONE, "pokemon")
Protect = Move("Protect", Type.NORMAL, MoveCategory.STATUS, 0, 100, 10, SecondaryEffects.PROTECT.value, "pokemon", priority=4)
Light_Screen = Move("Light Screen", Type.PSYCHIC, MoveCategory.STATUS, 0, 100, 5, SecondaryEffects.LIGHT_SCREEN.value, "pokemon")
Reflect = Move("Reflect", Type.PSYCHIC, MoveCategory.STATUS, 0, 100, 5, SecondaryEffects.REFLECT.value, "pokemon")
Spikes = Move("Spikes", Type.GROUND, MoveCategory.STATUS, 0, 100, 20, SecondaryEffects.SPIKES.value, "player")
Stealth_Rock = Move("Stealth Rock", Type.ROCK, MoveCategory.STATUS, 0, 100, 20, SecondaryEffects.STEALTH_ROCK.value, "player")
Toxic_Spikes = Move("Toxic Spikes", Type.POISON, MoveCategory.STATUS, 0, 100, 20, SecondaryEffects.TOXIC_SPIKES.value, "player")
Leaf_Storm = Move("Leaf Storm", Type.GRASS, MoveCategory.SPECIAL, 130, 90, 5, SecondaryEffects.LOWER_SPE_ATK_BY_2.value, "pokemon")
Leech_Seed = Move("Leech Seed", Type.GRASS, MoveCategory.STATUS, 0, 90, 10, SecondaryEffects.LEECH_SEED.value, "pokemon")
Dragon_Claw = Move("Dragon Claw", Type.DRAGON, MoveCategory.PHYSICAL, 80, 100, 15, SecondaryEffects.NONE, "pokemon")
Dragon_Dance = Move("Dragon Dance", Type.DRAGON, MoveCategory.STATUS, 0, 100, 20, SecondaryEffects.DRAGON_DANCE.value, "pokemon")
Fire_Blast = Move("Fire Blast", Type.FIRE, MoveCategory.SPECIAL, 110, 85, 5, SecondaryEffects.RARE_BURN.value, "pokemon")
Moonblast = Move("Moonblast", Type.FAIRY, MoveCategory.SPECIAL, 95, 100, 15, SecondaryEffects.RARE_SPECIAL_ATTACK_DOWN.value, "pokemon", bullet_move=True)
Diamond_Storm = Move("Diamond Storm", Type.ROCK, MoveCategory.PHYSICAL, 100, 95, 5, SecondaryEffects.DIAMOND_STORM.value, "pokemon")
Earth_Power = Move("Earth Power", Type.GROUND, MoveCategory.SPECIAL, 90, 100, 10, SecondaryEffects.RARE_SPECIAL_DEFENSE_DOWN.value, "pokemon")
Soft_Boiled = Move("Soft Boiled", Type.NORMAL, MoveCategory.STATUS, 0, 100, 5, SecondaryEffects.SOFT_BOILED.value, "pokemon")
Dark_Pulse = Move("Dark Pulse", Type.DARK, MoveCategory.SPECIAL, 80, 100, 15, SecondaryEffects.RARE_FLINCH.value, "pokemon")
Magma_Storm = Move("Magma Storm", Type.FIRE, MoveCategory.SPECIAL, 100, 75, 5, SecondaryEffects.MAGMA_STORM.value, "pokemon")
Shadow_Ball = Move("Shadow Ball", Type.GHOST, MoveCategory.SPECIAL, 80, 100, 15, SecondaryEffects.RARE_SPECIAL_DEFENSE_DOWN.value, "pokemon", bullet_move=True)
Sludge_Bomb = Move("Sludge Bomb", Type.POISON, MoveCategory.SPECIAL, 90, 100, 10, SecondaryEffects.COMMON_POISON.value, "pokemon", bullet_move=True)
Sludge_Wave = Move("Sludge Wave", Type.POISON, MoveCategory.SPECIAL, 95, 100, 10, SecondaryEffects.COMMON_POISON.value, "pokemon")
Hurricane = Move("Hurricane", Type.FLYING, MoveCategory.SPECIAL, 110, 70, 10, SecondaryEffects.COMMON_CONFUSION.value, "pokemon")
Iron_Head = Move("Iron Head", Type.STEEL, MoveCategory.PHYSICAL, 80, 100, 15, SecondaryEffects.COMMON_FLINCH.value, "pokemon")
Energy_Ball = Move("Energy Ball", Type.GRASS, MoveCategory.SPECIAL, 90, 100, 10, SecondaryEffects.RARE_SPECIAL_DEFENSE_DOWN.value, "pokemon", bullet_move=True)
Boomburst = Move("Boomburst", Type.NORMAL, MoveCategory.SPECIAL, 140, 100, 10, SecondaryEffects.NONE, "pokemon", sound_move=True)
Poison_Jab = Move("Poison Jab", Type.POISON, MoveCategory.PHYSICAL, 80, 100, 20, SecondaryEffects.COMMON_POISON.value, "pokemon")
Liquidation = Move("Liquidation", Type.WATER, MoveCategory.PHYSICAL, 85, 100, 10, SecondaryEffects.NONE, "pokemon")
Leaf_Blade = Move("Leaf Blade", Type.GRASS, MoveCategory.PHYSICAL, 90, 100, 15, SecondaryEffects.NONE, "pokemon")
Draco_Meteor = Move("Draco Meteor", Type.DRAGON, MoveCategory.SPECIAL, 130, 90, 5, SecondaryEffects.LOWER_SPE_ATK_BY_2.value, "pokemon")
Dragon_Pulse = Move("Dragon Pulse", Type.DRAGON, MoveCategory.SPECIAL, 85, 100, 10, SecondaryEffects.NONE, "pokemon")
Acrobatics = Move("Acrobatics", Type.FLYING, MoveCategory.PHYSICAL, 55, 100, 15, SecondaryEffects.NONE, "pokemon")
Sacred_Sword = Move("Sacred Sword", Type.FIGHT, MoveCategory.PHYSICAL, 90, 100, 15, SecondaryEffects.NONE, "pokemon")
Aura_Sphere = Move("Aura Sphere", Type.FIGHT, MoveCategory.SPECIAL, 80, 100, 20, SecondaryEffects.NONE, "pokemon")
Scald = Move("Scald", Type.WATER, MoveCategory.SPECIAL, 80, 100, 15, SecondaryEffects.COMMON_BURN.value, "pokemon")

class BaseMoveList(Enum):
    FLAMETHROWER = FlameThrower
    EARTHQUAKE = Earthquake
    ICE_BEAM = Ice_Beam
    WATER_SHURIKEN = Water_Shuriken
    HYDRO_PUMP = Hydro_Pump
    THUNDERBOLT = Thunderbolt
    THUNDER = Thunder
    SURF = Surf
    PSYCHIC = Psychic
    PSYSHOK = Psyshok
    AQUA_JET = Aqua_Jet
    AIR_SLASH = Air_Slash
    HEAVY_SLAM = Heavy_Slam
    BULLET_PUNCH = Bullet_Punch
    CLOSE_COMBAT = Close_Combat
    PROTECT = Protect
    LIGHT_SCREEN = Light_Screen
    REFLECT = Reflect
    SPIKES = Spikes
    STEALTH_ROCK = Stealth_Rock
    TOXIC_SPIKES = Toxic_Spikes
    LEAF_STORM = Leaf_Storm
    LEECH_SEED = Leech_Seed
    DRAGON_CLAW = Dragon_Claw
    DRAGON_DANCE = Dragon_Dance
    FIRE_BLAST = Fire_Blast
    MOONBLAST = Moonblast
    DIAMOND_STORM = Diamond_Storm
    EARTH_POWER = Earth_Power
    SOFT_BOILED = Soft_Boiled
    DARK_PULSE = Dark_Pulse
    MAGMA_STORM = Magma_Storm
    SHADOW_BALL = Shadow_Ball
    SLUDGE_BOMB = Sludge_Bomb
    SLUDGE_WAVE = Sludge_Wave
    HURRICANE = Hurricane
    IRON_HEAD = Iron_Head
    ENERGY_BALL = Energy_Ball
    BOOMBURST = Boomburst
    POISON_JAB = Poison_Jab
    LIQUIDATION = Liquidation
    LEAF_BLADE = Leaf_Blade
    DRACO_METEOR = Draco_Meteor
    DRAGON_PULSE = Dragon_Pulse
    ACROBATICS = Acrobatics
    SACRED_SWORD = Sacred_Sword
    AURA_SPHERE = Aura_Sphere
    SCALD = Scald