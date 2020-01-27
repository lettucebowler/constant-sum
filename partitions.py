#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse
import itertools
import math

# Parser to get base number for computations
parser = argparse.ArgumentParser(description='A parser')
parser.add_argument("-n", dest='number', default=2, help='number to partition', type=int)
args = parser.parse_args();
n = args.number

def partition(number):
        a = [0 for i in range(number + 1)]
        k = 1
        a[1] = number
        while k != 0:
            x = a[k - 1] + 1
            y = a[k] - 1
            k -= 1
            while x <= y:
                a[k] = x
                y -= x
                k += 1
            a[k] = x + y
            isEven = True
            for g in a[:k+1]:
                if g % 2 != 0:
                    isEven = False
            # isEven=True
            if isEven == True:
                yield a[:k + 1]

partList = list()
for part in partition(n):
    if len(part) > 0:
    # if len(part) > 0:
        cur = part[0]
        isBad = False
        # isBad = True
        # for h in part:
        #     if h != cur:
        #         isBad = False
        # if(n/2 % 2 == 1):
        #     if len(part) % 2 == 0:
        #         isBad = True
        if isBad == False:
                partList.append(part)
partList.sort(key=len, reverse=True)
print(str(len(partList)))
# for wiggle in partList:
#     print(str(wiggle))
