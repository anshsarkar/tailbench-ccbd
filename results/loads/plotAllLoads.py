import os, shutil
import numpy as np
import matplotlib.pyplot as plt

files = [os.path.join(os.path.abspath("less_data"), i) for i in os.listdir("less_data") if i.endswith(".txt") and not i.startswith("lat")]

PER = 95    # Set to 100 for max latency, 95 for 95th

data = dict()
for fname in files:
    with open(fname) as f:
        values = [float(i) for i in f.read().strip().split()]
        data[fname] = np.percentile(np.asarray(values), PER)
        
mem_var = dict()        
proc_var = dict()
cpu_var = dict()       
 
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
    
    load_cpu_proc = "{}_{}".format(load_cpu, load_proc)
    load_cpu_mem = "{}_{}".format(load_cpu, load_mem)
    load_mem_proc = "{}_{}".format(load_mem, load_proc)
    
    if app not in mem_var:
        mem_var[app] = dict()
    if load_cpu_proc not in mem_var[app]:
        mem_var[app][load_cpu_proc] = dict()
    mem_var[app][load_cpu_proc][load_mem] = y
    
    if app not in proc_var:
        proc_var[app] = dict()
    if load_cpu_mem not in proc_var[app]:
        proc_var[app][load_cpu_mem] = dict()
    proc_var[app][load_cpu_mem][load_proc] = y
    
    if app not in cpu_var:
        cpu_var[app] = dict()
    if load_mem_proc not in cpu_var[app]:
        cpu_var[app][load_mem_proc] = dict()
    cpu_var[app][load_mem_proc][load_cpu] = y
    
for app in mem_var:
    try:
        shutil.rmtree("Plots/Cores - Processes - Memory/{}".format(app))
    except:
        pass
    os.mkdir("Plots/Cores - Processes - Memory/{}".format(app))
    os.mkdir("Plots/Cores - Processes - Memory/{}/{}".format(app, "Variable Memory"))
    os.mkdir("Plots/Cores - Processes - Memory/{}/{}".format(app, "Variable Cores"))
    os.mkdir("Plots/Cores - Processes - Memory/{}/{}".format(app, "Variable Processes"))
    
    
for app in mem_var:
    print(app)
    for config in mem_var[app]:
        cores, processes = config.split("_")
        plt.figure()
        plt.xlabel("Memory per Process (GB)")
        plt.ylabel("{}th Percentile Latency (ms)".format(PER))
        plt.title("{} - {} Cores - {} Processes".format(app, cores, processes))
        X = np.array(list(mem_var[app][config].keys()))
        y = np.array(list(mem_var[app][config].values()))
        order = np.argsort(X)
        X = X[order]
        y = y[order]
        X = X.astype(str)
        plt.bar(X, y, width = 0.5, color = 'maroon')
        plt.savefig("Plots/Cores - Processes - Memory/{}/Variable Memory/{} - {} Cores - {} Processes".format(app, app, cores, processes), dpi = 1000)
        plt.close()
        
for app in proc_var:
    print(app)
    for config in proc_var[app]:
        cores, memory = config.split("_")
        plt.figure()
        plt.xlabel("Number of Processes")
        plt.ylabel("{}th Percentile Latency (ms)".format(PER))
        plt.title("{} - {} Cores - {} GB Memory".format(app, cores, memory))
        X = np.array(list(proc_var[app][config].keys()))
        y = np.array(list(proc_var[app][config].values()))
        order = np.argsort(X)
        X = X[order]
        y = y[order]
        X = X.astype(str)
        plt.bar(X, y, width = 0.5, color = 'maroon')
        plt.savefig("Plots/Cores - Processes - Memory/{}/Variable Processes/{} - {} Cores - {} GB Memory".format(app, app, cores, memory), dpi = 1000)
        plt.close()
        
for app in cpu_var:
    print(app)
    for config in cpu_var[app]:
        memory, processes = config.split("_")
        plt.figure()
        plt.xlabel("Number of Cores")
        plt.ylabel("{}th Percentile Latency (ms)".format(PER))
        plt.title("{} - {} GB Memory - {} Processes".format(app, memory, processes))
        X = np.array(list(cpu_var[app][config].keys()))
        y = np.array(list(cpu_var[app][config].values()))
        order = np.argsort(X)
        X = X[order]
        y = y[order]
        X = X.astype(str)
        plt.bar(X, y, width = 0.5, color = 'maroon')
        plt.savefig("Plots/Cores - Processes - Memory/{}/Variable Cores/{} - {} GB Memory - {} Processes".format(app, app, memory, processes), dpi = 1000)
        plt.close()

