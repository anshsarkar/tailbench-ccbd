#!/bin/sh

sudo find ../../TailBench/ -type f -iname "*.sh" -exec chmod +x {} \;
sudo find ../../TailBench/ -type f -not -regex ".*\..*" -exec chmod +x {} \;
sudo find ../../TailBench/ -type f -iname "*.*" -exec chmod +x {} \;