# STEAM models - Magnets folder

This folder contains the input files for the Magnets models of the STEAM Library

It is organized in subfolders, each containing the input files for one magnet.
The input files in these subfolders are usually:
- .yaml file including magnet and conductor information
- .data ROXIE file defining magnet geometry
- .iron ROXIE file defining magnet iron-yoke geometry

The folder also includes the following subfolders that do not define magnet inputs:
- settings, where settings of individual users can be conveniently stored

The folder also contains these files used for more than one model:
- .cadata ROXIE file defining conductor geometry

Note: The ROXIE files in this project contain small modifications with repect to the official CERN ROXIE model repository, which is found at: https://espace.cern.ch/roxie/Lists/Links/ .
We are grateful to the CERN TE-MSC colleagues who developed and maintain the ROXIE model repository.
