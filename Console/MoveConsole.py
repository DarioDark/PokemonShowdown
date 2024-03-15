from enum import Enum
from random import randint
from termcolor import colored

from AbilityConsole import Ability
from TypesConsole import Type
from CapacitySideEffectsConsole import SecondaryEffects, SecondaryEffectClass


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

    def __init__(self, name: str,
                 move_type: Type,
                 category: MoveCategory,
                 power,
                 base_accuracy: int,
                 max_pp: int,
                 secondary_effect: SecondaryEffectClass,
                 target: str,
                 priority: int = 0,
                 contact_move: bool = False,
                 bullet_move: bool = False,
                 sound_move: bool = False) -> None:
        self.name: str = name
        self.type: Type = move_type
        self.category: MoveCategory = category
        self.power: float = power
        self.base_accuracy: int = base_accuracy
        self.accuracy: float = base_accuracy
        self.max_pp: int = max_pp
        self.current_pp: int = max_pp
        self.secondary_effect: SecondaryEffectClass = secondary_effect
        self.target = target  # The target of the move, can be "enemy_pokemon", "self_pokemon", "enemy_player" or "self_player"
        self.priority: int = priority
        self.attributes: dict[str: bool] = {'contact': contact_move, 'bullet': bullet_move, 'sound': sound_move}

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

    def __getstate__(self) -> dict:
        return {
            'name': self.name,
            'type': self.type.name,
            'category': self.category.name,
            'power': self.power,
            'base_accuracy': self.base_accuracy,
            'accuracy': self.accuracy,
            'current_pp': self.current_pp,
            'max_pp': self.max_pp,
            'secondary_effect': self.secondary_effect.name.upper(),
            'target': self.target,
            'priority': self.priority,
            'contact_move': self.attributes['contact'],
            'bullet_move': self.attributes['bullet'],
            'sound_move': self.attributes['sound']
        }

    def __setstate__(self, state):
        self.name = state['name']
        self.type = Type[state['type']]
        self.category = MoveCategory[state['category']]
        self.power = state['power']
        self.base_accuracy = state['base_accuracy']
        self.accuracy = state['accuracy']
        self.current_pp = state['current_pp']
        self.max_pp = state['max_pp']
        self.secondary_effect = SecondaryEffects[state['secondary_effect']].value
        self.target = state['target']
        self.priority = state['priority']
        self.attributes = {'contact': state['contact_move'], 'bullet': state['bullet_move'], 'sound': state['sound_move']}

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


# Move declarations
FlameThrower = Move("Flamethrower", Type.FIRE, MoveCategory.SPECIAL, 90, 100, 15, SecondaryEffects.COMMON_BURN.value, "enemy_pokemon")
Thunderbolt = Move("Thunderbolt", Type.ELECTRIC, MoveCategory.SPECIAL, 90, 100, 15, SecondaryEffects.RARE_PARALYSIS.value, "enemy_pokemon")
Thunder = Move("Thunder", Type.ELECTRIC, MoveCategory.SPECIAL, 110, 70, 10, SecondaryEffects.COMMON_PARALYSIS.value, "enemy_pokemon")
Surf = Move("Surf", Type.WATER, MoveCategory.SPECIAL, 90, 100, 15, SecondaryEffects.NONE.value, "enemy_pokemon")
HydroPump = Move("Hydro Pump", Type.WATER, MoveCategory.SPECIAL, 110, 80, 5, SecondaryEffects.NONE.value, "enemy_pokemon")
IceBeam = Move("Ice Beam", Type.ICE, MoveCategory.SPECIAL, 90, 100, 10, SecondaryEffects.RARE_FREEZE.value, "enemy_pokemon")
Earthquake = Move("Earthquake", Type.GROUND, MoveCategory.PHYSICAL, 100, 100, 10, SecondaryEffects.NONE.value, "enemy_pokemon")
RockSlide = Move("Rock Slide", Type.ROCK, MoveCategory.PHYSICAL, 75, 90, 10, SecondaryEffects.NONE.value, "enemy_pokemon")
Psychic = Move("Psychic", Type.PSYCHIC, MoveCategory.SPECIAL, 90, 100, 15, SecondaryEffects.CONFUSION.value, "enemy_pokemon")
SkullBash = Move("Skull Bash", Type.NORMAL, MoveCategory.PHYSICAL, 130, 100, 5, SecondaryEffects.NONE.value, "enemy_pokemon")
AquaTail = Move("Aqua Tail", Type.WATER, MoveCategory.PHYSICAL, 90, 90, 10, SecondaryEffects.NONE.value, "enemy_pokemon")
QuickAttack = Move("Quick Attack", Type.NORMAL, MoveCategory.PHYSICAL, 40, 100, 30, SecondaryEffects.NONE.value, "enemy_pokemon")
CloseCombat = Move("Close Combat", Type.FIGHT, MoveCategory.PHYSICAL, 60, 100, 5, SecondaryEffects.NONE.value, "enemy_pokemon")

LeechSeed = Move("Leech Seed", Type.GRASS, MoveCategory.STATUS, 0, 90, 10, SecondaryEffects.LEECH_SEED.value, "enemy_pokemon")
StealthRock = Move("Stealth Rock", Type.ROCK, MoveCategory.STATUS, 0, 100, 10, SecondaryEffects.STEALTH_ROCK.value, "enemy_player")
LightScreen = Move("Light Screen", Type.PSYCHIC, MoveCategory.STATUS, 0, 100, 30, SecondaryEffects.LIGHT_SCREEN.value, "self_player")
Reflect = Move("Reflect", Type.PSYCHIC, MoveCategory.STATUS, 0, 100, 30, SecondaryEffects.REFLECT.value, "self_player")
Spikes = Move("Spikes", Type.GROUND, MoveCategory.STATUS, 0, 100, 20, SecondaryEffects.SPIKES.value, "enemy_player")
ToxicSpikes = Move("Toxic Spikes", Type.POISON, MoveCategory.STATUS, 0, 100, 20, SecondaryEffects.TOXIC_SPIKES.value, "enemy_player")

CONFUSION_ATTACK = Move("Confusion Attack", Type.NONE, MoveCategory.PHYSICAL, 40, 100, 100, SecondaryEffects.NONE.value, "self_pokemon")