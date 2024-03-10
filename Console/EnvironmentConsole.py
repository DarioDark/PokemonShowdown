from enum import Enum


class EnvironmentClass:
    def __init__(self):
        self.elements: list[EnvironmentElements] = []
        self.temporary_elements_turns: dict = {}
        
    def __getstate__(self):
        return {
            'elements': [element for element in self.elements if element]
        }
        
    def __setstate__(self, state):
        self.elements = [EnvironmentElements[element.name] for element in state['elements']]

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
        if turns != -1:
            self.temporary_elements_turns[element] = 5

    def remove_element(self, element: 'EnvironmentElements') -> None:
        """Remove an element from the environment.

        :param element: The element to remove.
        """
        self.elements.remove(element)
        
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
