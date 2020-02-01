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

    # Check each value in potentialSumList for validity as a constant sum
    # If valid, add it to sumList
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
        message = "n:" + str(self.n) + " g:" + str(self.g) + " p:" + str(self.p) + " part:" + str(self.part) + " csp:"
        message += str(const.csp)
        # if len(self.csp) > 0:
            # message += str(const.csp)
        # else:
        #     message += "Algorithm Failure"
        return(message)

# Create a constant-sum-partition from supplied partition
def genConstantSumPartition(total, part, g):
    groupList = list()
    group = list()
    numList = list(range(1, total + 1))
    allSame = False

    # Populate groupList with empty lists
    del group
    group = list()
    for i in range(len(part)):
        groupList.append(list())

    # Check for trivial case where all p in P are equal
    # if all(elem == part[0] for elem in part) and g % total == total // len(part) // 2:
    if all(elem == part[0] for elem in part):
        allSame = True

    # Check for case when all p in P = 2 (MOD n)
    # if all(elem % 4 == 2 for elem in part):
    if True:
        lista = list()
        listb = list()

        # Determine spot to split list
        if allSame:
            testValue = g // (part[0] // 2)
        else:
            testValue = g

        # Split numList into two lists containing pairs summing to g (MOD P)
        for j in numList:
            if j < testValue:
                if j not in lista or j not in listb:
                    lista.append(j)
            else:
                if j not in lista or j not in listb:
                    listb.append(j)
        del numList

        # Populate each p in P with a pair that sums to g (MOD n)
        counter = 0
        for sameP in range(len(part)):
            if len(listb) >= 2:
                groupList[sameP].append(listb.pop(0))
                groupList[sameP].append(listb.pop())
            else:
                if len(lista) >= 2:
                    groupList[sameP].append(lista.pop(0))
                    groupList[sameP].append(lista.pop())
                else:
                    if len(lista) == 1 and len(listb) == 1:
                        groupList[sameP].append(lista.pop())
                        groupList[sameP].append(listb.pop())

        # Combine the remaining elements in lista and listb back into numList
        numList = lista + listb
        numList.sort()

        # for y in groupList:










    # if len(groupList[0]) == 0:
    # #     for y in range(total):
    # #         del group
    # #         group = list()
    # #         groupList.append(group)
    # #         if (g + y) % total in numList and total - y in numList and g + y != total - y:
    # #             if y < len(part):
    # #                 if len(groupList[y]) == 0 and g + y < (g + total) / 2:
    # #                     groupList[y].append((g + y) % total)
    # #                     groupList[y].append(total - y)
    #
    #
    #     for a in range(len(part)):
    #         v = groupList[a]





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
    checkList = list()
    good = list()
    for k in groupList:
        k.sort()
        for l in k:
            if l not in checkList:
                checkSet.append(l)
            else:
                good.append("duplicates")

        G = sum(k)

        if G % total != g:
            good.append("sum")

    for h in range(len(part)):
        if len(groupList[h]) != part[h]:
            good.append("length")

    # Delete groupList if it does not pass validity checks
    groupList.sort(key=len)
    if len(good) != 0:
        groupList.append(good)


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
# partList = [[2, 2, 6, 6]]
for part in partList:
    if True:
    # if len(part) % 2 == 0:
        del sumList
        sumList = findPossibleSums(n, part)
        # sumList = [6]
        if len(sumList) > 0:
            # print(str(part))
            for possibleSum in sumList:
                csp = list(genConstantSumPartition(n, part, possibleSum))
                cspList.append(constantSumPartition(n, possibleSum, len(part),  part, csp))
                # else:
                #     print("Algorithm Failure")
                #     exit()

# Output data
for const in cspList:
    print(const.to_string())
