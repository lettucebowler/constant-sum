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
    # print("Total : "+ str(total))
    p = len(part)
    numList = list(range(1, total + 1))
    group = list()
    groupList = list()
    if p % 2 == 0 and total % 4 == 2:
        return groupList
    # if g == 2:
    #     numList.remove(1)
    groupIndex = 0
    for groupIndex in range(len(part)):
        print("group : " + str(groupIndex) + " " + str(g))
        print("half : " + str((total + g) // 2))
        del group
        group = list()

        if g == 2 and 1 in numList:
            numList.remove(1)
        if g % 2 == 0 and (total + g) // 2 in numList:
            print("half off")
            numList.remove((total + g) // 2)

        if groupIndex < len(part) - 1:
            print("if")
            # if groupIndex == 0 or g == numList[0] * 2:
            #     temp = numList[1]
            # else:
            #     temp = numList[0]
            curIndex = 0
            temp = numList[curIndex]
            while total + g - temp not in numList:
                curIndex += 1
                if curIndex < len(numList):
                    temp = numList[curIndex]
                else:
                    break
            # else:
            #     temp = numList[0]
            print(str(numList) + " " + str(temp))
            group.append(temp)
            numList.remove(temp)
            if temp >= g:
                temp = total + g - temp
            else:
                temp = g - temp
            group.append(temp)
            numList.remove(temp)

            if part[groupIndex] > 2:
                for gh in range(part[groupIndex] // 2 - 1):
                    cur = 0
                    while total - numList[cur] not in numList:
                        # print(str(numList) + " : " + str(total - numList[cur]))
                        cur += 1
                    temp = numList[cur]
                    print(str(numList) + " : " + str(temp))
                    group.append(temp)
                    numList.remove(temp)
                    group.append(total-temp)
                    numList.remove(total-temp)
        else:
            if g == 2 and 1 not in numList:
                numList.append(1)
            if g % 2 == 0 and (total + g) // 2 not in numList:
                numList.append(total + g // 2)
            for namber in numList:
                group.append(namber)
        groupList.append(group)
        groupIndex += 1
    return(sorted(groupList))


class csp():
    def __init__(self, base, partNum, sum, part, perm):
        self.base = base
        self.partNum = partNum
        self.sum = sum
        self.part = part
        self.perm = perm

    def to_string(self):
        return("p=" + str(self.partNum) + ", g=" + str(self.sum) + ", part=" + str(self.part) + ", group=" + str(self.perm))

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
    print(str(part) + " : " + str(sumList))
    for sum in sumList:
        print(str(part) + " : " + str(list(genConstantSumPartition(part, sum))))
