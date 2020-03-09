#!/usr/bin/env bash
mkdir data
# for i in {0..479001600..1}
for i in {0..64..4}
do
# rm data/$i
# echo $i&
./constant.py -n $i | grep duplicate
# ./run.sh $i&
# ./constant.py -n $i >> data/$i&
done
