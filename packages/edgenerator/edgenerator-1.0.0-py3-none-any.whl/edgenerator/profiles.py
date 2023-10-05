"""
This module contains profiles used for making energy diagrams.
"""
from attrs import define, field
from typing import List


@define
class EDProfile():
    """A class representing an energy diagram profile.

    Attributes:
        name (str): The name of the profile.
        outputfile (str): The name of the output file.
        width (int): The width of the energy diagram.
        height (int): The height of the energy diagram.
        energy_type (str): The type of energy (E, H, or G).
        energy_range (list[int]): The energy range (often in kcal mol-1).
        font_size (int): The font size of the energy diagram.
        font_family (str): The font family of the energy diagram.
        colour_list (list[str]): The list of colours used in the energy diagram.
        hide_energy (bool): Whether to hide the energy values in the energy diagram.
        normalise (bool): Whether to normalise the energy values in the energy diagram.
        plot_legend (bool): Whether to plot the legend in the energy diagram.
        delete_inputfile (bool): Whether to delete the input file after plotting the energy diagram.
    """

    name: str = "default"
    outputfile: str = "default_output"
    width: int = 8
    height: int = 8
    energy_type: str = "G"
    energy_range: List[int] = field(factory=lambda: [-40, 40])
    energy_unit: str = "$\Delta \it{XXX}$  / kcal mol$^{-1}$"  # noqa: W605 (invalid escape sequence)
    font_size: int = 14
    font_family: str = "DejaVu Sans"
    colour_list: List[str] = field(factory=lambda: ['black', 'blue', 'green', 'red', 'cyan', 'purple', 'brown'])
    hide_energy: bool = True
    normalise: bool = False
    plot_legend: bool = True
    delete_inputfile: bool = True

    def __post_attrs_init__(self):
        """ Post-initialisation hook for EDProfile. """
        self.energy_unit = self.energy_unit.replace("XXX", self.energy_unit)
