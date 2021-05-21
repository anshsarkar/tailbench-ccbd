import sys
import os
import time
import numpy as np
from scipy import stats
from psutil import virtual_memory
import multiprocessing

mem = virtual_memory()
mem = round(mem.total/1024**3)
cpu = multiprocessing.cpu_count()

paths = [r"../img-dnn/lats.bin", r"../masstree/lats.bin", r"../silo/lats.bin", r"../specjbb/lats.bin", r"../sphinx/lats.bin"]
buildStatements = [r"(cd ../harness/ ; sudo ./build.sh)", r"(cd ../ ; sudo ./build.sh harness)",r"(cd ../img-dnn/ ; sudo ./build.sh)", r"(cd ../masstree/ ; sudo ./build.sh)", r"(cd ../silo/ ; sudo ./build.sh)", r"(cd ../specjbb/ ; sudo ./build.sh)", r"(cd ../sphinx/ ; sudo ./build.sh)"]
executeStatements = [r"(cd ../img-dnn/ ; sudo ./run.sh)", r"(cd ../masstree/ ; sudo ./run.sh)", r"(cd ../silo/ ; sudo ./run.sh)", r"(cd ../specjbb/ ; sudo ./run.sh)",  r"(cd ../sphinx/ ; sudo ./run.sh)"]
#executeStatement = r"(cd ../{}/ ; sudo ./run.sh > {}.txt)"
loadStatement = r"sudo stress --cpu {} -m {} --vm-bytes {}M &"
kill = r"sudo pkill -9 stress"


class Lat:
    def __init__(self, fileName):
        f = open(fileName, 'rb')
        a = np.fromfile(f, dtype=np.uint64)
        self.reqTimes = a.reshape((a.shape[0]/3, 3))
        f.close()

    def parseQueueTimes(self):
        return self.reqTimes[:, 0]

    def parseSvcTimes(self):
        return self.reqTimes[:, 1]

    def parseSojournTimes(self):
        return self.reqTimes[:, 2]

def getLatPct(latsFile, load_cpu, load_proc, load_mem):
    assert os.path.exists(latsFile)

    latsObj = Lat(latsFile)
    temp_cpu = multiprocessing.cpu_count()
    qTimes = [l/1e6 for l in latsObj.parseQueueTimes()]
    svcTimes = [l/1e6 for l in latsObj.parseSvcTimes()]
    sjrnTimes = [l/1e6 for l in latsObj.parseSojournTimes()]
    f = open('lats-{}-{}-{}-{}-{}-{}.txt'.format(latsFile[3:-9], temp_cpu, mem, load_cpu, load_proc, load_mem),'w')
    f.write('%12s | %12s | %12s\n\n' \
            % ('QueueTimes', 'ServiceTimes', 'SojournTimes'))

    for (q, svc, sjrn) in zip(qTimes, svcTimes, sjrnTimes):
        f.write("%12s | %12s | %12s\n" \
                % ('%.3f' % q, '%.3f' % svc, '%.3f' % sjrn))
    f.close()

    f = open('{}-{}-{}-{}-{}-{}.txt'.format(latsFile[3:-9], temp_cpu, mem, load_cpu, load_proc, load_mem),'w')
    for i in sjrnTimes:
        f.write('%.3f\n' % i)
    f.close()

    p95 = stats.scoreatpercentile(sjrnTimes, 95)
    maxLat = max(sjrnTimes)
    print "95th percentile latency %.3f ms | max latency %.3f ms" \
            % (p95, maxLat)
    
def build():
    print("Building...")
    for e in buildStatements:
        print(e)
        os.system(e)

def run():
    os.system(kill)
    for i in range(1, cpu+1):
        for j in range(1, 11):
            for k in range(1, mem+1):
                print("Generating load...")
                load = loadStatement.format(i, j, k*1024)
                os.system(load)
                print(load)
                print("Executing...")
                for ex in executeStatements:
                    print(ex)
                    os.system(ex)
                generate(i, j, k*1024)
                os.system(kill)
                print("Killing load...")

def generate(load_cpu, load_proc, load_mem):
    print("Generating Output Files...")
    for p in paths:
        print(p)
        latsFile = p
        getLatPct(latsFile, load_cpu, load_proc, load_mem)

params = sys.argv[1:] #-b build, -e execute run.sh with application
params.sort()
for parameter in params:
    if parameter == '-b':
        build()
    if parameter == '-e':
        run()