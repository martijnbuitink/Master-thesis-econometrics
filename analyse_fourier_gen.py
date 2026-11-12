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
problem = {'num_vars': 4,
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


#X = fast_sampler.sample(problem, 64)

# Read results
result_gen10 = pd.read_csv(RESULTS / "First generations" / "result_mean_speed_y_gen10.csv")
result_gen20 = pd.read_csv(RESULTS / "First generations" / "result_mean_speed_y_gen20.csv")
result_gen30 = pd.read_csv(RESULTS / "First generations" / "result_mean_speed_y_gen30.csv")

#result_gen10 = pd.read_csv(RESULTS / "First generations" / "result_measure_gen10.csv")
#result_gen20 = pd.read_csv(RESULTS / "First generations" / "result_measure_gen20.csv")
#result_gen30 = pd.read_csv(RESULTS / "First generations" / "result_measure_gen30.csv")


result_gen10['Generations'] = 10
result_gen20['Generations'] = 20
result_gen30['Generations'] = 30


#Y10 = result_gen10['mean_pop_diversity']
#Y20 = result_gen20['mean_pop_diversity']
#Y30 = result_gen30['mean_pop_diversity']

Y10 = result_gen10['mean_speed_y']
Y20 = result_gen20['mean_speed_y']
Y30 = result_gen30['mean_speed_y']

Y10 = Y10.to_numpy()
Y20 = Y20.to_numpy()
Y30 = Y30.to_numpy()


Si10 = fast.analyze(problem, Y10, print_to_console=False)
Si20 = fast.analyze(problem, Y20, print_to_console=False)
Si30 = fast.analyze(problem, Y30, print_to_console=False)



# Si – Sa : Uncorrelated contribution of a term # ST : Total contribution of a particular dimension/parameter

Si = Si30

# import libraries
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "Results"

total = {'parameter': ['population_size', 'offspring_size', 'parent_selection', 'survivor_selection'], 'interaction': Si["ST"]} 
total = pd.DataFrame(data=total)

inter = {'parameter': ['population_size', 'offspring_size', 'parent_selection', 'survivor_selection'], 'main': Si["S1"]} 
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
plt.legend(handles=[top_bar, bottom_bar], loc=(0.01, 0.88))

#Set ylim
plt.ylim(0,1)
plt.ylabel('Effect')
plt.xlabel('Parameter')

# show the graph
plt.show()


import matplotlib.cm as cm
import matplotlib.pyplot as plt

def transpose_data(S1, ST):
    result = []
    for i in range(0, len(ST)):
        result.append([S1[i], ST[i]-S1[i]])
    return result

df10 = pd.DataFrame(transpose_data(Si10["S1"], Si10["ST"]),
                   index=["population_size", "offspring_size", "parent_selection", "survivor_selection"],
                   columns=["main", "interaction"])
df20 = pd.DataFrame(transpose_data(Si20["S1"], Si20["ST"]),
                   index=["population_size", "offspring_size", "parent_selection", "survivor_selection"],
                   columns=["main", "interaction"])
df30 = pd.DataFrame(transpose_data(Si30["S1"], Si30["ST"]),
                   index=["population_size", "offspring_size", "parent_selection", "survivor_selection"],
                   columns=["main", "interaction"])

dfall = [df10, df20, df30]
labels = ["10", "20", "30"]
title = "multiple stacked bar plot"
H = "/"

n_df = len(dfall)
n_col = len(dfall[0].columns)
n_ind = len(dfall[0].index)

# set the figure size
plt.figure(figsize=(8, 6))

axe = plt.subplot(111)



for df in dfall : # for each data frame
    axe = df.plot(kind="bar",
                  linewidth=0,
                  stacked=True,
                  ax=axe,
                  legend=False,
                  grid=False,
                  color=['darkblue','lightblue'])  # make bar plots

h,l = axe.get_legend_handles_labels() # get the handles we want to modify 
for i in range(0, n_df * n_col, n_col): # len(h) = n_col * n_df
    for j, pa in enumerate(h[i:i+n_col]):
        for rect in pa.patches: # for each index
            rect.set_x(rect.get_x() + 1 / float(n_df + 1) * i / float(n_col))
            rect.set_hatch(H * int(i / n_col)) #edited part
            rect.set_width(1 / float(n_df + 1))

axe.set_xticks((np.arange(0, 2 * n_ind, 2) + 1 / float(n_df + 1)) / 2.) 
axe.set_xticklabels(df.index, rotation = 0)

# Add invisible data to add another legend 
n=[]
for i in range(n_df):
    n.append(axe.bar(0, 0, color="gray", hatch=H * i))

l1 = axe.legend(h[:n_col], l[:n_col], loc=[1.01, 0.5]) 
if labels is not None:
    l2 = plt.legend(n, labels, loc=[1.01, 0.1])
axe.add_artist(l1)


#Set ylim
plt.ylim(0,1)
plt.ylabel('Effect')
plt.xlabel('Parameter')


plt.savefig(RESULTS / "Thesis_mean_speed_y_10_20_30.pdf", format='pdf', bbox_inches='tight')
