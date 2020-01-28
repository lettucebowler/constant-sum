#!/usr/bin/env bash
for i in {2..48..2}
do
rm data/$i
./constant.py -n $i >> data/$i
done
