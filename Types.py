from enum import Enum
from termcolor import colored

class TypeClass:
    def __init__(self, name: str, color: str) -> None:
        self.name = name
        self.color = color
        self.default_color = color
        self.weaknesses: list[TypeClass] = []
        self.resistances: list[TypeClass] = []
        self.immunities: list[TypeClass] = []
      
    def __repr__(self) -> str:
        return colored(self.name, self.color)  
    
    def test(self):
        diction = {
            'name': self.name,
            'color': self.color,
            'default_color': self.default_color,
            'weaknesses': [type.name for type in self.weaknesses],
            'resistances': [type.name for type in self.resistances],
            'immunities': [type.name for type in self.immunities],
        }
        print("caca: ", [Type[type_name.upper()].value for type_name in diction['weaknesses']])
        print("type: ", Type[self.name.upper()].value.weaknesses)
       
    def __getstate__(self):
        return {
            'name': self.name,
            'color': self.color,
            'default_color': self.default_color,
            'weaknesses': [type.name for type in self.weaknesses],
            'resistances': [type.name for type in self.resistances],
            'immunities': [type.name for type in self.immunities],
        }

    def __setstate__(self, state):
        self.name = state['name']
        self.color = state['color']
        self.default_color = state['default_color']
        self.weaknesses = [Type[type_name.upper()].value for type_name in state['weaknesses']]
        self.resistances = [Type[type_name.upper()].value for type_name in state['resistances']]
        self.immunities = [Type[type_name.upper()].value for type_name in state['immunities']]
       
    def get_attributes(self) -> str:
        weaknesses_names = ', '.join([type.name for type in self.weaknesses])
        resistances_names = ', '.join([type.name for type in self.resistances])
        immunities_names = ', '.join([type.name for type in self.immunities])
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
Type.FIRE.value.weaknesses = [Type.WATER.value, Type.ROCK.value, Type.GROUND.value]
Type.FIRE.value.resistances = [Type.FIRE.value, Type.PLANT.value, Type.ICE.value, Type.BUG.value, Type.STEEL.value, Type.FAIRY.value]
Type.FIRE.value.immunities = []

# Water
Type.WATER.value.weaknesses = [Type.ELECTRIC.value, Type.PLANT.value]
Type.WATER.value.resistances = [Type.FIRE.value, Type.WATER.value, Type.ICE.value, Type.STEEL.value]
Type.WATER.value.immunities = []

# Plant
Type.PLANT.value.weaknesses = [Type.FIRE.value, Type.FLYING.value, Type.ICE.value, Type.POISON.value, Type.BUG.value]
Type.PLANT.value.resistances = [Type.WATER.value, Type.ELECTRIC.value, Type.PLANT.value, Type.FIGHT.value, Type.FAIRY.value]
Type.PLANT.value.immunities = []

# Electric
Type.ELECTRIC.value.weaknesses = [Type.GROUND.value]
Type.ELECTRIC.value.resistances = [Type.ELECTRIC.value, Type.FLYING.value, Type.STEEL.value]
Type.ELECTRIC.value.immunities = []

# Psychic
Type.PSYCHIC.value.weaknesses = [Type.DARK.value, Type.BUG.value, Type.GHOST.value]
Type.PSYCHIC.value.resistances = [Type.FIGHT.value, Type.PSYCHIC.value]
Type.PSYCHIC.value.immunities = []

# Fight
Type.FIGHT.value.weaknesses = [Type.FLYING.value, Type.PSYCHIC.value, Type.FAIRY.value]
Type.FIGHT.value.resistances = [Type.BUG.value, Type.ROCK.value, Type.DARK.value]
Type.FIGHT.value.immunities = []

# Dark
Type.DARK.value.weaknesses = [Type.FIGHT.value, Type.BUG.value, Type.FAIRY.value]
Type.DARK.value.resistances = [Type.GHOST.value, Type.DARK.value]
Type.DARK.value.immunities = [Type.PSYCHIC.value]

# Dragon
Type.DRAGON.value.weaknesses = [Type.ICE.value, Type.DRAGON.value, Type.FAIRY.value]
Type.DRAGON.value.resistances = [Type.FIRE.value, Type.WATER.value, Type.ELECTRIC.value, Type.PLANT.value]
Type.DRAGON.value.immunities = []

# Fairy
Type.FAIRY.value.weaknesses = [Type.POISON.value, Type.STEEL.value]
Type.FAIRY.value.resistances = [Type.FIGHT.value, Type.BUG.value, Type.DARK.value]
Type.FAIRY.value.immunities = [Type.DRAGON.value]

# Steel
Type.STEEL.value.weaknesses = [Type.FIRE.value, Type.FIGHT.value, Type.GROUND.value]
Type.STEEL.value.resistances = [Type.NORMAL.value, Type.FLYING.value, Type.ROCK.value, Type.BUG.value, Type.STEEL.value, Type.PLANT.value, Type.PSYCHIC.value, Type.ICE.value, Type.DRAGON.value, Type.FAIRY.value]
Type.STEEL.value.immunities = [Type.POISON.value]

# Ground
Type.GROUND.value.weaknesses = [Type.WATER.value, Type.PLANT.value, Type.ICE.value]
Type.GROUND.value.resistances = [Type.POISON.value, Type.ROCK.value]
Type.GROUND.value.immunities = [Type.ELECTRIC.value]

# Flying
Type.FLYING.value.weaknesses = [Type.ELECTRIC.value, Type.ICE.value, Type.ROCK.value]
Type.FLYING.value.resistances = [Type.FIGHT.value, Type.BUG.value, Type.PLANT.value]
Type.FLYING.value.immunities = [Type.GROUND.value]

# Normal
Type.NORMAL.value.weaknesses = []
Type.NORMAL.value.resistances = [Type.GHOST.value]
Type.NORMAL.value.immunities = []

# Poison
Type.POISON.value.weaknesses = [Type.GROUND.value, Type.PSYCHIC.value]
Type.POISON.value.resistances = [Type.FIGHT.value, Type.POISON.value, Type.PLANT.value, Type.FAIRY.value]
Type.POISON.value.immunities = []

# Bug
Type.BUG.value.weaknesses = [Type.FIRE.value, Type.FLYING.value, Type.ROCK.value]
Type.BUG.value.resistances = [Type.FIGHT.value, Type.GROUND.value, Type.PLANT.value]
Type.BUG.value.immunities = []

# Rock
Type.ROCK.value.weaknesses = [Type.WATER.value, Type.PLANT.value, Type.FIGHT.value, Type.GROUND.value, Type.STEEL.value]
Type.ROCK.value.resistances = [Type.NORMAL.value, Type.FLYING.value, Type.POISON.value, Type.FIRE.value]
Type.ROCK.value.immunities = []

# Ghost
Type.GHOST.value.weaknesses = [Type.GHOST.value, Type.DARK.value]
Type.GHOST.value.resistances = [Type.POISON.value, Type.BUG.value]
Type.GHOST.value.immunities = [Type.NORMAL.value, Type.FIGHT.value]

# Ice
Type.ICE.value.weaknesses = [Type.FIRE.value, Type.FIGHT.value, Type.ROCK.value, Type.STEEL.value]
Type.ICE.value.resistances = [Type.ICE.value]
Type.ICE.value.immunities = []

# None (if the Pokemon has only one type, the second type is None), this type has no weaknesses, resistances or immunities, its serves as a placeholder
Type.NONE.value.weaknesses = []
Type.NONE.value.resistances = []
Type.NONE.value.immunities = []

