#!/usr/bin/env bash
mkdir data
for i in {0..479001600..1}
do
# rm data/$i
# echo $i&
# time ./constant.py -n $i&
# ./run.sh $i&
# ./constant.py -n $i >> data/$i&
./pairs.py -n $i&
done
