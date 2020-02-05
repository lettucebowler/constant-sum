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
    sumList = list()

    # Check each value in potentialSumList for validity as a constant sum
    # If valid, add it to sumList
    for g in potentialSumList:
        if g * p % n == n/2:
            sumList.append(g)

    return sorted(sumList)

print("0 MOD 8")
for q in range(1, n + 1):
    if q % 8 == 0:
        if q <= n // 2:
            print("p:" + str(q) + " " + str(findPossibleSums(n, q)))
        else:
            print("p:" + str(q) + " " + str(list()))

print("2 MOD 8")
for q in range(1, n + 1):
    if q % 8 == 2:
        if q <= n // 2:
            print("p:" + str(q) + " " + str(findPossibleSums(n, q)))
        else:
            print("p:" + str(q) + " " + str(list()))

print("4 MOD 8")
for q in range(1, n + 1):
    if q % 8 == 4:
        if q <= n // 2:
            print("p:" + str(q) + " " + str(findPossibleSums(n, q)))
        else:
            print("p:" + str(q) + " " + str(list()))

print("6 MOD 8")
for q in range(1, n + 1):
    if q % 8 == 6:
        if q <= n // 2:
            print("p:" + str(q) + " " + str(findPossibleSums(n, q)))
        else:
            print("p:" + str(q) + " " + str(list()))