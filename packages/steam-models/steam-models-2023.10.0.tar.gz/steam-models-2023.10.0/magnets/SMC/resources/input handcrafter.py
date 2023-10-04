import numpy as np
import svgwrite
from scipy.interpolate import CubicSpline

def apritner(key, list_input):
    str_list = []
    for i, inp in enumerate(list_input):
        if (i == 0) and (i == len(list_input) - 1):
            str_list.append('[' + str(inp) + ']')
        elif i == 0:
            str_list.append('[' + str(inp))
        elif i == len(list_input) - 1:
            str_list.append(str(inp) + ']')
        else:
            str_list.append(str(inp))
    print(f'{key}: ' + ', '.join(str_list))

#inputs specific for magnet
conductors_in_groups = [35]
alpha_starts = [-90.0]
I_initial = 14500.0
QH_in_magnet = ['ref_QH']

# inputs general
magnetic_length = 0.3   # TODO
groups = [1, 2, 1, 2]
polarities = [1, -1, -1, 1]
number_of_groups = len(groups)

alpha_steps = [0] * len(conductors_in_groups)   # taken from roxie, same cable everywhere
rotation_ht_def = [0.0, 180.0, 90.0, 270.0]
mirror_ht_def = [0, 0, 1, 1]
mirrorY_ht_def = [0, 0, 0, 0]
tQuench_def = -0.015
initialQuenchTemp_def = 10
post_proc_coil_sections = 1

#bare_cable_height_high_in_groups = [1.658e-3, 1.658e-3, 1.658e-3, 1.658e-3, 1.658e-3, 1.658e-3]    # the same cable everywhere
cable_h = {'SMC11T150': {'i': 1.305e-3, 'o': 1.305e-3, 'w': 14.847e-3}}

# Quench heater power supply and circuit parameters
U0_def = 450.0
C_def = 0.0141
h_def = 2.5e-05
s_ins_def = 5e-05
type_ins_def = 2
s_ins_He_def = 0.0005
type_ins_He_def = 2
l_def = magnetic_length
target_I = 150  # A
t_trigger_def = 99999.0

w_def = {'ref_QH': 0.02}
l_copper_def = {'ref_QH': 0.2641}
l_stainless_steel_def = {'ref_QH': 0.05}
QH_turns_starting_turn = {'ref_QH': 2}
QH_covered_wedge_width = {'ref_QH': 0}
QH_cable_covered = {'ref_QH': 'SMC11T150'}
QH_cable_side_covered = {'ref_QH': 'o'}
QH_turns_covered = {'ref_QH': round(w_def['ref_QH'] / cable_h[QH_cable_covered['ref_QH']][QH_cable_side_covered['ref_QH']])}

ro_SS_LEDET_mat = 0.00000049999     #  @1.9 in LEDET-materials-library, rhoSS_CERN_mat.m
fScaling_RhoSS = 1.09
ro_SS_LEDET = ro_SS_LEDET_mat * fScaling_RhoSS

# CLIQ
R_CLIQ_def = 0.025
f_CLIQ = 48.765#45.315 #47.89        # target frequency of CLIQ discharge, neglecting magnet quenched region resistance and differential inductance (Hz)
fI_CLIQ = 1000/I_initial       # fraction of nominal current for CLIQ discharge

w_def = {}
for i, QH_type in enumerate(QH_in_magnet):
    cable_type = QH_cable_covered[QH_type]
    cable_side = QH_cable_side_covered[QH_type]
    cable_height = cable_h[cable_type][cable_side]
    wedge_covered = QH_covered_wedge_width[QH_type]
    n_turns_covered = QH_turns_covered[QH_type]
    w_def[QH_type] = round((n_turns_covered*cable_height + wedge_covered), 5)



# 'code'
key = 'conductor_to_group'
conductor_to_group = len(conductors_in_groups) * number_of_groups * [1]
apritner(key, conductor_to_group)

key = 'group_to_coil_section'
group_to_coil_section = []
for g in groups:
    group_to_coil_section.extend(len(conductors_in_groups) * [g])
apritner(key, group_to_coil_section)

key = 'polarities_in_group'
polarities_in_group = []
for p in polarities:
    polarities_in_group.extend(len(conductors_in_groups) * [p])
apritner(key, polarities_in_group)

key = 'half_turn_length'
half_turn_length = len(conductors_in_groups) * number_of_groups * [magnetic_length]
apritner(key, half_turn_length)

key = 'overwrite_electrical_order'
overwrite_electrical_order = list(range(1, sum(conductors_in_groups) * number_of_groups + 1))
apritner(key, overwrite_electrical_order)

key = 'I_initial'
print(f'{key}: {I_initial}')

key = 'I_control_LUT'
print(f'{key}: [{I_initial}, {I_initial}, {0.0}]')

key = 'Iref'
print(f'{key}: {I_initial}')

key = 'current_direction'
current_direction = [1]
apritner(key, current_direction)


key = 'alphaDEG_ht'
alphaDEG_ht = []
for _ in range(number_of_groups):
    for alpha_start, alpha_step, c_in_g in zip(alpha_starts, alpha_steps, conductors_in_groups):
        for c in range(c_in_g):
            alphaDEG_ht.append(round(alpha_start + c * alpha_step, 4))
apritner(key, alphaDEG_ht)

key = 'rotation_ht'
rotation_ht = []
for r in rotation_ht_def:
    rotation_ht.extend(sum(conductors_in_groups) * [r])
apritner(key, rotation_ht)

key = 'mirror_ht'
mirror_ht = []
for m in mirror_ht_def:
    mirror_ht.extend(sum(conductors_in_groups) * [m])
apritner(key, mirror_ht)

key = 'mirrorY_ht'
mirrorY_ht = []
for mY in mirrorY_ht_def:
    mirrorY_ht.extend(sum(conductors_in_groups) * [mY])
apritner(key, mirrorY_ht)

key = 'tQuench'
tQuench = []
for _ in range(post_proc_coil_sections):
    tQuench.append(tQuench_def)
apritner(key, tQuench)

key = 'initialQuenchTemp'
initialQuenchTemp = []
for _ in range(post_proc_coil_sections):
    initialQuenchTemp.append(initialQuenchTemp_def)
apritner(key, initialQuenchTemp)

f_cover_def = {}
for QH_type in QH_in_magnet:
    f_cover_def[QH_type] = round(l_stainless_steel_def[QH_type]/(l_stainless_steel_def[QH_type] + l_copper_def[QH_type]), 5)

R_warm = []
R_heaters = []
for i_g in range(number_of_groups):
    for i_qh, QH_type in enumerate(QH_in_magnet):
        R_heater = l_def * ro_SS_LEDET * f_cover_def[QH_type] / (h_def * w_def[QH_type])  # assuming SS dominates, i.e. as in LEDET
        R_w = U0_def / target_I - R_heater
        R_warm.append(round(R_w, 5))
        R_heaters.append(R_heater)
# print(f'R_heaters: {R_heaters}')

N_strips = number_of_groups * len(QH_in_magnet)
print(f'N_strips: {N_strips}')

keys = ['t_trigger', 'U0', 'C']
vals = [t_trigger_def, U0_def, C_def]
for key, val in zip(keys, vals):
    out_list =[]
    for _ in range(N_strips):
        out_list.append(val)
    apritner(key, out_list)

keys = ['R_warm']
vals = [R_warm]
for key, val in zip(keys, vals):
    apritner(key, val)

keys = ['w']
vals = [w_def]
for key, val in zip(keys, vals):
    out_list = []
    for _ in range(number_of_groups):
        for QH_type in QH_in_magnet:
            out_list.append(val[QH_type])
    apritner(key, out_list)

keys = ['h', 's_ins', 'type_ins', 's_ins_He', 'type_ins_He', 'l']
vals = [h_def, s_ins_def, type_ins_def, s_ins_He_def, type_ins_He_def, l_def]
for key, val in zip(keys, vals):
    out_list =[]
    for _ in range(N_strips):
        out_list.append(val)
    apritner(key, out_list)


keys = ['l_copper', 'l_stainless_steel', 'f_cover']
vals = [l_copper_def, l_stainless_steel_def, f_cover_def]
for key, val in zip(keys, vals):
    out_list = []
    for _ in range(number_of_groups):
        for QH_type in QH_in_magnet:
            out_list.append(val[QH_type])
    apritner(key, out_list)

# for key, val in zip(keys, vals):
#     apritner(key, val)

key = 'iQH_toHalfTurn_From'
iQH_toHalfTurn_From = []
for i_g in range(number_of_groups):
    for i_qh, QH_type in enumerate(QH_in_magnet):
        for _ in range(QH_turns_covered[QH_type]):
            iQH_toHalfTurn_From.append(i_g*len(QH_in_magnet) + i_qh+1)
apritner(key, iQH_toHalfTurn_From)

key = 'iQH_toHalfTurn_To'
iQH_toHalfTurn_To = []
for i_g in range(number_of_groups):
    for i_qh, QH_type in enumerate(QH_in_magnet):
        for i_t in range(QH_turns_covered[QH_type]):
            iQH_toHalfTurn_To.append(i_g * sum(conductors_in_groups) + QH_turns_starting_turn[QH_type] + i_t)
        #iQH_toHalfTurn_To.extend(list(range(i_g * sum(conductors_in_groups) + st, i_g * sum(conductors_in_groups) + st + QH_half_turns_covered[i_st])))
apritner(key, iQH_toHalfTurn_To)



# find l_copper to achieve target_I without negative R_warm at full l_def, only works for full length l_def
# print(f"Finding optimal l_copper:...")
# for i_qh, QH_type in enumerate(QH_in_magnet):
#     l_copper = 0.9
#     R_w = 1
#     while R_w < 0 or R_w > 1e-2:
#         f_cover_def = round(l_stainless_steel_def[QH_type] / (l_stainless_steel_def[QH_type] + l_copper), 5)
#         R_heater = l_def * ro_SS_LEDET * f_cover_def / (h_def * w_def[QH_type])  # assuming SS dominates, i.e. as in LEDET
#         R_w = U0_def / target_I - R_heater
#         if R_w > 0:
#             l_copper = round(l_copper * 0.999, 4)
#         else:
#             l_copper = round(l_copper * 1.001, 4)
#     print(f"'{QH_type}': l_copper: {l_copper} for R_warm: {R_w}")
# print(f"Paste these values into l_copper_def")



def create_svg_table(data_list, headers, cell_width=200, cell_height=30, header_color='gray', row_color='white'):
    # Combine the dictionaries into a single list of (key, value) tuples
    rows = []
    keys = set()
    for data in data_list:
        for key, value in data.items():
            if key not in keys:
                rows.append((key, [value]))
                keys.add(key)
            else:
                for i, row in enumerate(rows):
                    if row[0] == key:
                        row[1].append(value)
                        break

    # Calculate the size of the SVG based on the number of rows and columns
    num_rows = len(rows)
    num_cols = len(data_list) + 1
    svg_width = num_cols * cell_width
    svg_height = (num_rows + 1) * cell_height

    # Create the SVG object
    dwg = svgwrite.Drawing(size=(svg_width, svg_height))

    # Draw the table headers
    for i, header in enumerate(headers):
        dwg.add(dwg.rect((i * cell_width, 0), (cell_width, cell_height), fill=header_color))
        dwg.add(dwg.text(header, insert=(i * cell_width + cell_width / 2, cell_height / 2), fill='white', text_anchor='middle', alignment_baseline='middle'))

    # Draw the table rows
    for i, (key, values) in enumerate(rows):
        y = (i + 1) * cell_height
        dwg.add(dwg.rect((0, y), (cell_width, cell_height), fill=row_color))
        dwg.add(dwg.text(key, insert=(cell_width / 2, y + cell_height / 2), fill='black', text_anchor='middle', alignment_baseline='middle'))
        for j, value in enumerate(values):
            dwg.add(dwg.rect((cell_width * (j + 1), y), (cell_width, cell_height), fill=row_color))
            if isinstance(value, float):
                value = round(value, 5)
            value_str = str(value)
            dwg.add(dwg.text(value_str, insert=(cell_width * (j + 1) + cell_width / 2, y + cell_height / 2), fill='black', text_anchor='middle', alignment_baseline='middle'))

    return dwg.tostring()


data_list = [l_copper_def, l_stainless_steel_def, QH_turns_covered, QH_covered_wedge_width, QH_cable_side_covered]

headers = ['heater name', 'l copper (m)', 'l SS (m)', '# turns covered', 'Wedge width covered', 'Inner/Outer']
svg = create_svg_table(data_list, headers)
with open('heater_parmas.svg', 'w') as f:
    f.write(svg)