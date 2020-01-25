#!/usr/bin/env bash
for i in {2..4..2}
do
  ./constant.py -n $i >> data/$i&
done
