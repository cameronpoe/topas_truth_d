# uses TruthTuple data to construct a plot of annihilation energy at annihilation and distance from start at annihilation

from config.definitions import ROOT_DIR
import os
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

tup_file = open(os.path.join(ROOT_DIR, 'TruthTuple.phsp'), 'r')
tup_lines = tup_file.readlines()


previous_id = 0
starting_energy = -1.0
starting_x_pos = 0.0
starting_position = np.empty(3, dtype=float)

energy = -1.0
energy_deposited = -1.0
difference = 0.0

num_positrons = 0
non_zero_diff = 0

x_distance = 0.0
distance = 0.0

data = pd.DataFrame(columns=['starte', 'finale', 'xdist', 'diste', 'linenum'])


count = 0
# iterates through the different event lines
for line in tup_lines:
    count += 1
    line_list = line.split()
    # each subsequent step of a history
    id = int(line_list[7])
    if id == -11 and not id == previous_id:
        # adds data line to pandas dataframe
        data.loc[len(data.index)] = [starting_energy, difference, x_distance, distance, count]
        
        # defines history's starting energy for data line
        starting_energy = float(line_list[1])
        # defines history's starting x value
        starting_x_pos = float(line_list[3])
        # defines history's starting position for use in distance calculation
        starting_position = np.array([float(line_list[3]), float(line_list[4]), float(line_list[5])])

        # adds count to tally of positrons with non-zero final energy (difference is the actual final energy)
        if not difference == 0.0:
            non_zero_diff += 1
        
        # adds count to tally of number of positron histories looped through 
        num_positrons += 1
    
    elif id == -11:
        # calculates the difference between energy at beginning of the step and energy deposited. 
        # we believe that when step is the very last one of the positron history, the difference is how much energy the positron annihilates with
        energy = float(line_list[1])
        energy_deposited = float(line_list[2])
        difference = energy - energy_deposited
        # calculates the distance from origin point in x
        x_position = float(line_list[3])
        x_distance = x_position - starting_x_pos
        # calculates the absolute distance from origin point
        position = np.array([x_position, float(line_list[4]), float(line_list[5])])
        distance = np.linalg.norm(np.subtract(position, starting_position))
        
    previous_id = id

# adds final history data
data.loc[len(data.index)] = [starting_energy, difference, x_distance, distance, count]
# does final history checks/counts
if not difference == 0.0:
    non_zero_diff += 1

# drops first line of dataframe since it is built on default values
data = data.drop(0)

plt.figure(1)
fig1, ax1 = plt.subplots()
ax1.hist(data['starte'], range=(0.0, 635.0), bins=2540, density=True)
x = np.linspace(0.25, 635.0, 2539)
def y(x):
    return ((-1.54629e-13)*((635.0-x)**2)*(x**2))/(1.0-math.exp(((18.0*math.pi)/137.0)*math.sqrt((2.0*x)/511.0)))
y2 = np.vectorize(y)
ax1.plot(x, y2(x), 'r', label='Input function')
plt.title('Probability Density of Positron Kinetic Energies at Decay')
plt.legend(loc='upper right')
plt.xticks()
plt.ylabel('Probability')
plt.xlim((0.0, 650.0))
plt.ylim((0.0, 0.004))
plt.xlabel('Kinetic Energy (keV)')
plt.savefig('starte.png')

plt.figure(3)
fig3, ax3 = plt.subplots()
ax3.hist(data["diste"], range=(0.0, 0.25), bins=100, density=True)
plt.title('Probability Density of Absolute Distances from Positron Decay Point to Annihilation Point', wrap=True)
plt.xticks()
plt.locator_params(axis='y', integer=True)
plt.ylabel('Probability')
plt.xlabel('Distance (cm)')
plt.savefig('absdist.png')

plt.figure(4)
fig4, ax4 = plt.subplots()
ax4.hist(data["xdist"], range=(-0.2, 0.2), bins=80, density=True)
plt.title('Probability Density of Distances along X-axis from Positron Decay Point to Annihilation Point', wrap=True)
plt.xticks()
plt.yticks()
plt.locator_params(axis='y', integer=True)
plt.ylabel('Probability')
plt.xlabel('Distance (cm)')
plt.savefig('xdist.png')

plt.figure(2)
fig2, ax2 = plt.subplots()
ax2.hist(data.replace(0.0, np.NaN)['finale'], range=(0.0, 560.0), bins=35)
plt.title('Distribution of Non-zero Kinetic Energies at Annihilation Point')
plt.xticks()
plt.locator_params(axis='y', integer=True)
plt.ylabel('Frequency (# of positrons)')
plt.xlabel('Kinetic Energy (keV)')
plt.savefig('finale.png')

f = open('README_annihilation_spectrum.txt', 'w')

f.write('Number of positrons: %s\n'%str(num_positrons))
f.write('Minimum non-zero values of the columns: %s'%str(data.where(data.gt(0)).min(0)))
f.write('Maximum annihilation energy: %s keV at line %s\n'%(str(data['finale'].max()), str(data.loc[data['finale'].idxmax(), 'linenum'])))
f.write('Maximum absolute distance : %s\n'%str(data['diste'].max()))
f.write('Maximum distance in x direction: %s\n'%str(data['xdist'].max()))
f.write('Minimum distance in x direction: %s\n'%str(data['xdist'].min()))
f.write('Number of positrons with non-zero difference between final energy and final energy deposited: %s\n'%str(non_zero_diff))

tup_file.close()
f.close()