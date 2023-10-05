import os
import attrs
from typing import Optional

from edgenerator.ed_class import EDGeneratorSettings
from edgenerator.profiles import EDProfile
from edgenerator.energy_leveler import ReadInput
from edgenerator.read_excel import read_excelfile
from edgenerator.prepare_input import make_inputfile


def run_edgenerator(excelfile_path: str, workdir_path: str, profile: Optional[EDProfile] = None):
    """
    Runs the program
    Arguments:
        Absolute path to the excel file
        Absolute path of the output folder
    Output:
        A png file (or pdf) with the energy diagram
    """
    if profile is None:
        profile = EDProfile()
        print("No profile specified, using default profile")
    else:
        print(f"Using user profile with name {profile.name}")

    # Create the EDGeneratorSettings instance, which contains the settings and the pathways (one pathway contains multiple States) used for the diagram
    ed_settings = EDGeneratorSettings(settings=profile)

    print(f"Reading Excel file (path = {excelfile_path})")
    ed_settings = read_excelfile(excelfile_path, ed_settings)

    print("\n***Settings***")
    [print(f"{key}: {value}") for key, value in attrs.asdict(ed_settings.settings).items()]
    print(f"Num. Paths {len(ed_settings.paths)}\n")

    # Assign colours to the pathways as specified by the profile
    ed_settings.assign_colour_to_pathways()

    # Make links between states in a pathway so sequential states are connected with lines in the diagram
    ed_settings.make_links()

    # Calculate the relative energies (with respect to the first state in the pathway, often being "R1", or reactant)
    if ed_settings.settings.normalise:
        ed_settings.calculate_relative_energies()

    # Make the inputfile that will be read by energyleveler.py
    inputfile = make_inputfile(workdir_path, ed_settings)

    print("Running energyleveler.py...\n")
    diagram = ReadInput(inputfile)
    diagram.MakeLeftRightPoints()
    diagram.Draw()
    if ed_settings.settings.delete_inputfile:
        print("Removing inputfile...")
        os.remove(inputfile)

    print("Finished!\n")

    print("o=======================================================o")
    print(f"{ed_settings.settings.outputfile}.png is made in {workdir_path}!")
    print("o=======================================================o")
