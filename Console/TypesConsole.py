from enum import Enum
from termcolor import colored


class TypeClass:
    def __init__(self, name: str, color: str):
        self.name: str = name
        self.color: str = color
        self.default_color: str = color
        self.weaknesses: list[Type] = []
        self.resistances: list[Type] = []
        self.immunities: list[Type] = []
      
    def __repr__(self) -> str:
        return colored(self.name, self.color)  

    def __getstate__(self):
        return {
            'name': self.name,
            'color': self.color,
            'default_color': self.default_color,
            'weaknesses': self.weaknesses,
            'resistances': self.resistances,
            'immunities': self.immunities,
        }

    def __setstate__(self, state):
        self.name = state['name']
        self.color = state['color']
        self.default_color = state['default_color']
        self.weaknesses = state['weaknesses']
        self.resistances = state['resistances']
        self.immunities = state['immunities']
       
    def get_attributes(self) -> str:
        weaknesses_names = ', '.join([pokemon_type.value.name for pokemon_type in self.weaknesses])
        resistances_names = ', '.join([pokemon_type.value.name for pokemon_type in self.resistances])
        immunities_names = ', '.join([pokemon_type.value.name for pokemon_type in self.immunities])
        return (f"{colored(self.name, attrs=['bold'])} :" +
                f"\n• {colored('Weaknesses:'.ljust(12), 'red')} {weaknesses_names}" + 
                f"\n• {colored('Resistances:'.ljust(12), 'cyan')} {resistances_names}" +
                f"\n• {colored('Immunities:'.ljust(12), 'light_yellow')} {immunities_names}")


Fire = TypeClass("Fire", "red")
Water = TypeClass("Water", "blue")
Plant = TypeClass("Plant", "green")
Electric = TypeClass("Electric", "yellow")
Psychic = TypeClass("Psychic", "light_magenta")
Fight = TypeClass("Fight", "light_red")
Dark = TypeClass("Dark", "grey")
Dragon = TypeClass("Dragon", "blue")
Fairy = TypeClass("Fairy", "light_magenta")
Steel = TypeClass("Steel", "dark_grey")
Ground = TypeClass("Ground", "yellow")
Flying = TypeClass("Flying", "light_blue")
Normal = TypeClass("Normal", "white")
Poison = TypeClass("Poison", "magenta")
Bug = TypeClass("Bug", "light_green")
Rock = TypeClass("Rock", "yellow")
Ghost = TypeClass("Ghost", "blue")
Ice = TypeClass("Ice", "light_cyan")
NoneType = TypeClass("None", "white")


class Type(Enum):
    FIRE = Fire
    WATER = Water
    PLANT = Plant
    ELECTRIC = Electric
    PSYCHIC = Psychic
    FIGHT = Fight
    DARK = Dark
    DRAGON = Dragon
    FAIRY = Fairy
    STEEL = Steel
    GROUND = Ground
    FLYING = Flying
    NORMAL = Normal
    POISON = Poison
    BUG = Bug
    ROCK = Rock
    GHOST = Ghost
    ICE = Ice
    NONE = NoneType


# Fire
Type.FIRE.value.weaknesses = [Type.WATER, Type.ROCK, Type.GROUND]
Type.FIRE.value.resistances = [Type.FIRE, Type.PLANT, Type.ICE, Type.BUG, Type.STEEL, Type.FAIRY]
Type.FIRE.value.immunities = []

# Water
Type.WATER.value.weaknesses = [Type.ELECTRIC, Type.PLANT]
Type.WATER.value.resistances = [Type.FIRE, Type.WATER, Type.ICE, Type.STEEL]
Type.WATER.value.immunities = []

# Plant
Type.PLANT.value.weaknesses = [Type.FIRE, Type.FLYING, Type.ICE, Type.POISON, Type.BUG]
Type.PLANT.value.resistances = [Type.WATER, Type.ELECTRIC, Type.PLANT, Type.FIGHT, Type.FAIRY]
Type.PLANT.value.immunities = []

# Electric
Type.ELECTRIC.value.weaknesses = [Type.GROUND]
Type.ELECTRIC.value.resistances = [Type.ELECTRIC, Type.FLYING, Type.STEEL]
Type.ELECTRIC.value.immunities = []

# Psychic
Type.PSYCHIC.value.weaknesses = [Type.DARK, Type.BUG, Type.GHOST]
Type.PSYCHIC.value.resistances = [Type.FIGHT, Type.PSYCHIC]
Type.PSYCHIC.value.immunities = []

# Fight
Type.FIGHT.value.weaknesses = [Type.FLYING, Type.PSYCHIC, Type.FAIRY]
Type.FIGHT.value.resistances = [Type.BUG, Type.ROCK, Type.DARK]
Type.FIGHT.value.immunities = []

# Dark
Type.DARK.value.weaknesses = [Type.FIGHT, Type.BUG, Type.FAIRY]
Type.DARK.value.resistances = [Type.GHOST, Type.DARK]
Type.DARK.value.immunities = [Type.PSYCHIC]

# Dragon
Type.DRAGON.value.weaknesses = [Type.ICE, Type.DRAGON, Type.FAIRY]
Type.DRAGON.value.resistances = [Type.FIRE, Type.WATER, Type.ELECTRIC, Type.PLANT]
Type.DRAGON.value.immunities = []

# Fairy
Type.FAIRY.value.weaknesses = [Type.POISON, Type.STEEL]
Type.FAIRY.value.resistances = [Type.FIGHT, Type.BUG, Type.DARK]
Type.FAIRY.value.immunities = [Type.DRAGON]

# Steel
Type.STEEL.value.weaknesses = [Type.FIRE, Type.FIGHT, Type.GROUND]
Type.STEEL.value.resistances = [Type.NORMAL, Type.FLYING, Type.ROCK, Type.BUG, Type.STEEL, Type.PLANT, Type.PSYCHIC, Type.ICE, Type.DRAGON, Type.FAIRY]
Type.STEEL.value.immunities = [Type.POISON]

# Ground
Type.GROUND.value.weaknesses = [Type.WATER, Type.PLANT, Type.ICE]
Type.GROUND.value.resistances = [Type.POISON, Type.ROCK]
Type.GROUND.value.immunities = [Type.ELECTRIC]

# Flying
Type.FLYING.value.weaknesses = [Type.ELECTRIC, Type.ICE, Type.ROCK]
Type.FLYING.value.resistances = [Type.FIGHT, Type.BUG, Type.PLANT]
Type.FLYING.value.immunities = [Type.GROUND]

# Normal
Type.NORMAL.value.weaknesses = []
Type.NORMAL.value.resistances = [Type.GHOST]
Type.NORMAL.value.immunities = []

# Poison
Type.POISON.value.weaknesses = [Type.GROUND, Type.PSYCHIC]
Type.POISON.value.resistances = [Type.FIGHT, Type.POISON, Type.PLANT, Type.FAIRY]
Type.POISON.value.immunities = []

# Bug
Type.BUG.value.weaknesses = [Type.FIRE, Type.FLYING, Type.ROCK]
Type.BUG.value.resistances = [Type.FIGHT, Type.GROUND, Type.PLANT]
Type.BUG.value.immunities = []

# Rock
Type.ROCK.value.weaknesses = [Type.WATER, Type.PLANT, Type.FIGHT, Type.GROUND, Type.STEEL]
Type.ROCK.value.resistances = [Type.NORMAL, Type.FLYING, Type.POISON, Type.FIRE]
Type.ROCK.value.immunities = []

# Ghost
Type.GHOST.value.weaknesses = [Type.GHOST, Type.DARK]
Type.GHOST.value.resistances = [Type.POISON, Type.BUG]
Type.GHOST.value.immunities = [Type.NORMAL, Type.FIGHT]

# Ice
Type.ICE.value.weaknesses = [Type.FIRE, Type.FIGHT, Type.ROCK, Type.STEEL]
Type.ICE.value.resistances = [Type.ICE]
Type.ICE.value.immunities = []

# None (if the Pokemon has only one type, the second type is None), this type has no weaknesses, resistances or immunities, its serves as a placeholder
Type.NONE.weaknesses = []
Type.NONE.resistances = []
Type.NONE.immunities = []
