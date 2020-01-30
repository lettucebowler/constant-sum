#!/usr/bin/env python3
import os;
import sys
import subprocess;
import argparse
import itertools
import math

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
        i = 0
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
                i += 1
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

class constantSumPartition():
    def __init__(self, n, g, p, part, csp):
        self.n = n
        self.p = p
        self.g = g
        self.part = part
        self.csp = csp

    def to_string(self):
        return("n:" + str(self.n) + " g:" + str(self.g) + " p:" + str(self.p) + " part:" + str(self.part) + " csp:" + str(self.csp))

# Create a random constant-sum-partition from supplied partition
def genConstantSumPartition(part, g):
    total = 0
    for x in part:
        total += x
    groupList = list()
    group = list()
    numList = list(range(1, total + 1))

    # Populate groupList with empty lists
    del group
    group = list()
    for i in range(len(part)):
        groupList.append(list())

    # Check for trivial case where all p in P are equal
    tempSet = set()
    for o in part:
        tempSet.add(o)
    if len(tempSet) == 1:
        lista = list()
        listb = list()
        if g % 2 ==1:
            testValue = g
        else:
            testValue = g - 1
        for j in numList:
            if j < testValue:
                lista.append(j)
            else:
                listb.append(j)

        for sameP in range(len(part)):
            while len(groupList[sameP]) < part[sameP]:
                if len(lista) >= 2:
                        groupList[sameP].append(lista.pop(0))
                        groupList[sameP].append(lista.pop())
                else:
                    if len(listb) >= 2:
                        groupList[sameP].append(listb.pop(0))
                        groupList[sameP].append(listb.pop())




    if len(groupList[0]) == 0:
    #     for y in range(total):
    #         del group
    #         group = list()
    #         groupList.append(group)
    #         if (g + y) % total in numList and total - y in numList and g + y != total - y:
    #             if y < len(part):
    #                 if len(groupList[y]) == 0 and g + y < (g + total) / 2:
    #                     groupList[y].append((g + y) % total)
    #                     groupList[y].append(total - y)


        for a in range(len(part)):
            v = groupList[a]





    #         groupList = groupList[:len(part)]
    #         for get in groupList:
    #             if len(get) == 0:
    #                 temp = numList[0]
    #                 get.append(temp)
    #                 get.append(g - temp)
    #                 numList.remove(temp)
    #                 numList.remove(g - temp)

    #     for set in groupList:
    #         for item in set:
    #             if item in numList:
    #                 numList.remove(item)

    #     for z in range(len(groupList)):
    #         if part[z] > 2:
    #             group = groupList[z]
    #             for h in numList:
    #                 if len(group) < part[z]:
    #                     if (total - h) in numList and (total - h) != h:
    #                         group.append(h)
    #                         group.append(total - h)
    #                         numList.remove(h)
    #                         numList.remove(total - h)
    #                     if z == len(groupList) - 1:
    #                         for b in numList:
    #                             groupList[z].append(b)

    # Validate results before returning
    # checkSet = list()
    # for k in groupList:
    #     k.sort()
    #     for l in k:
    #         if l not in checkSet:
    #             checkSet.append(l)
    #         else:
    #             del groupList
    #             groupList = list()
    #     G = sum(k)
    #     if G % total != g:
    #         del groupList
    #         groupList = list()
    # groupList.sort(key=len)
    return groupList

# ----------------------------Main Program------------------------------------ #
partList = list()
partCount = 0

# Exit if n is odd.
if n % 2 == 1:
    print("This program is only designed for even numbers.")
    exit()

# Populate partition list and filter out irrelevant partitions.
for part in partition(n):
    partCount += 1
    partList.append(part)
partList.sort(reverse=True, key=len)

# Calculate a csp for each partition and possible sum
sumList = list()
cspList = list()
count = 0
for part in partList:
    print(str(part))
    # if len(part) % 2 == 0:
    del sumList
    sumList = findPossibleSums(n, part)
    for possibleSum in sumList:
        # print(str(possibleSum))
        csp = list(genConstantSumPartition(part, possibleSum))
        if len(csp) > 0:
            # print("append : " + str(part))
            cspList.append(constantSumPartition(n, possibleSum, len(part), part, csp))
        else:
            print("Algorithm Failure")
            exit()

# Output data
# lengths = list()
for const in cspList:
#     del lengths
#     lengths = list()
#     for u in const:
#         lengths.append(len(u))
    print(const.to_string())
