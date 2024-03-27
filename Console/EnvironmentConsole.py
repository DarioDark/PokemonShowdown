from enum import Enum


class EnvironmentClass:
    def __init__(self):
        self.elements: list[EnvironmentElements] = []
        self.temporary_elements_turns: dict[EnvironmentElements: int] = {}

    def __getstate__(self):
        state = self.__dict__.copy()  # start with the object's dictionary
        state['elements'] = [element.name for element in self.elements if element]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)  # update the object's state from the dictionary
        self.elements = [EnvironmentElements[element_name] for element_name in state['elements']]

    def pass_turn(self) -> None:
        """Pass a turn in the environment, removing temporary elements if their duration is over."""
        for element_name in self.temporary_elements_turns:
            self.temporary_elements_turns[element_name] -= 1
            if self.temporary_elements_turns[element_name] == 0:
                self.elements.remove(element_name)
                del self.temporary_elements_turns[element_name]
    
    def add_element(self, element: 'EnvironmentElements', turns: int = -1) -> None:
        """Add an element to the environment.

        :param element: The element to add.
        :param turns: The number of turns the element will last.
        """
        self.elements.append(element)

        # Weathers
        elements_to_remove = [EnvironmentElements.SUN, EnvironmentElements.RAIN, EnvironmentElements.SAND, EnvironmentElements.SNOW]
        if element in elements_to_remove:
            for elem in elements_to_remove:
                if elem in self.elements and elem != element:
                    self.elements.remove(elem)
                    del self.temporary_elements_turns[elem]

        if turns != -1:
            self.temporary_elements_turns[element] = turns

    def remove_toxic_spikes(self) -> None:
        """Remove all toxic spikes from the environment.
        """
        for _ in range(self.elements.count(EnvironmentElements.TOXIC_SPIKES)):
            self.elements.remove(EnvironmentElements.TOXIC_SPIKES)
        

class EnvironmentElements(Enum):
    LIGHT_SCREEN = "Light Screen"
    REFLECT = "Reflect"
    STEALTH_ROCK = "Stealth Rock"
    SPIKES = "Spikes"
    TOXIC_SPIKES = "Toxic Spikes"
    AURORA_VEIL = "Aurora Veil"
    TAILWIND = "Tailwind"
    # TRICK_ROOM = "Trick Room"
    SUN = "Sun"
    RAIN = "Rain"
    SAND = "Sand"
    SNOW = "Snow"
    GRASSY_TERRAIN = "Grassy Terrain"
    MISTY_TERRAIN = "Misty Terrain"
    ELECTRIC_TERRAIN = "Electric Terrain"
    PSYCHIC_TERRAIN = "Psychic Terrain"
