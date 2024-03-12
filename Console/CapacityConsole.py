from enum import Enum
from random import randint
from termcolor import colored

from TypesConsole import Type
from CapacitySideEffectsConsole import SecondaryEffectClass


class Capacity:
    def __init__(self, name: str, type: Type, accuracy: float, pp: int, secondary_effect: SecondaryEffectClass) -> None:
        self.name: str = name
        self.type: Type = type
        self.base_accuracy: float = accuracy
        self.accuracy: float = accuracy
        self.current_pp: int = pp
        self.max_pp: int = pp
        self.secondary_effect: SecondaryEffectClass = secondary_effect               

    def get_current_pp_percentage(self) -> float:
        percentage = (self.current_pp / self.max_pp) * 100
        return round(percentage * 2) / 2
    
    def get_colored_pp_number(self) -> str:
        pp_colors = {100: "green", 60: "light_green",  45: "yellow", 20: "light_red", 0: "red"}
        pp_percentage = self.get_current_pp_percentage()
        for key in sorted(pp_colors.keys(), reverse=True):
            if pp_percentage >= key:
                color: str = pp_colors[key]
                break
        return f"{colored(self.current_pp, color)}/{self.max_pp}"
    
    def get_grey_pp_number(self) -> str:
        return colored(f"{self.current_pp}/{self.max_pp}", 'dark_grey')
    
    def is_secondary_effect_applied(self) -> bool:
        if self.secondary_effect:
            if randint(1, 100) <= self.secondary_effect.probability:
                return True
        return False
    
    def apply_secondary_effect(self, target) -> None:  # The target can be the opposing pokemon, the opposing player or the player itself
        if isinstance(self.secondary_effect, SecondaryEffectClass):
            self.secondary_effect.apply(target)

            
class CapacityCategory(Enum):
    PHYSICAL = "Physical"
    SPECIAL = "Special"
    STATUS = "Status"
