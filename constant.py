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
    total = 0
    for x in part:
        total += x
    groupList = list()
    group = list()
    numList = list(range(1, total + 1))
    if len(part) == 1:
        group = list(range(1, total+1))
        groupList.append(group)
    else:
        for y in range(total):
            del group
            group = list()
            groupList.append(group)
            if (g + y) % total in numList and total - y in numList and g + y != total - y:
                if y < len(part):
                    if len(groupList[y]) == 0 and g + y < (g + total) / 2:
                        groupList[y].append((g + y) % total)
                        groupList[y].append(total - y)

            groupList = groupList[:len(part)]
            for get in groupList:
                if len(get) == 0:
                    temp = numList[0]
                    get.append(temp)
                    get.append(g - temp)
                    numList.remove(temp)
                    numList.remove(g - temp)

        for set in groupList:
            for item in set:
                if item in numList:
                    numList.remove(item)
    # print(str(numList))

        for z in range(len(groupList)):
            if part[z] > 2:
                group = groupList[z]
                for h in numList:
                    if len(group) < part[z]:
                        if (total - h) in numList and (total - h) != h:
                            # print(str(h) + " " + str(total - h) + " " + str(numList))
                            group.append(h)
                            group.append(total - h)
                            numList.remove(h)
                            numList.remove(total - h)
                        if z == len(groupList) - 1:
                            for b in numList:
                                groupList[z].append(b)
            # for q in range((part[z] - 2) // 2):
            #     temp = numList[0]
            #     groupList[z].append(temp)
            #     groupList[z].append(total - temp)
            #     numList.remove(temp)
    checkSet = list()
    for k in groupList:
        k.sort()
        for l in k:
            if l not in checkSet:
                checkSet.append(l)
            else:
                del groupList
                groupList = list()
        G = sum(k)
        if G % total != g:
            del groupList
            groupList = list()
    groupList.sort(key=len)
    return groupList

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
csp = list()
count = 0
for part in partList:
    del sumList
    sumList = findPossibleSums(n, part)
    for possibleSum in sumList:
        csp = list(genConstantSumPartition(part, possibleSum))
        if len(csp) > 0:
            print("n:" + str(n) + " p:" + str(len(part)) + " part:" + str(part)
            + " csp:" + str(csp) + " sum:" + str(possibleSum))
        else:
            print("Algorithm Failure")
            exit()
