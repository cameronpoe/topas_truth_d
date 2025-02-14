# uses TruthTuple data to construct a plot of annihilation energy at annihilation and distance from start at annihilation

#from config.definitions import ROOT_DIR
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

SMALL_SIZE = 10
MEDIUM_SIZE = 12
LABEL_SIZE = 14.0
TICK_SIZE = 10.5
BIGGER_SIZE = 15

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=LABEL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=TICK_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=TICK_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=MEDIUM_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)


tup_file = open('50kPositronData/TruthTuple.phsp', 'r')
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
ax1.hist(data['starte'], range=(0.0, 635.0), bins=127, density=True, label='50,000 $e^+$ in\n5.0 keV bins')
x = np.linspace(0.25, 635.0, 2539)
def y(x):
    return ((-1.54629e-13)*((635.0-x)**2)*(x**2))/(1.0-math.exp(((18.0*math.pi)/137.0)*math.sqrt((2.0*x)/511.0)))
y2 = np.vectorize(y)
ax1.plot(x, y2(x), 'r', label='$^1$$^8$F K.E. Function,\nLevin (1999)')
plt.margins(x=0.0)
plt.suptitle('Probability Density of Kinetic Energies at Decay in the XCAT Brain', wrap=True)
plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
plt.legend(loc='upper right')
plt.xticks()
plt.minorticks_on()
plt.ylabel('Probability (1/keV)')
plt.xlim((0.0, 650.0))
plt.ylim((0.0, 0.004))
plt.xlabel('Kinetic Energy (keV)')
plt.savefig('starte-v2.2.png')

# plots figure 3, histogram of absolute distances from decay point
plt.figure(3)
fig3, ax3 = plt.subplots()
ax3.hist(data["diste"].multiply(10.0), range=(0.0, 2.5), bins=50, density=True, label='50,000 $e^+$ in\n0.05 mm bins')
plt.margins(x=0.0)
plt.title('Probability Density of Absolute Distances from Decay Point to Annihilation Point in the XCAT Brain', wrap=True)
plt.legend(loc='upper right')
plt.xticks()
plt.minorticks_on()
plt.ylabel('Probability (1/keV)')
plt.xlabel('Distance (mm)')
plt.savefig('absdist-v2.2.png')

plt.figure(4)
fig4, ax4 = plt.subplots()
weights4 = np.ones_like(data['xdist']) / len(data['xdist'])
ax4.hist(data["xdist"].multiply(10.0), range=(-2.0, 2.0), bins=80, label='50,000 $e^+$ in\n0.05 mm bins', weights=weights4)
plt.title('Probability of Distances along X-axis from Decay Point to Annihilation Point in the XCAT Brain', wrap=True)
plt.legend(loc='upper right')
plt.xticks()
plt.yticks()
plt.minorticks_on()
plt.ylabel('Probability (per 0.05 mm bin)')
plt.xlabel('Distance (mm)')
plt.savefig('xdist-v2.2.png')

plt.figure(2)
fig2, ax2 = plt.subplots()
weights2 = np.ones_like(data['finale']) / len(data['finale'])
ax2.hist(data['finale'], range=(0.0, 560.0), bins=56, label='50,000 $e^+$ in\n10 keV bins', weights=weights2)
ax2.annotate('49,588 $e^+$ at <10 keV', xy = (15, 0.1), 
             fontsize = 11, xytext = (100, 0.2), 
             arrowprops = dict(facecolor = 'black', width=1),
             color = 'black')
plt.margins(x=0.0)
plt.title('Probability of Kinetic Energies at Annihilation Point in the XCAT Brain', wrap=True)
plt.legend(loc='upper right')
plt.yscale('log')
plt.xticks()
plt.minorticks_on()
plt.ylabel('Probability (per 10 keV bin)')
plt.xlabel('Kinetic Energy (keV)')
plt.savefig('finale_log-v2.2.png')

f = open('README_annihilation_spectrum.txt', 'w')

f.write('Number of positrons: %s\n'%str(num_positrons))
f.write('Minimum non-zero values of the columns: %s'%str(data.where(data.gt(0)).min(0)))
f.write('Maximum annihilation energy: %s keV at line %s\n'%(str(data['finale'].max()), str(data.loc[data['finale'].idxmax(), 'linenum'])))
f.write('Maximum absolute distance : %s\n'%str(data['diste'].max()))
f.write('Maximum distance in x direction: %s\n'%str(data['xdist'].max()))
f.write('Minimum distance in x direction: %s\n'%str(data['xdist'].min()))
f.write('Number of positrons with non-zero difference between final energy and final energy deposited: %s\n'%str(non_zero_diff))


f.write('\n\nUsing Pandas Dataframe queries:\n')
f.write('Number of identically zero final energies: %s\n'%data.query('finale == 0.0')['finale'].count())
f.write('Number of final energies less than 10 keV: %s\n'%data.query('finale < 10')['finale'].count())

tup_file.close()
f.close()