#!/usr/bin/env bash
# mkdir data
for i in {2..128..2}
do
# rm data/$i
# echo $i&
# time ./constant.py -n $i&
./run.sh $i
# ./constant.py -n $i >> data/$i&
done
