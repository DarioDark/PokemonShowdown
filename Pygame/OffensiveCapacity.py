from Capacity import *
from enum import Enum
from CapacitySideEffects import SecondaryEffects

class OffensiveCapacity(Capacity):
    def __init__(self, name: str, pokemon_type: Type, category: CapacityCategory, power: int, accuracy: int, pp: int, secondary_effect: SecondaryEffectClass) -> None:
        super().__init__(name, pokemon_type, accuracy, pp, secondary_effect)
        self.category = category
        self.power = power
        self.target = 'pokemon'
        
    def __repr__(self) -> str:
        if self.category == CapacityCategory.PHYSICAL:
            category_color = "red"
        else:
            category_color = "magenta"
        return (f"{colored(self.name, self.type.value.color)} ({self.type.value}) " + "PP: " + self.get_colored_pp_number() + " ~ "
                f"{colored(self.category.value, category_color)} / {self.power} power ~ {self.accuracy}% accuracy / {self.secondary_effect}")
        
    def __getstate__(self):
        return {
            'name': self.name,
            'type': self.type.name,
            'category': self.category.name,
            'power': self.power,
            'accuracy': self.accuracy,
            'current_pp': self.current_pp,
            'max_pp': self.max_pp,
            'secondary_effect': self.secondary_effect.name.upper()
        }
        
    def __setstate__(self, state):
        self.name = state['name']
        self.type = Type[state['type']]
        self.category = CapacityCategory[state['category']]
        self.power = int(state['power'])
        self.accuracy = state['accuracy']
        self.current_pp = state['current_pp']
        self.max_pp = state['max_pp']
        self.secondary_effect = SecondaryEffects[state['secondary_effect']].value


# Move declarations
Flamethrower = OffensiveCapacity("Flamethrower", Type.FIRE, CapacityCategory.SPECIAL, 90, 100, 15, SecondaryEffects.COMMON_BURN.value)
Thunderbolt = OffensiveCapacity("Thunderbolt", Type.ELECTRIC, CapacityCategory.SPECIAL, 90, 100, 15, SecondaryEffects.RARE_PARALYSIS.value)
Thunder = OffensiveCapacity("Thunder", Type.ELECTRIC, CapacityCategory.SPECIAL, 110, 70, 10, SecondaryEffects.COMMON_PARALYSIS.value)
Surf = OffensiveCapacity("Surf", Type.WATER, CapacityCategory.SPECIAL, 90, 100, 15, SecondaryEffects.NONE.value)
HydroPump = OffensiveCapacity("Hydro Pump", Type.WATER, CapacityCategory.SPECIAL, 110, 80, 5, SecondaryEffects.NONE.value) 
IceBeam = OffensiveCapacity("Ice Beam", Type.ICE, CapacityCategory.SPECIAL, 90, 100, 10, SecondaryEffects.RARE_FREEZE.value) 

Earthquake = OffensiveCapacity("Earthquake", Type.GROUND, CapacityCategory.PHYSICAL, 100, 100, 10, SecondaryEffects.NONE.value)
RockSlide = OffensiveCapacity("Rock Slide", Type.ROCK, CapacityCategory.PHYSICAL, 75, 90, 10, SecondaryEffects.NONE.value)

Psychic = OffensiveCapacity("Psychic", Type.PSYCHIC, CapacityCategory.SPECIAL, 90, 100, 15, SecondaryEffects.CONFUSION.value)

SkullBash = OffensiveCapacity("Skull Bash", Type.NORMAL, CapacityCategory.PHYSICAL, 130, 100, 5, SecondaryEffects.NONE.value) 

AquaTail = OffensiveCapacity("Aqua Tail", Type.WATER, CapacityCategory.PHYSICAL, 90, 90, 10, SecondaryEffects.NONE.value)
QuickAttack = OffensiveCapacity("Quick Attack", Type.NORMAL, CapacityCategory.PHYSICAL, 40, 100, 30, SecondaryEffects.NONE.value)