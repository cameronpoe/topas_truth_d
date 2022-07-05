# uses TruthTuple data to construct a plot of annihilation energy at annihilation and distance from start at annihilation

from config.definitions import ROOT_DIR
import os
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

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

# plots figure 1, the energy at decay
plt.figure(1)
fig1, ax1 = plt.subplots()
ax1.hist(data['starte'], range=(0.0, 635.0), bins=1270, density=True, label='50,000 $e^+$ in\n0.5 keV bins')
x = np.linspace(0.25, 635.0, 2539)
def y(x):
    return ((-1.54629e-13)*((635.0-x)**2)*(x**2))/(1.0-math.exp(((18.0*math.pi)/137.0)*math.sqrt((2.0*x)/511.0)))
y2 = np.vectorize(y)
ax1.plot(x, y2(x), 'r', label='Input function')
plt.suptitle('Probability Density of Kinetic Energies at Decay in the XCAT Brain', wrap=True)
plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
plt.legend(loc='upper right')
plt.xticks()
plt.minorticks_on()
plt.ylabel('Probability (1/keV)')
plt.xlim((0.0, 650.0))
plt.ylim((0.0, 0.004))
plt.xlabel('Kinetic Energy (keV)')
plt.savefig('starte.png')

# plots figure 3, histogram of absolute distances from decay point
plt.figure(3)
fig3, ax3 = plt.subplots()
ax3.hist(data["diste"].multiply(10.0), range=(0.0, 2.5), bins=50, density=True, label='50,000 $e^+$ in\n0.05 mm bins')
plt.title('Probability Density of Absolute Distances from Decay Point to Annihilation Point in the XCAT Brain', wrap=True)
plt.legend(loc='upper right')
plt.xticks()
plt.minorticks_on()
plt.ylabel('Probability (1/keV)')
plt.xlabel('Distance (mm)')
plt.savefig('absdist.png')

plt.figure(4)
fig4, ax4 = plt.subplots()
ax4.hist(data["xdist"].multiply(10.0), range=(-2.0, 2.0), bins=80, density=True, label='50,000 $e^+$ in\n0.05 mm bins')
plt.title('Probability Density of Distances along X-axis from Decay Point to Annihilation Point in the XCAT Brain', wrap=True)
plt.legend(loc='upper right')
plt.xticks()
plt.yticks()
plt.minorticks_on()
plt.ylabel('Probability (1/keV)')
plt.xlabel('Distance (mm)')
plt.savefig('xdist.png')

plt.figure(2)
fig2, ax2 = plt.subplots()
ax2.hist(data['finale'], range=(0.0, 560.0), bins=56, label='50,000 $e^+$ in\n10 keV bins', density=True)
#y_vals = ax2.get_yticks()
#ax2.yaxis.set_major_locator(mticker.FixedLocator(y_vals))
#ax2.set_yticklabels([f'{x:.2f}'.format(x * 10.0) for x in y_vals])
plt.title('Probability Density of Kinetic Energies at Annihilation Point in the XCAT Brain', wrap=True)
plt.legend(loc='upper right')
plt.yscale('log')
plt.xticks()
plt.minorticks_on()
plt.ylabel('Probability (1/keV)')
#plt.ylabel('Probability (per 10 keV bin)')
plt.xlabel('Kinetic Energy (keV)')
plt.savefig('finale_log.png')

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