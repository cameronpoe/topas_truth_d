# uses TruthTuple data to construct a plot of annihilation energy at annihilation and distance from start at annihilation

from config.definitions import ROOT_DIR
import os
import pandas as pd
import numpy as np

tup_file = open(os.path.join(ROOT_DIR, 'TruthTuple.phsp'), 'r')
tup_lines = tup_file.readlines()

num_positrons = 0
starting_energy = -1.0
energy = -1.0
previous_id = 0
starting_position = np.empty(3, dtype=float)
distance = 0.0
data = pd.DataFrame(columns=['StartingE', 'FinalE', 'Dist'])

# iterates through the different event lines
for line in tup_lines:
    line_list = line.split()
    # each subsequent step of a history
    id = int(line_list[7])
    if id == -11 and not id == previous_id:
        data.loc[len(data.index)] = [starting_energy, energy, distance]
        starting_energy = float(line_list[1])
        starting_position = np.array([float(line_list[3]), float(line_list[4]), float(line_list[5])])
        num_positrons += 1
    elif id == -11:
        energy = float(line_list[1])
        position = np.array([float(line_list[3]), float(line_list[4]), float(line_list[5])])
        distance = np.linalg.norm(np.subtract(position, starting_position))
    previous_id = id
data.loc[len(data.index)] = [starting_energy, energy, distance]
data.drop(0)
print('Number of positrons found: ' + str(num_positrons))
print(data)
tup_file.close()