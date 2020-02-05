#!/usr/bin/env python3
import os;
import sys
import argparse

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
def findPossibleSums(n, p):
    potentialSumList = list(range(1, n))
    sumList = list()

    # Check each value in potentialSumList for validity as a constant sum
    # If valid, add it to sumList
    for g in potentialSumList:
        if g * p % n == n/2:
            sumList.append(g)

    return sorted(sumList)

def makeGrid(gridNum):
    numList = list(range(gridNum))
    numArray = list()
    tempList = list()
    for x in range(len(numList) // 2):
        del tempList
        tempList = list()
        tempVal = numList.pop(0)
        tempList.append(tempVal)
        if gridNum - tempVal in numList:
            tempList.append(gridNum - tempVal)
        else:
            tempList.append(gridNum // 2)
        numArray.append(tempList)
    del numList
    return numArray

# Create a constant-sum-partition from supplied partition
def genConstantSumPartition(total, part, g):
    groupList = list()
    numGrid = makeGrid(total)
    for wah in numGrid:
        print(str(wah))
    print("")

    # Validate results before returning
    checkList = list()
    good = list()
    groupList.sort(key=len)
    for k in groupList:

        # Check for Duplicates in csp
        k.sort()
        for l in k:
            if l not in checkList:
                checkList.append(l)
            elif "duplicates" not in good:
                good.append("duplicates")

        # Check that all groupings add up to g (MOD n)
        G = sum(k)
        if G % total != g and "sum" not in good:
            good.append("sum")

    # Check that each grouping is the write size for given partition of n
    for h in range(len(groupList)):
        if len(groupList[h]) != part[h] and "length" not in good:
            good.append("length")

    # Append a list of the errors found to the csp list
    if len(good) != 0:
        groupList.append(good)
    return groupList

# Storage object for csp data
class constantSumPartition():
    def __init__(self, n, g, p, csp):
        self.n = n
        self.p = p
        self.g = g
        self.csp = csp

    def to_string(self):
        message = "n:" + str(self.n) + " g:" + str(self.g) + " p:" + str(self.p) + " csp:" + str(const.csp)
        # message += str(const.csp)
        return(message)

# Exit if n is odd.
if n % 2 == 1:
    print("This program is only designed for even numbers.")
    exit()

# # Populate partition list and filter out irrelevant partitions.
# partList = list()
# for part in partition(n):
#     partList.append(part)
# partList.sort(reverse=True, key=len)

# Calculate a csp for each partition and possible sum
sumList = list()
cspList = list()
count = 0
# partList = [[2, 2, 6, 6]]
for part in range(1, n // 2 + 1):
    del sumList
    sumList = findPossibleSums(n, part)
    # sumList = [6]
    if len(sumList) > 0:
        for possibleSum in sumList:
            csp = list(genConstantSumPartition(n, part, possibleSum))
            newConst = constantSumPartition(n, possibleSum, part, csp)
            cspList.append(newConst)

# Output data
for const in cspList:
    print(const.to_string())
