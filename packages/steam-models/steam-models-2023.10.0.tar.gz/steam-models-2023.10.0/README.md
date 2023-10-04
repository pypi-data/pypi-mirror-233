# steam_models

Repository of STEAM superconducting magnets and circuit models
(Copyright © 2022, CERN, Switzerland. All rights reserved.)


# Installation

## Released version:
pip install steam-models

## Test version:
pip install -i https://test.pypi.org/simple/ steam-models

# Links
STEAM website: https://espace.cern.ch/steam/

# Contact
steam-team@cern.ch

# STEAM User Agreement
By using any software of the STEAM framework, users agree with this document:
https://edms.cern.ch/document/2024516


# QUICK START
- Clone the project to your local folder
- Available model input files are located in subfolders \conductors, \magnets, and \circuits. In this example, the model located in \magnets\MBRD\input\ will be built.
- Add your personal settings file: you can start by copying/pasting the file settings\user_settings\settings.SYSTEM.yaml
- Install the Python package steam-sdk (https://pypi.org/project/steam-sdk/)
    - If you know how to install a Python package, go for it!
    - If you don't know, you can run these code lines in a notebook cell
```ruby
import sys
!{sys.executable} -m pip install --user --upgrade steam-sdk
```
- Open the notebook STEAM_Library_withoutWidgets.ipynb (recommended using Jupyter or SWAN)
- Edit the values of the following inputs according to wishes:
```ruby
case_model:    str  = 'magnet'
model_name:    str  = 'MBRD'
software:      str  = 'LEDET'
flagBuild:     bool = True
verbose:       bool = False
flag_plot_all: bool = True
```
- Run the cell. The code will generate a LEDET model in the folder \magnets\MBRD\output\.
