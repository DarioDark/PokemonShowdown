from enum import Enum
from random import randint
from termcolor import colored

from AbilityConsole import Ability
from TypesConsole import Type
from MoveSideEffectsConsole import SecondaryEffects, SecondaryEffectClass


class MoveCategory(Enum):
    PHYSICAL = "Physical"
    SPECIAL = "Special"
    STATUS = "Status"


class Move:
    PP_COLORS = {100: "green",
                 60: "light_green",
                 45: "yellow",
                 20: "light_red",
                 0: "red"}

    def __init__(self, name: str = "",
                 move_type: Type = Type.NONE,
                 category: MoveCategory = MoveCategory.PHYSICAL,
                 power: int = 0,
                 base_accuracy: int = 0,
                 max_pp: int = 0,
                 secondary_effect: SecondaryEffects = SecondaryEffects.NONE,
                 target: str = "",
                 priority: int = 0,
                 contact_move: bool = False,
                 bullet_move: bool = False,
                 sound_move: bool = False,
                 nbr_hit: int = 1) -> None:
        self.name: str = name
        self.type: Type = move_type
        self.category: MoveCategory = category
        self.power: float = power
        self.base_accuracy: int = base_accuracy
        self.accuracy: float = base_accuracy
        self.max_pp: int = max_pp
        self.current_pp: int = max_pp
        self.secondary_effect: SecondaryEffects = secondary_effect
        self.target = target  # The target of the move, can be "pokemon", "player"
        self.priority: int = priority
        self.attributes: dict[str: bool] = {'contact': contact_move, 'bullet': bullet_move, 'sound': sound_move, 'nbr_hit': nbr_hit}

    def __repr__(self):
        if self.category == MoveCategory.STATUS:
            return (f"{colored(self.name, self.type.value.color)} ({self.type.value}) " + "PP: " + self.print_colored_pp() + " ~ "
                    f"{colored(self.category.value, 'cyan')} / {self.accuracy}% accuracy / {self.secondary_effect}")
        else:
            if self.category == MoveCategory.PHYSICAL:
                category_color = "red"
            else:
                category_color = "magenta"
        return (f"{colored(self.name, self.type.value.color)} ({self.type.value}) " + "PP: " + self.print_colored_pp() + " ~ "
                f"{colored(self.category.value, category_color)} / {self.power} power ~ {self.accuracy}% accuracy / {self.secondary_effect}")

    def __getstate__(self):
        state = self.__dict__.copy()
        state['type'] = self.type.name
        state['category'] = self.category.name
        state['secondary_effect'] = self.secondary_effect.name.upper()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

        self.type = Type[state['type']]
        self.category = MoveCategory[state['category']]
        self.secondary_effect = SecondaryEffects[state['secondary_effect']].value

    def get_current_pp_percentage(self) -> float:
        percentage = (self.current_pp / self.max_pp) * 100
        return round(percentage * 2) / 2

    def get_hit_number(self) -> int:
        if self.name == "Water Shuriken":
            return randint(2, 5)
        return self.attributes['nbr_hit']
    
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
    
    def apply_secondary_effect(self, target, attacker) -> None:
        """Applies the move's secondary effect.

        :param target: "self_player", "enemy_player", "self_pokemon", "enemy_pokemon"
        """
        if isinstance(self.secondary_effect, SecondaryEffectClass):
            self.secondary_effect.apply(target, attacker)


CONFUSION_ATTACK = Move("Confusion Attack", Type.NONE, MoveCategory.PHYSICAL, 40, 100, 100, SecondaryEffects.NONE.value, "self_pokemon")