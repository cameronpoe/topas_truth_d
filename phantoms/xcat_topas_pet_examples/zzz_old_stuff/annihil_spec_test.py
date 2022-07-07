import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from random import seed
from random import randint

import seaborn as sns

data = pd.DataFrame(columns=['Col1'])

i = 0
while i < 495:
    data.loc[len(data.index)] = [0]
    i += 1

seed(1)
j = 0
while j < 5:
    data.loc[len(data.index)] = [randint(1,500)]
    j += 1

plt.figure(2)
fig2, ax2 = plt.subplots()
weights = np.ones_like(data['Col1']) / len(data['Col1'])
ax2.hist(data['Col1'], range=(0.0, 500.0), weights=weights, bins=50, label='500 numbers\n in 10 unit bins')
plt.title('Probability Density of Some Numbers from 0 to 500', wrap=True)

plt.text(2, 3, '49584 $e^+$ at <10 keV')
ax2.annotate('49584 $e^+$ at <10 keV', xy = (15, 0.1), 
             fontsize = 11, xytext = (100, 0.2), 
             arrowprops = dict(facecolor = 'black', width=1),
             color = 'black')
plt.legend(loc='upper right')
plt.yscale('log')
plt.xticks()
plt.minorticks_on()
plt.ylabel('Probability')
plt.xlabel('Number')
plt.savefig('randnum.png')

#sns.histplot(data['Col1'], stat='probability', bins=50, binrange=(0.0, 500.0))