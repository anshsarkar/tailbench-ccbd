#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source ${DIR}/../configs.sh

THREADS=1
QPS=100
WARMUPREQS=500
MAXREQS=500

BIN=./bin/moses_integrated

cp moses.ini.template moses.ini
sed -i -e "s#@DATA_ROOT#$DATA_ROOT#g" moses.ini

TBENCH_QPS=${QPS} TBENCH_MAXREQS=${MAXREQS} TBENCH_WARMUPREQS=${WARMUPREQS} \
    TBENCH_MINSLEEPNS=10000 chrt -r 99 ${BIN} -config ./moses.ini \
    -input-file ${DATA_ROOT}/moses/testTerms \
    -threads ${THREADS} -num-tasks 100000 -verbose 0
