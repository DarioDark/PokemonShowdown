from ConsoleCapacity import *
from ConsoleCapacitySideEffects import SecondaryEffects


class StatusCapacity(Capacity):
    def __init__(self, name: str, type: Type, accuracy:int, pp: int, secondary_effect: SecondaryEffectClass, target: str = "pokemon") -> None:
        super().__init__(name, type, accuracy, pp, secondary_effect)
        self.category = CapacityCategory.STATUS
        self.target = target # The target of the move, can be "pokemon", "player" or "self"
        
    def __repr__(self) -> str:
        pp_colors = {100: "green", 60: "light_green",  45: "yellow", 20: "light_red", 0: "red"}
        pp_percentage = self.get_current_pp_percentage()
        for key in sorted(pp_colors.keys(), reverse=True):
            if pp_percentage >= key:
                color = pp_colors[key]
                break
        return (f"{colored(self.name, self.type.value.color)} ({self.type.value}) " + "PP: " + self.get_colored_pp_number() + " ~ "
                f"{colored(self.category.value, 'cyan')} / {self.accuracy}% accuracy / {self.secondary_effect}")
    
    def __getstate__(self):
        return {
            'name': self.name,
            'type': self.type.name,
            'category': self.category.name,
            'accuracy': self.accuracy,
            'current_pp': self.current_pp,
            'max_pp': self.max_pp,
            'secondary_effect': self.secondary_effect.name.upper()
        }
        
    def __setstate__(self, state):
        self.name = state['name']
        self.type = Type[state['type']]
        self.category = CapacityCategory[state['category']]
        self.accuracy = state['accuracy']
        self.current_pp = state['current_pp']
        self.max_pp = state['max_pp']
        self.secondary_effect = SecondaryEffects[state['secondary_effect']]
           
           
LeechSeed = StatusCapacity("Leech Seed", Type.PLANT, 90, 10, SecondaryEffects.LEECH_SEED.value)
StealthRock = StatusCapacity("Stealth Rock", Type.ROCK, 100, 10, SecondaryEffects.STEALTH_ROCK.value, "player")
LightScreen = StatusCapacity("Light Screen", Type.PSYCHIC, 100, 30, SecondaryEffects.LIGHT_SCREEN.value, "self")
Reflect = StatusCapacity("Reflect", Type.PSYCHIC, 100, 30, SecondaryEffects.REFLECT.value, "self")