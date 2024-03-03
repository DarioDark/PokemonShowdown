from enum import Enum

class EnvironmentClass:
    def __init__(self):
        self.elements: list[EnvironmentElements] = [EnvironmentElements.STEALTH_ROCK, EnvironmentElements.SPIKES]
        
    def __getstate__(self):
        return {
            'elements': [element for element in self.elements if element]
        }
        
    def __setstate__(self, state):
        self.elements = [EnvironmentElements[element.name] for element in state['elements']]
    
    def add_element(self, element: 'SecondaryEffectClass') -> None:
        self.elements.append(element)
        
    def remove_element(self, element: 'SecondaryEffectClass') -> None:
        self.elements.remove(element)
        
    def remove_toxic_spikes(self) -> None:
        for _ in range(self.elements.count(EnvironmentElements.TOXIC_SPIKES.value)):
            self.elements.remove(EnvironmentElements.TOXIC_SPIKES.value)
        

class EnvironmentElements(Enum):
    LIGHT_SCREEN = "Light Screen"
    REFLECT = "Reflect"
    SPIKES = "Spikes"
    STEALTH_ROCK = "Stealth Rock"
    TOXIC_SPIKES = "Toxic Spikes"
    TAILWIND = "Tailwind"