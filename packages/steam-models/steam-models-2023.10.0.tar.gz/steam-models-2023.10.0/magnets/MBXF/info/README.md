# MBXF Quench Heaters

# IMPORTANT NOTES
The design of the MBXF quench heater strips features a zig-zag pattern that aims at covering different half-turns at different longitudinal positions.
In reality, the QH strips heat up different blocks of turns for Section A and B (see figure).

In the LEDET 2D model, this is reproduced by modeling one cross-section whose turns are heated up by strips both in Section A and B.
Each of the four quench heater circuits (composed of 2 strips in series) is modeled with FOUR quench heater strips, each as long as half a strip.
This approximation is taken since the strips touch the half-turns in Sections A and B (see figure) roughly for half of their length.
- #1 One (half-)strip heats the 1st block of half-turns for Section B (see figure)
- #2 One (half-)strip heats the 2nd block of half-turns for Section B (see figure)
- #3 One (half-)strip heats the 2nd block of half-turns for Section A (see figure)
- #4 One (half-)strip heats the 3rd block of half-turns for Section A (see figure)

To obtain correct QH peak current and discharge time constant, the following changes are applied to the parameters of the (half-)strips:
- voltage applied to each QH circuit is divided by 4
- QH power-supply capacitance is multiplied by 4
- QH circuit warm resistance is divided by 4
- QH strip length is divided by 2

The QH warm resistances and stainless-steel resistivity are selected so as to achieve the design power density of about 120 W/cm^2 (from "D1 update", HL-LHC Collaboration Meeting, 2019)