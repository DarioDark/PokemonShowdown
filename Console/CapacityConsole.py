from enum import Enum
from random import randint
from termcolor import colored

from AbilityConsole import Ability
from TypesConsole import Type
from CapacitySideEffectsConsole import SecondaryEffectClass


class CapacityCategory(Enum):
    PHYSICAL = "Physical"
    SPECIAL = "Special"
    STATUS = "Status"


class Move:
    PP_COLORS = {100: "green",
                 60: "light_green",
                 45: "yellow",
                 20: "light_red",
                 0: "red"}

    def __init__(self, name: str, move_type: Type, base_accuracy: int, max_pp: int, secondary_effect: SecondaryEffectClass) -> None:
        self.name: str = name
        self.type: Type = move_type
        self.base_accuracy: int = base_accuracy
        self.accuracy: float = base_accuracy
        self.max_pp: int = max_pp
        self.current_pp: int = max_pp
        self.secondary_effect: SecondaryEffectClass = secondary_effect
        self.attributes: dict[str: bool] = {'contact': False,
                                            'bullet': False,
                                            'sound': False}

    def get_current_pp_percentage(self) -> float:
        percentage = (self.current_pp / self.max_pp) * 100
        return round(percentage * 2) / 2
    
    def print_colored_pp(self) -> str:
        pp_percentage = self.get_current_pp_percentage()
        for key in sorted(Move.PP_COLORS.keys(), reverse=True):
            if pp_percentage >= key:
                color: str = Move.PP_COLORS[key]
                break
        return f"{colored(self.current_pp, color)}/{self.max_pp}"
    
    def print_greyed_out_pp(self) -> str:
        return colored(f"{self.current_pp}/{self.max_pp}", 'dark_grey')
    
    def is_secondary_effect_applied(self, attacker: 'Pokemon') -> bool:
        if self.secondary_effect:
            if attacker.ability == Ability.SERENE_GRACE:
                if randint(1, 100) <= self.secondary_effect.probability * 2:
                    return True
            elif randint(1, 100) <= self.secondary_effect.probability:
                return True
        return False
    
    def apply_secondary_effect(self, target) -> None:
        """Applies the move's secondary effect.

        :param target: "self_player", "enemy_player", "self_pokemon", "enemy_pokemon"
        """
        if isinstance(self.secondary_effect, SecondaryEffectClass):
            self.secondary_effect.apply(target)
