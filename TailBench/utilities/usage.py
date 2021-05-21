import numpy as np
#import plotly.graph_objects as go
#from plotly.offline import plot
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
#import plotly.express as px
import sys
import time
import os
import shutil
#import seaborn as sns

appThreads = {'img-dnn':2, 'masstree':3, 'silo':3}

files = [i for i in os.listdir('.') if i.endswith('.txt')]

final_data = dict()

for filename in files:
    with open(filename) as f:
        content = f.read().strip().split('\n')
        data = dict()
        for line in content:
            tmp = line.split()
            if tmp[0] not in data:
                data[tmp[0]] = {'cpu':[], 'ram':[]}
            data[tmp[0]]['cpu'].append(float(tmp[8]))
            data[tmp[0]]['ram'].append(float(tmp[9]))
    final_data[filename] = data
        

#per config, plot cpu for all threads on same plot, plot ram for all on same
    
count = len(final_data)
for ctr, config in enumerate(final_data):
    print(f"{ctr+1}/{count}")
    threads = list(final_data[config].keys())
    fig, axes = plt.subplots(ncols=2, nrows=1, figsize = (12, 5))
    axes[0].set_xlabel("Time Intervals (3 sec)")
    axes[0].set_ylabel("CPU Usage (%)")
    axes[1].set_xlabel("Time Intervals (3 sec)")
    axes[1].set_ylabel("RAM Usage (%)")
    axes[0].set_title("CPU Usage for {}".format(config[:-4]))
    axes[1].set_title("RAM Usage for {}".format(config[:-4]))
    for thread_num, thread in enumerate(threads):
        cpu = final_data[config][thread]["cpu"]
        ram = final_data[config][thread]["ram"]
        cpu.insert(0, 0.0)
        ram.insert(0, 0.0)
        cpu = np.asarray(cpu, dtype = 'float')
        ram = np.asarray(ram, dtype = 'float')
        axes[0].plot(range(len(cpu)), cpu, label = "Thread "+str(thread_num+1))
        axes[1].plot(range(len(ram)), ram, label = "Thread "+str(thread_num+1))
        axes[0].legend()
        axes[1].legend()
    fig.savefig("Plots/{}.png".format(config[:-4]), dpi = 1000)
        