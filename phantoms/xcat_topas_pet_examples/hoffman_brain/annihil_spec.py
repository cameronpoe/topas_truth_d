# uses TruthTuple data to construct a plot of annihilation energy at annihilation and distance from start at annihilation

from config.definitions import ROOT_DIR
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

tup_file = open(os.path.join(ROOT_DIR, 'TruthTuple.phsp'), 'r')
tup_lines = tup_file.readlines()

num_positrons = 0
starting_energy = -1.0
energy = -1.0
previous_id = 0
starting_position = np.empty(3, dtype=float)
distance = 0.0
non_zero_diff = 0
difference = 0.0
energy_deposited = -1.0
data = pd.DataFrame(columns=['Starting Energy (keV)', 'Final Energy (keV)', 'Distance Travelled (cm)'])

# iterates through the different event lines
for line in tup_lines:
    line_list = line.split()
    # each subsequent step of a history
    id = int(line_list[7])
    if id == -11 and not id == previous_id:
        data.loc[len(data.index)] = [starting_energy, difference, distance]
        starting_energy = float(line_list[1])
        starting_position = np.array([float(line_list[3]), float(line_list[4]), float(line_list[5])])
        if not difference == 0.0:
            non_zero_diff += 1
        num_positrons += 1
    elif id == -11:
        energy = float(line_list[1])
        energy_deposited = float(line_list[2])
        position = np.array([float(line_list[3]), float(line_list[4]), float(line_list[5])])
        distance = np.linalg.norm(np.subtract(position, starting_position))
        difference = energy - energy_deposited
    previous_id = id
data.loc[len(data.index)] = [starting_energy, difference, distance]
if not difference == 0.0:
    non_zero_diff += 1
data = data.drop(0)

hist_starte = data.plot.hist(column=['Starting Energy (keV)'], range=[0.0, 650.0], bins=1300)
fig1 = hist_starte.get_figure()
fig1.savefig(os.path.join(ROOT_DIR, "fig1.png"))

hist_finale = data.plot.hist(column=['Final Energy (keV)'], range = [0.0, 50.0], bins=100)
fig2 = hist_finale.get_figure()
fig2.savefig(os.path.join(ROOT_DIR, "fig2.png"))

hist_distance = data.plot.hist(column=['Distance Travelled (cm)'], bins=100, range=[0.0, .5])
fig3 = hist_distance.get_figure()
fig3.savefig(os.path.join(ROOT_DIR, "fig3.png"))

print('Number of positrons found: ' + str(num_positrons))
print(data)
print('Number of positrons with non-zero difference between final energy and final energy deposited: ' + str(non_zero_diff))
tup_file.close()