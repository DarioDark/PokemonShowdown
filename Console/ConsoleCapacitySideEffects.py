from enum import Enum
from random import randint
from ConsoleStatus import PrimeStatus, SubStatus
from ConsoleEnvironment import EnvironmentElements
from ConsoleTypes import Type


class SecondaryEffectClass:
    def __init__(self, name: str, probability: int, description: str, effect_function: 'function', turn_total: int = -1,
                 probability_vanishing: int = 0, ) -> None:
        self.name: str = name
        self.probability: int = max(probability, 0)  # percentage
        self.description: str = description
        self.effect_function = effect_function
        self.turn_total: int = turn_total
        self.turn_counter: int = 0
        self.probability_vanishing: int = probability_vanishing

    def __repr__(self) -> str:
        if self.name == "None":
            return f"{self.description}"
        return f"{self.description} with {self.probability}% chance"

    def apply(self, target: 'Pokemon') -> None:
        self.effect_function(target)

    def reset(self) -> None:
        self.turn_counter = 0

    def check_turns(self) -> bool:
        """Check if the effect is still active. Return False if the effect is still active, True otherwise."""
        if self.turn_total == -1 and self.probability_vanishing == 0:  # The effect is permanent
            return False
        elif self.turn_total == -1 and self.probability_vanishing != 0:  # The effect is permanent but can vanish each turn (ex: freeze)
            if randint(1, 100) <= self.probability_vanishing:
                return True
        elif self.turn_counter < self.turn_total:
            if randint(1, 100) <= self.probability_vanishing:
                self.turn_counter += 1
                return False
        return True


# Effects functions      
def burn(target: 'Pokemon') -> None:
    if target.status == PrimeStatus.NORMAL and not Type.FIRE in target.types:
        target.status = PrimeStatus.BURN
        target.attack = int(target.attack / 2)
        print(f"{target.name} is burned !")


def poison(target: 'Pokemon') -> None:
    if target.status == PrimeStatus.NORMAL and Type.POISON in target.types:
        target.status = PrimeStatus.POISON
        print(f"{target.name} is poisoned !")


def severe_poison(target: 'Pokemon') -> None:
    if target.status == PrimeStatus.NORMAL and Type.POISON in target.types:
        target.status = PrimeStatus.SEVERE_POISON
        target.nbr_turn_severe_poison = 0
        print(f"{target.name} is badly poisoned !")


def paralysis(target: 'Pokemon') -> None:
    if target.status == PrimeStatus.NORMAL and Type.ELECTRIC in target.types:
        target.status = PrimeStatus.PARALYSIS
        target.speed = int(target.speed / 2)
        print(f"{target.name} is paralyzed !")


def sleep(target: 'Pokemon') -> None:
    if target.status == PrimeStatus.NORMAL:
        target.status = PrimeStatus.SLEEP
        print(f"{target.name} fell asleep !")


def freeze(target: 'Pokemon') -> None:
    if target.status == PrimeStatus.NORMAL and Type.ICE in target.types:
        target.status = PrimeStatus.FREEZE
        print(f"{target.name} is frozen !")


def confusion(target: 'Pokemon') -> None:
    target.sub_status.append(SubStatus.CONFUSION)
    print(f"{target.name} is confused !")


def flinch(target: 'Pokemon') -> None:
    target.sub_status.append(SubStatus.FLINCH)
    print(f"{target.name} flinched !")


# Entire capacities
def leech_seed(target: 'Pokemon') -> None:
    if Type.PLANT in target.types:
        print(f"But it failed ! This doesn't affect {target.name}...")
    else:
        if not SubStatus.LEECH_SEED in target.sub_status:
            target.sub_status.append(SubStatus.LEECH_SEED)
            print(f"{target.name} is infected !")
        else:
            print(f"But it failed ! {target.name} is already infected !")


def stealth_rock(target: 'Player') -> None:
    if not EnvironmentElements.STEALTH_ROCK in target.environment.elements:
        target.environment.add_element(EnvironmentElements.STEALTH_ROCK)
        print(f"Sharp rocks are floating around the enemy team !")
    else:
        print(f"But it failed ! Stealth Rock is already set up !")


def light_screen(target: 'Player') -> None:
    if not EnvironmentElements.LIGHT_SCREEN in target.environment.elements:
        target.environment.add_element(EnvironmentElements.LIGHT_SCREEN)
        print(f"Light Screen was set up !")
    else:
        print(f"But it failed ! Light Screen is already set up !")


def reflect(target: 'Player') -> None:
    if not EnvironmentElements.REFLECT in target.environment.elements:
        target.environment.add_element(EnvironmentElements.REFLECT)
        print(f"Reflect was set up !")
    else:
        print(f"But it failed ! Reflect is already set up !")


# Side effects declarations
none_effect = SecondaryEffectClass("None", 0, "No secondary effect.", None)
common_burn = SecondaryEffectClass("Common_burn", 30, "Burn the opposing Pokemon", burn)
rare_burn = SecondaryEffectClass("Rare_burn", 10, "Burn the opposing Pokemon", burn)
common_poison = SecondaryEffectClass("Common_poison", 30, "Poison the opposing Pokemon", poison)
# severe_poison = SecondaryEffectClass("Severe Poison", 10, "Badly poison the opposing Pokemon.", severe_poison)
common_paralysis = SecondaryEffectClass("Common_paralysis", 30, "Paralyze the opposing Pokemon", paralysis)
rare_paralysis = SecondaryEffectClass("Rare_paralysis", 10, "Paralyze the opposing Pokemon", paralysis)
rare_freeze = SecondaryEffectClass("Rare_freeze", 10, "Freeze the opposing Pokemon", freeze, -1, 20)
confusion_effect = SecondaryEffectClass("Confusion", 10, "Confuse the opposing Pokemon", confusion)

leech_seed_effect = SecondaryEffectClass("Leech_seed", 100, "The opposing Pokemon is seeded", leech_seed)
stealth_rock_effect = SecondaryEffectClass("Stealth_rock", 100, "Set up Stealth Rock", stealth_rock)
light_screen_effect = SecondaryEffectClass("Light_screen", 100, "Set up Light Screen", light_screen, 5)
reflect_effect = SecondaryEffectClass("Reflect", 100, "Set up Reflect", reflect, 5)
spikes_effect = SecondaryEffectClass("Spikes", 100, "Set up Spikes", stealth_rock)


# Side effects enum
class SecondaryEffects(Enum):
    NONE = none_effect
    COMMON_BURN = common_burn
    RARE_BURN = rare_burn
    COMMON_POISON = common_poison
    COMMON_PARALYSIS = common_paralysis
    RARE_PARALYSIS = rare_paralysis
    CONFUSION = confusion_effect
    RARE_FREEZE = rare_freeze
    LEECH_SEED = leech_seed_effect
    STEALTH_ROCK = stealth_rock_effect
    SPIKES = spikes_effect
    LIGHT_SCREEN = light_screen_effect
    REFLECT = reflect_effect
