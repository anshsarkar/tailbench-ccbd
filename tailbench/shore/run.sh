#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source ${DIR}/../configs.sh

THREADS=1
QPS=400
WARMUPREQS=10000
MAXREQS=2000

DUMMYREQS=1000000 # set this really high so MAXREQS controls execution

# Point this to an appropriate location on your system
SCRATCH_DIR=/doesnotexist

BIN="shore-kits/shore_kits_integrated"

# Setup
TMP=$(mktemp -d --tmpdir=${SCRATCH_DIR})
ln -s $TMP scratch
mkdir scratch/log && ln -s scratch/log log
mkdir scratch/diskrw && ln -s scratch/diskrw diskrw

cp ${DATA_ROOT}/shore/db-tpcc-1 scratch/ && \
    ln -s scratch/db-tpcc-1 db-tpcc-1
chmod 644 scratch/db-tpcc-1

cp shore-kits/run-templates/cmdfile.template cmdfile
sed -i -e "s#@NTHREADS#$THREADS#g" cmdfile
sed -i -e "s#@REQS#$DUMMYREQS#g" cmdfile

cp shore-kits/run-templates/shore.conf.template \
    shore.conf
sed -i -e "s#@NTHREADS#$THREADS#g" shore.conf

# Run app
TBENCH_QPS=${QPS} TBENCH_MAXREQS=${MAXREQS} TBENCH_WARMUPREQS=${WARMUPREQS} \
    TBENCH_MINSLEEPNS=10000 chrt -r 99 ${BIN} -i cmdfile

# Cleanup
rm -f log scratch cmdfile db-tpcc-1 diskrw shore.conf info

../utilities/parselats.py ./lats.bin

mv lats.bin lats.int.bin
mv lats.txt lats.int.txt
