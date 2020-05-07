#!/usr/bin/env bash
mkdir data
for i in {0..512..4}
do
./constant.py -n $i >> data/$i&
done
