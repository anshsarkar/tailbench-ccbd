#!/bin/bash
# ops-per-worker is set to a very large value, so that TBENCH_MAXREQS controls how
# many ops are performed
NUM_WAREHOUSES=1
NUM_THREADS=1

QPS=2000
MAXREQS=20000
WARMUPREQS=20000

TBENCH_QPS=${QPS} TBENCH_MAXREQS=${MAXREQS} TBENCH_WARMUPREQS=${WARMUPREQS} \
    TBENCH_MINSLEEPNS=10000 chrt -r 99 \
    ./out-perf.masstree/benchmarks/dbtest_integrated --verbose \
    --bench tpcc --num-threads ${NUM_THREADS} --scale-factor ${NUM_WAREHOUSES} \
    --retry-aborted-transactions --ops-per-worker 10000000
