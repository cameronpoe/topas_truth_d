# this python script outputs TOPAS-formatted strings corresponding to weights of positrons at certain kinetic energies
# the equation comes from the non-relativistic treatment beta decay from Wu and Moszkowski

import math
import matplotlib.pyplot as plt

def spectrum_map(energy):
    coefficient = -1.54629E-13
    weight = (coefficient*((635. - energy)**2)*(energy**2))/(1-math.exp(((18*math.pi)/137)*(((2*energy)/511))**0.5))
    return weight


energy_string = ''
weight_string = ''
input_energy = 0
count = 0
total_weight = 0
tuple_list = []
while input_energy < 635:
    count += 1
    input_energy += 1
    energy_string += str(input_energy) + ' '
    weight_string += str(spectrum_map(input_energy)) + ' '
    total_weight += spectrum_map(input_energy)
    tuple_list.append((input_energy, spectrum_map(input_energy)))
energy_string = str(count) + ' ' + energy_string
weight_string = str(count) + ' ' + weight_string

f = open('beta_spectrum_strings.txt', 'w')
f.write(energy_string + '\n' + weight_string)
f.close()

print('Sum of all the recorded weights is: ' + str(total_weight))

plt.scatter(*zip(*tuple_list))
plt.show()