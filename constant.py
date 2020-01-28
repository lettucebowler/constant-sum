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

# Returns a list of all partitions of number, made up of only even numbers.
# If number is odd, returns an empty set.
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
            if isEven == True:
                yield a[:k + 1]

# n : number program is checking
# part : partition of n to check for potential sums
def findPossibleSums(n, part):
    p = len(part)
    potentialSumList = list(range(1, n))
    sumList = list()

    for g in potentialSumList:
        if g * p % n == n/2:
            sumList.append(g)
    return sorted(sumList)

# Create a random constant-sum-partition from supplied partition
def genConstantSumPartition(part, g):
    groupList = list()
    group = list()
    total = 0
    for x in part:
        total += x

    numList = list(range(1, total + 1))
    for y in range(total):
        del group
        group = list()
        groupList.append(group)
        if (g + y) % total in numList and total - y in numList and g + y != total - y:
            if y < len(part):
                if len(groupList[y]) == 0 and g + y < (g + total) / 2:
                    groupList[y].append((g + y) % total)
                    groupList[y].append(total - y)

    for set in groupList:
        for item in set:
            if item in numList:
                numList.remove(item)

    groupList = groupList[:len(part)]
    for get in groupList:
        if len(get) == 0:
            get.append(numList[0])
            get.append(g - numList[0])

    for z in range(len(groupList)):
        if part[z] > 2:
            for q in range((part[z] - 2) // 2):
                temp = numList[0]
                groupList[z].append(temp)
                groupList[z].append(total - temp)
                numList.remove(temp)

    for k in groupList:
        k.sort()

    return sorted(groupList)

# class csp():
#     def __init__(self, base, partNum, sum, part, perm):
#         self.base = base
#         self.partNum = partNum
#         self.sum = sum
#         self.part = part
#         self.perm = perm
#
#     def to_string(self):
#         return("p=" + str(self.partNum) + ", g=" + str(self.sum) + ", part=" + str(self.part) + ", group=" + str(self.perm))

# ----------------------------Main Program------------------------------------ #
partList = list()

# Exit if n is odd.
if n % 2 == 1:
    print("This program is only designed for even numbers.")
    exit()

# Populate partition list and filter out irrelevant partitions.
for part in partition(n):
    partList.append(part)
partList.sort(reverse=True, key=len)

# Print partition and possible sums
sumList = list()
count = 0
for part in partList:
    del sumList
    sumList = findPossibleSums(n, part)
    # print(str(part) + " : " + str(sumList))
    for sum in sumList:
        print("n:" + str(n) + " p:" + str(len(part)) + " part:" + str(part)
        + " csp:" + str(list(genConstantSumPartition(part, sum))) + " sum:" + str(sum))
