from CapacityConsole import *
from OffensiveCapacityConsole import *


class ZMove(Capacity):
    MOVE_NAMES = {'NORMAL': 'Breakneck Blitz',
                  'FIRE': 'Inferno Overdrive',
                  'WATER': 'Hydro Vortex',
                  'ELECTRIC': 'Gigavolt Havoc',
                  'GRASS': 'Bloom Doom',
                  'ICE': 'Subzero Slammer',
                  'FIGHTING': 'All-Out Pummeling',
                  'POISON': 'Acid Downpour',
                  'GROUND': 'Tectonic Rage',
                  'FLYING': 'Supersonic Skystrike',
                  'PSYCHIC': 'Shattered Psyche',
                  'BUG': 'Savage Spin-Out',
                  'ROCK': 'Continental Crush',
                  'GHOST': 'Never-Ending Nightmare',
                  'DRAGON': 'Devastating Drake',
                  'DARK': 'Black Hole Eclipse',
                  'STEEL': 'Corkscrew Crash',
                  'FAIRY': 'Twinkle Tackle'}

    REAL_POWER = {55: 100,
                  65: 120,
                  75: 140,
                  85: 160,
                  95: 175,
                  100: 180,
                  110: 185,
                  125: 190,
                  130: 195,
                  140: 200}

    def __init__(self, move: 'OffensiveCapacity or StatusCapacity') -> None:
        # Get the move's attributes
        move_type: Type = move.type
        category: CapacityCategory = move.category
        if isinstance(move, OffensiveCapacity):
            power: int = move.power
        secondary_effect: SecondaryEffectClass = move.secondary_effect
        target = move.target

        # Set the Z-Move's attributes
        if category == CapacityCategory.PHYSICAL or category == CapacityCategory.SPECIAL:
            name = self.MOVE_NAMES[move_type.name]
        else:
            name = move_type.name + ' Z'
        super().__init__(name, move_type, 100, 1, secondary_effect)
        self.move = move
        self.category = category
        if isinstance(move, OffensiveCapacity):
            for power in self.REAL_POWER:
                print("ZMove: ", move.power, power, self.REAL_POWER[power])
                if power >= move.power:
                    self.power = self.REAL_POWER[power]
                    break
        self.target = target

    def __repr__(self) -> str:
        if self.category == CapacityCategory.PHYSICAL:
            category_color = "red"
        else:
            category_color = "magenta"
        if isinstance(self.move, OffensiveCapacity):
            return (f"{colored(self.name, self.type.value.color)} ({self.type.value}) " + "PP: " + self.get_colored_pp_number() + " ~ "
                    f"{colored(self.category.value, category_color)} / {self.power} power ~ {self.accuracy}% accuracy / {self.secondary_effect}")
        else:
            return (f"{colored(self.name, self.type.value.color)} ({self.type.value}) " + "PP: " + self.get_colored_pp_number() + " ~ "
                    f"{colored(self.category.value, category_color)} / {self.accuracy}% accuracy / {self.secondary_effect}")

