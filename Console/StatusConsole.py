from enum import Enum


class PrimeStatus(Enum):
    NORMAL = "Normal"
    BURN = "Burn"
    POISON = "Poison"
    SEVERE_POISON = "Severe Poison"
    PARALYSIS = "Paralysis"
    SLEEP = "Sleep"
    FREEZE = "Freeze"


class SubStatus(Enum):
    CONFUSION = "Confusion"
    LEECH_SEED = "Leech Seed"
    FLINCH = "Flinch"
    FLASH_FIRE = "Flash Fire"
    UNBURDEN = "Unburden"
    PROTECT = "Protect"
    MAGMA_STORM = "Magma Storm"
