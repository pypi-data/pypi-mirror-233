# Energy Diagram Generator (edgenerator)

Welcome to the Energy Diagram Generator (edgenerator) project. This project generates energy diagrams often used in computational chemistry. The project is currently in development and is not yet ready for use. The project is developed by Siebe Lekanne Deprez (GitHub: SiebeLeDe) and is based on the work of [JFurness1](https://github.com/JFurness1/EnergyLeveller)

## Purpose of Energy Diagram Generator (edgenerator)

Plotting energy diagrams manually with for example Excel takes a lot of time and labour. Also, when you want you change colours or other properties of the energy diagram, you have to change every single plot. Therefore, this package contains python scripts that make it more easy for making energy diagrams associated with computational chemistry.

## Example Usage

There are two objects to import: `EDProfile` and `run_edgenerator`. The first object is used to define the properties of the energy diagram and can be considered as a config file. The second one is a function and is used to generate the energy diagram. I recommend having a python linter that lists the options for the `EDProfile`.

```python
import os
from edgenerator.main_program import run_edgenerator
from edgenerator.profiles import EDProfile

user_profile = EDProfile(
    name="test",
    energy_range=[-100, 100],
    colour_list=['#000000', '#0000FF', '#008000', '#FF0000', '#800080', 'yellow'],
    hide_energy=True,
    delete_inputfile=False,
    plot_legend=True)


workbook_path = os.path.join(os.path.dirname(__file__), 'NA Active Site_dE.xlsx')
workdir = os.path.dirname(__file__)

run_edgenerator(excelfile_path=workbook_path, workdir_path=workdir, profile=user_profile)
```

## EDProfile options

The following options are available when creating an `EDProfile` object:

- `name` (str): The name of the profile. Defaults to "default".
- `outputfile` (str): The name of the output file. Defaults to "default_output".
- `width` (int): The width of the energy diagram. Defaults to 10.
- `height` (int): The height of the energy diagram. Defaults to 10.
- `energy_type` (str): The type of energy (E, H, or G). Defaults to "E".
- `energy_range` (list[int]): The energy range (often in kcal mol-1). Defaults to [-100, 100].
- `font_size` (int): The font size of the energy diagram. Defaults to 14.
- `font_family` (str): The font family of the energy diagram. Defaults to "Arial".
- `hide_energy` (bool): Whether to hide the energy values in the energy diagram. Defaults to True
- `normalise` (bool): Whether to normalise the energy values in the energy diagram. Defaults to False.
- `plot_legend` (bool): Whether to plot the legend in the energy diagram. Defaults to True.
- `delete_inputfile` (bool): Whether to delete the input file after plotting the energy diagram. Defaults to False.
- `image_format` (str): The image format of the energy diagram. Defaults to "png".

## How to Contribute

Everyone is welcome to contribute to this project. Please do so by making a pull request, or raising an issue.
Preferably, please use the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) and the Google docstring style when writing docstrings.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
