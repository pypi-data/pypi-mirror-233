from edgenerator.state_classes import Pathway
from edgenerator.profiles import EDProfile
from attrs import define, field


@define
class EDGeneratorSettings():
    settings: EDProfile = field(factory=lambda: EDProfile)
    paths: list[Pathway] = field(factory=lambda: [])

    def assign_colour_to_pathways(self):
        """
        Loops over pathways found in the profile and assigns a colour to each of them
        The colours are defined in the profiles.py with the associated profile
        """
        if len(self.settings.colour_list) < len(self.paths):
            raise IndexError(f"Error: not enough colours defined in profile: {self.settings.name}")

        for i, path in enumerate(self.paths):
            path.colour = self.settings.colour_list[i]

    def make_links(self):
        """
        Creates links between states in a pathway by assigning the label of the next state to the current state
        """
        for path in self.paths:
            for i, state in enumerate(path):
                state.linksTo = path.states[i+1].label if i < len(path.states)-1 else None

    def calculate_relative_energies(self):
        """
        Calculates the relative energies of the states in the pathways with respect to the first state (being the reactant)
        """
        for path in self.paths:
            for state in path:
                state.energy = state.energy - path.states[0].energy
