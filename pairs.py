#!/usr/bin/env python3
import argparse
import math

# Parser to get base number for computations
parser = argparse.ArgumentParser(description='A parser')
parser.add_argument("-n", dest='number', default=2, \
    help='number to partition', type=int)
args = parser.parse_args()
n = args.number

check = [5, 6, 7, 17, 18, 19]
nums = [2, 3, 4, 8, 9, 10, 14, 15, 16, 20, 21, 22]
# nums = [1, 2]
nums.sort()
nPerm = []
nooms = [g for g in nums]
# test the xth permutation of nums
for y in range(len(nums)):
    q = n // math.factorial(len(nooms) - 1) % len(nooms)
    nPerm.append(nooms.pop(q))
bad = False
for z in range(0, len(nums), 2):
    if nPerm[z] + nPerm[z + 1] != check[z // 2]:
        bad = True
        break
if bad == False:
    print(str(nPerm))
