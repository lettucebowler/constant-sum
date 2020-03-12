#!/usr/bin/env python3
import argparse
import operator
from math import gcd
from copy import deepcopy
from functools import reduce

# Parser to get base number for computations
parser = argparse.ArgumentParser(description='A parser')
parser.add_argument("-n", dest='number', default=2, type=int)
parser.add_argument("-p", dest='partitions', default=2, type=int)
args = parser.parse_args()
n = args.number
p = args.partitions

def findSums(n, p):
    return sorted(sum for sum in range(1, n) if sum * p % n == n // 2)

def get_order(n, t):
    return n * t // gcd(n, t) // t

sums = findSums(n, p)
print("{}".format(get_order(n, sums[0])))