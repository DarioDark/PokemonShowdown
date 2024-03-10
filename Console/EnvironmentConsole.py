from enum import Enum


class EnvironmentClass:
    def __init__(self):
        self.elements: list[EnvironmentElements] = [EnvironmentElements.TOXIC_SPIKES]
        
    def __getstate__(self):
        return {
            'elements': [element for element in self.elements if element]
        }
        
    def __setstate__(self, state):
        self.elements = [EnvironmentElements[element.name] for element in state['elements']]
    
    def add_element(self, element: 'EnvironmentElements') -> None:
        """Add an element to the environment.

        :param element: The element to add.
        """
        self.elements.append(element)
        
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
    # TAILWIND = "Tailwind"
    # TRICK_ROOM = "Trick Room"
