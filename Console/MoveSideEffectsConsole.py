from enum import Enum

from AbilityConsole import Ability
from StatusConsole import PrimeStatus, SubStatus
from EnvironmentConsole import EnvironmentElements
from TypesConsole import Type


class SecondaryEffectClass:
    def __init__(self, name: str, probability: int, description: str, effect_function, turn_total: int = -1) -> None:
        self.name: str = name
        self.probability: int = max(probability, 0)
        self.description: str = description
        self.effect_function = effect_function
        self.turn_total: int = turn_total
        self.turn_counter: int = 0

    def __repr__(self) -> str:
        if self.name == "None":
            return f"{self.description}"
        return f"{self.description} with {self.probability}% chance"

    def apply(self, target, attacker) -> None:
        self.effect_function(target, attacker)

    def reset(self) -> None:
        self.turn_counter = 0

    # Effects functions
    @staticmethod
    def burn(target: 'Pokemon', attacker: 'Pokemon') -> None:
        if target.status != PrimeStatus.NORMAL or Type.FIRE in target.types:
            return
        target.status = PrimeStatus.BURN
        print(f"{target.name} is burned !")

    @staticmethod
    def poison(target: 'Pokemon', attacker: 'Pokemon') -> None:
        if target.status != PrimeStatus.NORMAL or Type.POISON in target.types:
            return
        target.status = PrimeStatus.POISON
        print(f"{target.name} is poisoned !")

    @staticmethod
    def severe_poison(target: 'Pokemon', attacker: 'Pokemon') -> None:
        if target.status != PrimeStatus.NORMAL or Type.POISON in target.types:
            return
        target.status = PrimeStatus.SEVERE_POISON
        target.nbr_turn_severe_poison = 0
        print(f"{target.name} is badly poisoned !")

    @staticmethod
    def paralysis(target: 'Pokemon', attacker: 'Pokemon') -> None:
        if target.status != PrimeStatus.NORMAL or Type.ELECTRIC in target.types or target.ability == Ability.LIMBER:
            return
        target.status = PrimeStatus.PARALYSIS
        print(f"{target.name} is paralyzed !")

    @staticmethod
    def sleep(target: 'Pokemon', attacker: 'Pokemon') -> None:
        if target.status != PrimeStatus.NORMAL:
            return
        target.status = PrimeStatus.SLEEP
        print(f"{target.name} fell asleep !")

    @staticmethod
    def freeze(target: 'Pokemon', attacker: 'Pokemon') -> None:
        if target.status != PrimeStatus.NORMAL or Type.ICE in target.types:
            return
        target.status = PrimeStatus.FREEZE
        print(f"{target.name} is frozen !")

    @staticmethod
    def confusion(target: 'Pokemon', attacker: 'Pokemon') -> None:
        target.sub_status.append(SubStatus.CONFUSION)
        print(f"{target.name} is confused !")

    @staticmethod
    def flinch(target: 'Pokemon', attacker: 'Pokemon') -> None:
        if target.ability == Ability.INNER_FOCUS:
            return
        target.sub_status.append(SubStatus.FLINCH)
        print(f"{target.name} flinched !")

    @staticmethod
    def rare_special_defense_down(target, attacker) -> None:
        target.lower_special_defense(1)
        print(f"{target.name}'s special defense was lowered !")

    @staticmethod
    def protect(target, attacker) -> None:
        target.sub_status.append(SubStatus.PROTECT)
        print(f"{target.name} protected itself !")

    # Entire capacities
    @staticmethod
    def stealth_rock(target, attacker) -> None:
        print("target env", target.environment.elements, target.environment)
        if EnvironmentElements.STEALTH_ROCK in target.environment.elements:
            print(f"But it failed ! Stealth Rock is already set up !")
        else:
            target.environment.add_element(EnvironmentElements.STEALTH_ROCK)
            print(f"Sharp rocks are floating around the enemy team !")

    @staticmethod
    def spikes(target, attacker) -> None:
        if target.environment.elements.count(EnvironmentElements.SPIKES) == 3:
            print(f"But it failed ! Spikes are already set up !")
        else:
            target.environment.add_element(EnvironmentElements.SPIKES)
            print(f"Sharp spikes spread around the enemy team !")

    @staticmethod
    def toxic_spikes(target, attacker) -> None:
        if target.environment.elements.count(EnvironmentElements.TOXIC_SPIKES) == 2:
            print(f"But it failed ! Toxic Spikes are already set up !")
        else:
            target.environment.add_element(EnvironmentElements.TOXIC_SPIKES)
            print(f"Toxic Spikes spread around the enemy team !")

    @staticmethod
    def light_screen(target, attacker) -> None:
        if EnvironmentElements.LIGHT_SCREEN in attacker.environment.elements:
            print(f"But it failed ! Light Screen is already set up !")
        else:
            attacker.environment.add_element(EnvironmentElements.LIGHT_SCREEN, 5)
            print(f"Light Screen was set up !")

    @staticmethod
    def reflect(target, attacker) -> None:
        if EnvironmentElements.REFLECT in attacker.environment.elements:
            print(f"But it failed ! Reflect is already set up !")
        else:
            attacker.environment.add_element(EnvironmentElements.REFLECT, 5)
            print(f"Reflect was set up !")

    @staticmethod
    def leech_seed(target, attacker) -> None:
        if Type.GRASS in target.types:
            print(f"But it failed ! This doesn't affect {target.name}...")
        else:
            if SubStatus.LEECH_SEED in target.sub_status:
                print(f"But it failed ! {target.name} is already infected !")
            else:
                target.sub_status.append(SubStatus.LEECH_SEED)
                print(f"{target.name} is infected !")

    @staticmethod
    def lower_spe_attack_by_2(target, attacker) -> None:
        attacker.lower_special_attack(2)

    @staticmethod
    def dragon_dance(target, attacker) -> None:
        attacker.raise_attack(1)
        attacker.raise_speed(1)

    @staticmethod
    def diamond_storm(target, attacker) -> None:
        attacker.raise_defense(1)

    @staticmethod
    def soft_boiled(target, attacker) -> None:
        hp_to_heal = attacker.max_hp // 2
        attacker.heal(hp_to_heal)

    @staticmethod
    def magma_storm(target, attacker) -> None:
        target.sub_status.append(SubStatus.MAGMA_STORM)

    @staticmethod
    def rare_special_attack_down(target, attacker) -> None:
        target.lower_special_attack(1)

    @staticmethod
    def rare_def_drop(target, attacker) -> None:
        target.lower_defense(1)


# Side effects declarations
none_effect = SecondaryEffectClass("None", 0,"No secondary effect.", None)
common_burn = SecondaryEffectClass("Common_burn", 30, "Burn the opposing Pokemon", SecondaryEffectClass.burn)
rare_burn = SecondaryEffectClass("Rare_burn", 10, "Burn the opposing Pokemon", SecondaryEffectClass.burn)
common_poison = SecondaryEffectClass("Common_poison", 30, "Poison the opposing Pokemon", SecondaryEffectClass.poison)
# severe_poison = SecondaryEffectClass("Severe Poison", 10, "Badly poison the opposing Pokemon.", severe_poison)
common_paralysis = SecondaryEffectClass("Common_paralysis", 30, "Paralyze the opposing Pokemon", SecondaryEffectClass.paralysis)
rare_paralysis = SecondaryEffectClass("Rare_paralysis", 10, "Paralyze the opposing Pokemon", SecondaryEffectClass.paralysis)
rare_freeze = SecondaryEffectClass("Rare_freeze", 10, "Freeze the opposing Pokemon", SecondaryEffectClass.freeze, 3)
confusion_effect = SecondaryEffectClass("Confusion", 10, "Confuse the opposing Pokemon", SecondaryEffectClass.confusion)
common_flinch = SecondaryEffectClass("Common_flinch", 30, "Flinch the opposing Pokemon", SecondaryEffectClass.flinch)
rare_flinch = SecondaryEffectClass("Rare_flinch", 10, "Flinch the opposing Pokemon", SecondaryEffectClass.flinch)
common_confusion = SecondaryEffectClass("Common_confusion", 30, "Confuse the opposing Pokemon", SecondaryEffectClass.confusion)
rare_def_drop = SecondaryEffectClass("Rare_def_drop", 20, "Lower the opposing Pokemon's defense", SecondaryEffectClass.rare_def_drop)
rare_special_attack_down = SecondaryEffectClass("Rare_special_defense_down", 10, "Lower the opposing Pokemon's special defense", SecondaryEffectClass.rare_special_attack_down)
rare_special_defense_down = SecondaryEffectClass("Rare_special_defense_down", 10, "Lower the opposing Pokemon's special defense", SecondaryEffectClass.rare_special_defense_down)
protect_effect = SecondaryEffectClass("Protect", 100, "Protect the user", SecondaryEffectClass.protect)
leech_seed_effect = SecondaryEffectClass("Leech_seed", 100, "The opposing Pokemon is seeded", SecondaryEffectClass.leech_seed)
stealth_rock_effect = SecondaryEffectClass("Stealth_rock", 100, "Set up Stealth Rock", SecondaryEffectClass.stealth_rock)
light_screen_effect = SecondaryEffectClass("Light_screen", 100, "Set up Light Screen", SecondaryEffectClass.light_screen)
reflect_effect = SecondaryEffectClass("Reflect", 100, "Set up Reflect", SecondaryEffectClass.reflect)
spikes_effect = SecondaryEffectClass("Spikes", 100, "Set up Spikes", SecondaryEffectClass.spikes)
toxic_spikes_effect = SecondaryEffectClass("Toxic_spikes", 100, "Set up Toxic Spikes", SecondaryEffectClass.toxic_spikes)
lower_spe_atk_by_2 = SecondaryEffectClass("Leaf_storm", 100, "Lower the user's special attack", SecondaryEffectClass.lower_spe_attack_by_2)
dragon_dance_effect = SecondaryEffectClass("Dragon_dance", 100, "The user's attack and speed are raised", SecondaryEffectClass.dragon_dance)
diamond_storm_effect = SecondaryEffectClass("Diamond_storm", 50, "Raise the user's defense", SecondaryEffectClass.diamond_storm)
soft_boiled_effect = SecondaryEffectClass("Soft_boiled", 100, "Heal the user", SecondaryEffectClass.soft_boiled)
magma_storm_effect = SecondaryEffectClass("Magma_storm", 75, "The opposing Pokemon is trapped", SecondaryEffectClass.magma_storm)


class SecondaryEffects(Enum):
    NONE = none_effect
    COMMON_BURN = common_burn
    RARE_BURN = rare_burn
    COMMON_POISON = common_poison
    COMMON_PARALYSIS = common_paralysis
    RARE_PARALYSIS = rare_paralysis
    RARE_FREEZE = rare_freeze
    CONFUSION = confusion_effect
    COMMON_FLINCH = common_flinch
    RARE_FLINCH = rare_flinch
    COMMON_CONFUSION = common_confusion

    RARE_SPECIAL_ATTACK_DOWN = rare_special_defense_down
    RARE_SPECIAL_DEFENSE_DOWN = rare_special_defense_down
    PROTECT = protect_effect

    STEALTH_ROCK = stealth_rock_effect
    SPIKES = spikes_effect
    TOXIC_SPIKES = toxic_spikes_effect
    LIGHT_SCREEN = light_screen_effect
    REFLECT = reflect_effect

    LEECH_SEED = leech_seed_effect
    LOWER_SPE_ATK_BY_2 = lower_spe_atk_by_2
    DRAGON_DANCE = dragon_dance_effect
    DIAMOND_STORM = diamond_storm_effect
    SOFT_BOILED = soft_boiled_effect
    MAGMA_STORM = magma_storm_effect
