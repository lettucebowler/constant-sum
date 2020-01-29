#!/usr/bin/env bash
for i in {2..128..2}
do
rm data/$i
./constant.py -n $i >> data/$i&
done
