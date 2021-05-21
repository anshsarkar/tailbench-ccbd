import os
import numpy as np
import matplotlib.pyplot as plt

files = [os.path.join(os.path.abspath("TextFiles"), i) for i in os.listdir("TextFiles") if i.endswith(".txt") and not i.startswith("lat")]

PER = 95    # Set to 100 for max latency, 95 for 95th

data = dict()
for fname in files:
    with open(fname) as f:
        values = [float(i) for i in f.read().strip().split()]
        data[fname] = np.percentile(np.asarray(values), PER)
        
      
proc_const = dict()
cpu_const = dict()        

for config in data:
    y = data[config]
    fname = config.split(os.path.sep)[-1]
    fname = fname[:-4].split('-')
    #print(fname)
    if fname[0] == 'img':
        del fname[1]
        fname[0] = "img-dnn"
    app, cpu, mem, load_cpu, load_proc, load_mem = fname
    cpu = int(cpu)
    mem = int(float(mem))
    load_cpu = int(load_cpu)
    load_proc = int(load_proc)
    load_mem = int(load_mem)
    #print(app, cpu, mem, load_cpu, load_proc, load_mem)
    
    if app not in cpu_const:
        cpu_const[app] = dict()
    if load_cpu not in cpu_const[app]:
        cpu_const[app][load_cpu] = dict()
    cpu_const[app][load_cpu][load_proc] = y
    
    if app not in proc_const:
        proc_const[app] = dict()
    if load_proc not in proc_const[app]:
        proc_const[app][load_proc] = dict()
    proc_const[app][load_proc][load_cpu] = y
    
for app in cpu_const:
    print(app)
    plt.figure()
    plt.xlabel("Processes")
    plt.ylabel("{}th Percentile Latency (ms)".format(PER))
    plt.title(app)
    for cpu in cpu_const[app]:
        X = np.array(list(cpu_const[app][cpu].keys()))
        y = np.array(list(cpu_const[app][cpu].values()))
        order = np.argsort(X)
        X = X[order]
        y = y[order]
        plt.plot(X, y, label = cpu)
    plt.legend()
    plt.savefig("Plots/{}-Cores.png".format(app), dpi = 1000)


for app in proc_const:
    print(app)
    plt.figure()
    plt.xlabel("CPU Cores")
    plt.ylabel("{}th Percentile Latency (ms)".format(PER))
    plt.title(app)
    for proc in proc_const[app]:
        X = np.array(list(proc_const[app][proc].keys()))
        y = np.array(list(proc_const[app][proc].values()))
        order = np.argsort(X)
        X = X[order]
        y = y[order]
        plt.plot(X, y, label = proc)
    plt.legend()
    plt.savefig("Plots/{}-Processes.png".format(app), dpi = 1000)