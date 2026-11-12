#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 20:27:24 2023

@author: Martijn
"""
from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib.sample import fast_sampler
from SALib.analyze import fast
from SALib.test_functions import Ishigami 
import numpy as np 
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "Results"

# Define problem
# Bounds are 0.5 above and below bound (later rounded to integers) 
problem = {'num_vars': 5,
           'names': ['population_size',
                     'offspring_size',
                     'num_generations',
                     'parent_selection',
                     'survivor_selection'],
           'bounds': [[49.5,200.5],
                      [49.5,100.5],
                      [49.5,200.5],
                      [1.5, 4.5],
                      [1.5, 4.5]],
           'dists': ['unif',
                     'unif',
                     'unif',
                     'unif',
                     'unif']
    }
# Plot average speed_y against generation

#X = fast_sampler.sample(problem, 64)

# Read results
#result = pd.read_csv(RESULTS / "With number of generations" / "result_mean_speed_y.csv")
result = pd.read_csv(RESULTS / "With number of generations" / "result_measure.csv")

Y = result['mean_pop_diversity']
#Y = result['mean_speed_y']
Y = Y.to_numpy()
Si = fast.analyze(problem, Y, print_to_console=False)

print(Si)

[0.6534006549067373, 0.06866589499313742, 7.795835867134887e-29] [1.1030936611314267e-30, 1.4447834927263737e-29, 0.05256232010089031]



# Si – Sa : Uncorrelated contribution of a term # ST : Total contribution of a particular dimension/parameter

# import libraries
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "Results"

total = {'parameter': ['population_size', 'offspring_size', 'num_generations', 'parent_selection', 'survivor_selection'], 'interaction': Si["ST"]}
total = pd.DataFrame(data=total)

inter = {'parameter': ['population_size', 'offspring_size', 'num_generations', 'parent_selection', 'survivor_selection'], 'main': Si["S1"]}
inter = pd.DataFrame(data=inter)

# set the figure size
plt.figure(figsize=(8, 6))

# set plot style: grey grid in the background:
sns.set(style="darkgrid")

# bar chart 1 -> top bars (group of 'smoker=No')
bar1 = sns.barplot(x="parameter",  y="interaction", data=total, color='lightblue')

# bar chart 2 -> bottom bars (group of 'smoker=Yes')
bar2 = sns.barplot(x="parameter", y="main", data=inter, color='darkblue')

# add legend
top_bar = mpatches.Patch(color='lightblue', label='interaction')
bottom_bar = mpatches.Patch(color='darkblue', label='main')
#plt.legend(handles=[top_bar, bottom_bar], loc=(1.04, 0.5))
plt.legend(handles=[top_bar, bottom_bar], loc=(0.01, 0.88))

#Set ylim
plt.ylim(0,1)
plt.ylabel('Effect')
plt.xlabel('Parameter')

# show the graph
plt.savefig(RESULTS / "Thesis_measure_with_nr_gen.pdf", format='pdf')
plt.show()
