#!/usr/bin/env bash
for i in {0..128..4}
do
./constant.py -n $i&
done
