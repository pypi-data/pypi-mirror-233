from typing import List, Tuple, Any
from attrs import define, field


@define(frozen=False, slots=False)
class State:
    """
    Class for describing one state
    """
    name: str = ""
    color: str = "k"
    labelColor: str = "k"
    linksTo: str = ""
    label: str = ""
    legend: str = None
    energy: float = 0.0
    normalisedPosition: float = 0.0
    column: int = 1
    leftPointx: int = 0
    leftPointy: int = 0
    rightPointx: int = 0
    rightPointy: int = 0
    labelOffset: Tuple[int, int] = (0, 0)
    textOffset: Tuple[int, int] = (0, 0)
    imageOffset: Tuple[int, int] = (0, 0)
    imageScale: float = 1.0
    image: Any = None
    show_energy: bool = True
    dont_plot: bool = False


@define(frozen=False, slots=False)
class Pathway():
    """
    Class for describing one pathway.
    Attributes:
    - name (str): name of pathway corresponding to system
    - colour (str): color of the pathway
    - states (List[State]): list of states in the pathway
    """

    name: str
    colour: str = "k"
    states: List[State] = field(factory=list)

    def print_pathway(self):
        """
        Prints the label and energy of each state in the pathway.
        """
        for state in self.states:
            print(state.label, state.energy)

    def add_state(self, new_state):
        """
        Adds a new state to the pathway.

        Args:
        - new_state (State): the new state to add to the pathway
        """
        self.states.append(new_state)

    def __iter__(self):
        """
        Returns an iterator over the states in the pathway.
        """
        for state in self.states:
            yield state
