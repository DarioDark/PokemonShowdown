from CapacityConsole import *
from CapacitySideEffectsConsole import SecondaryEffects


class StatusCapacity(Capacity):
    def __init__(self, name: str = None, type: Type = None, accuracy:int = None, pp: int = None, secondary_effect: SecondaryEffectClass = None, target: str = None):
        super().__init__(name, type, accuracy, pp, secondary_effect)
        self.category = CapacityCategory.STATUS
        self.target = target  # The target of the move, can be "enemy_pokemon", "self_pokemon", "enemy_player" or "self_player"
        
    def __repr__(self) -> str:
        """Return a string representation of the capacity.

        :return: The string representation of the capacity
        """
        pp_colors = {100: "green", 60: "light_green",  45: "yellow", 20: "light_red", 0: "red"}
        pp_percentage = self.get_current_pp_percentage()
        for key in sorted(pp_colors.keys(), reverse=True):
            if pp_percentage >= key:
                color = pp_colors[key]
                break
        return (f"{colored(self.name, self.type.value.color)} ({self.type.value}) " + "PP: " + self.get_colored_pp_number() + " ~ "
                f"{colored(self.category.value, 'cyan')} / {self.accuracy}% accuracy / {self.secondary_effect}")
    
    def __getstate__(self) -> dict:
        return {
            'name': self.name,
            'type': self.type.name,
            'category': self.category.name,
            'accuracy': self.accuracy,
            'current_pp': self.current_pp,
            'max_pp': self.max_pp,
            'secondary_effect': self.secondary_effect.name.upper(),
            'target': self.target
        }
        
    def __setstate__(self, state) -> None:
        self.name = state['name']
        self.type = Type[state['type']]
        self.category = CapacityCategory[state['category']]
        self.accuracy = state['accuracy']
        self.current_pp = state['current_pp']
        self.max_pp = state['max_pp']
        self.secondary_effect = SecondaryEffects[state['secondary_effect']].value
        self.target = state['target']
           
           
LeechSeed = StatusCapacity("Leech Seed", Type.GRASS, 90, 10, SecondaryEffects.LEECH_SEED.value, "enemy_pokemon")
StealthRock = StatusCapacity("Stealth Rock", Type.ROCK, 100, 10, SecondaryEffects.STEALTH_ROCK.value, "enemy_player")
LightScreen = StatusCapacity("Light Screen", Type.PSYCHIC, 100, 30, SecondaryEffects.LIGHT_SCREEN.value, "self_player")
Reflect = StatusCapacity("Reflect", Type.PSYCHIC, 100, 30, SecondaryEffects.REFLECT.value, "enemy_self")
Spikes = StatusCapacity("Spikes", Type.GROUND, 100, 20, SecondaryEffects.SPIKES.value, "enemy_player")
