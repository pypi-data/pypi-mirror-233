from edgenerator.ed_class import EDGeneratorSettings

# o=======================================================o
#                        Functions
# o=======================================================o


def make_inputfile(output_path: str, ed_settings: EDGeneratorSettings) -> str:
    """
    Makes the input file for the energyleveler.py script
    All the information should be present in the ::EDGeneratorSettings:: instance called ed_settings
    """

    outfile = f"{output_path}/{ed_settings.settings.outputfile}.inp"
    with open(outfile, 'w') as output:
        output.write(f"output-file     = {outfile}.png"
                     f"\nwidth           = {ed_settings.settings.width}"
                     f"\nheight          = {ed_settings.settings.height}"
                     f"\nenergy-units    = {ed_settings.settings.energy_unit}"
                     f"\nenergy range    = {ed_settings.settings.energy_range[0]},{ed_settings.settings.energy_range[1]}"
                     f"\nfont size       = {ed_settings.settings.font_size}"
                     f"\nfont            = {ed_settings.settings.font_family}"

                     "\n\n#   This is a comment. Lines that begin with a # are ignored."
                     "\n#   Available colours are those accepted by matplotlib "
                     "\n\n#   Now begins the states input")

        for i, path in enumerate(ed_settings.paths):
            output.write(f"\n\n#-------  Path {i+1}: {path.name} ----------\n")
            for j, state in enumerate(path.states):
                output.write("\n{")
                output.write(f"\n\ttext-colour = {path.colour}")
                output.write(f"\n\tname        = {state.label}")
                output.write(f"\n\tcolumn      = {state.column}")
                output.write(f"\n\tenergy      = {float(state.energy) :2.1f}")

                # conditional prints
                if i == 0:
                    output.write("\n\tlabelColour = black")
                else:
                    output.write(f"\n\tlabelColour = {path.colour}")

                if i == 0:
                    output.write(f"\n\tlabel       = {state.label.split('_')[1]}")

                if j == 0 and ed_settings.settings.plot_legend:
                    output.write(f"\n\tlegend       = {path.name}")

                if ed_settings.settings.hide_energy:
                    output.write("\n\tHIDE ENERGY")

                if state.linksTo is not None:
                    output.write(f"\n\tlinksto     = {state.linksTo}:{path.colour}")

                output.write("\n}\n")
        return outfile
