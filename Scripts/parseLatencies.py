import sys
import os
from psutil import virtual_memory
import multiprocessing
import numpy as np
from scipy import stats

mem = virtual_memory()
ram = round(mem.total/1024**3)
cpu = multiprocessing.cpu_count()

paths = [r"../img-dnn/lats.bin", r"../masstree/lats.bin",
         r"../silo/lats.bin", r"../specjbb/lats.bin", r"../sphinx/lats.bin"]
buildStatements = [r"(cd ../harness/ ; sudo ./build.sh)", r"(cd ../ ; sudo ./build.sh harness)", r"(cd ../img-dnn/ ; sudo ./build.sh)",
                   r"(cd ../masstree/ ; sudo ./build.sh)", r"(cd ../silo/ ; sudo ./build.sh)", r"(cd ../specjbb/ ; sudo ./build.sh)", r"(cd ../sphinx/ ; sudo ./build.sh)"]
#executeStatements = [r"(cd ../img-dnn/ ; sudo ./run.sh)", r"(cd ../masstree/ ; sudo ./run.sh)", r"(cd ../silo/ ; sudo ./run.sh)", r"(cd ../specjbb/ ; sudo ./run.sh)",  r"(cd ../sphinx/ ; sudo ./run.sh)"]
executeStatement = r"(cd ../{}/ ; sudo ./run.sh > {}.txt)"
coreOffStatements = [
    r"echo 0 | sudo tee /sys/devices/system/cpu/cpu{}/online".format(i) for i in range(cpu)]
coreOnStatements = [
    r"echo 1 | sudo tee /sys/devices/system/cpu/cpu{}/online".format(i) for i in range(cpu)]


class Lat(object):
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


def getLatPct(latsFile):
    assert os.path.exists(latsFile)

    latsObj = Lat(latsFile)
    temp_cpu = multiprocessing.cpu_count()
    qTimes = [l/1e6 for l in latsObj.parseQueueTimes()]
    svcTimes = [l/1e6 for l in latsObj.parseSvcTimes()]
    sjrnTimes = [l/1e6 for l in latsObj.parseSojournTimes()]
    f = open('lats-{}-{}-{}.txt'.format(latsFile[3:-9], temp_cpu, ram), 'w')
    f.write('%12s | %12s | %12s\n\n'
            % ('QueueTimes', 'ServiceTimes', 'SojournTimes'))

    for (q, svc, sjrn) in zip(qTimes, svcTimes, sjrnTimes):
        f.write("%12s | %12s | %12s\n"
                % ('%.3f' % q, '%.3f' % svc, '%.3f' % sjrn))
    f.close()

    f = open('{}-{}-{}.txt'.format(latsFile[3:-9], temp_cpu, ram), 'w')
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
    print("Executing...")
    for e in coreOnStatements:
        os.system(e)
    ctr = cpu

    '''while ctr>=1:
        print ctr,"cores..."
        for e in executeStatements:
            print(e)
            os.system(e)
        generate()
        os.system(coreOffStatements[ctr-1])
        os.system(coreOffStatements[ctr-2])
        os.system(coreOffStatements[ctr-3])
        os.system(coreOffStatements[ctr-4])
        ctr-=4'''

    params = sys.argv[1:]
    params.sort()
    applications = params[params.index('-e')+1:]
    for app in applications:
        while ctr >= 1:
            print ctr, "cores..."
            runStatement = executeStatement.format(
                app, app+'-'+str(ctr)+'-'+str(ram))
            print(runStatement)
            time.sleep(15)
            os.system(runStatement)
            generate()
            os.system(coreOffStatements[ctr-1])
            os.system(coreOffStatements[ctr-2])
            os.system(coreOffStatements[ctr-3])
            os.system(coreOffStatements[ctr-4])
            ctr -= 4

    for e in coreOnStatements:
        os.system(e)


def generate():
    print("Generating Output Files...")
    for p in paths:
        print(p)
        latsFile = p
        getLatPct(latsFile)


params = sys.argv[1:]  # -b build, -e execute run.sh, -o generate output
params.sort()
for parameter in params:
    if parameter == '-b':
        build()
    if parameter == '-e':
        run()
    if parameter == "-o":
        generate()
