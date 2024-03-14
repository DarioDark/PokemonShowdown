from MoveConsole import *


class ZMove(Move):
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

    TRANSFORMED_POWER = {55: 100,
                         65: 120,
                         75: 140,
                         85: 160,
                         95: 175,
                         100: 180,
                         110: 185,
                         125: 190,
                         130: 195,
                         140: 200}

    def __init__(self, move: 'OffensiveMove or StatusMove') -> None:
        # Transforms the move into a Z-Move
        if move.category == MoveCategory.PHYSICAL or move.category == MoveCategory.SPECIAL:
            name = self.MOVE_NAMES[move.type.name]
        else:
            name = move.name + ' Z'
        super().__init__(name, move.type, move.category, move.power, 100, 1, move.secondary_effect, move.target)

        # Get the Z-Move's attributes
        self.category = move.category
        self.target = move.target
        if self.category == MoveCategory.STATUS:
            for power in self.TRANSFORMED_POWER:
                if power >= move.power:
                    self.power = self.TRANSFORMED_POWER[power]
                    break

    def __repr__(self) -> str:
        if self.category == MoveCategory.STATUS:
            return (f"{colored(self.name, self.type.value.color)} ({self.type.value}) " + "PP: " + self.print_colored_pp() + " ~ "
                    f"{colored(self.category.value, 'cyan')} / {self.accuracy}% accuracy / {self.secondary_effect}")
        elif self.category == MoveCategory.PHYSICAL:
            category_color = "red"
        else:
            category_color = "magenta"
        return (f"{colored(self.name, self.type.value.color)} ({self.type.value}) " + "PP: " + self.print_colored_pp() + " ~ "
                f"{colored(self.category.value, category_color)} / {self.power} power ~ {self.accuracy}% accuracy / {self.secondary_effect}")
