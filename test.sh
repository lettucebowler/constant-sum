#!/usr/bin/env bash
for i in {2..24..2}
do
./constant.py -n $i >> data/$i
done
