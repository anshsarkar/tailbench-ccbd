#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source ${DIR}/../configs.sh

THREADS=1
AUDIO_SAMPLES='audio_samples'

LD_LIBRARY_PATH=./sphinx-install/lib:${LD_LIBRARY_PATH} \
    TBENCH_QPS=1 TBENCH_MAXREQS=10 TBENCH_WARMUPREQS=10 TBENCH_MINSLEEPNS=10000 TBENCH_RANDSEED=$RANDOM\
    TBENCH_AN4_CORPUS=${DATA_ROOT}/sphinx TBENCH_AUDIO_SAMPLES=${AUDIO_SAMPLES} \
    ./decoder_integrated -t $THREADS
