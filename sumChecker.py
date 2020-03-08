#!/usr/bin/env python3
import os;
import sys
import subprocess;
import argparse
import itertools
import math
import random

# Parser to get base number for computations
parser = argparse.ArgumentParser(description='A parser')
parser.add_argument("-n", dest='number', default=2, help='number to partition', type=int)
args = parser.parse_args();
n = args.number

def findPossibleSums(n, p):
    potentialSumList = list(range(1, n))
    return sorted(sum for sum in potentialSumList if sum * p % n == n // 2)

for i in range(0, 8, 2):
    print(str(i) + " MOD 8")
    for q in range(1, n + 1):
        if q % 8 == i:
            if q <= n // 2:
                print("p:" + str(q) + " " + str(findPossibleSums(n, q)))
            else:
                print("p:" + str(q) + " " + str(list()))
