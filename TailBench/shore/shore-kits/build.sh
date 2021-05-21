#!/bin/bash

#run on mad6
./autogen.sh
./configure --enable-shore6 --enable-dbgsymbols SHORE_HOME=../shore-mt/
make -j32
