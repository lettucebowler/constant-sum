#!/usr/bin/env python3
import os;
import sys
import argparse
import math

# Parser to get base number for computations
parser = argparse.ArgumentParser(description='A parser')
parser.add_argument("-n", dest='number', default=2, help='number to partition', type=int)
args = parser.parse_args();
n = args.number

# n : number program is checking
# part : partition of n to check for potential sums
def findSums(n, p):
    potentialSumList = list(range(1, n))
    sumList = list()

    # Check each value in potentialSumList for validity as a constant sum
    # If valid, add it to sumList
    for g in potentialSumList:
        if g * p % n == n/2:
            sumList.append(g)
    return sorted(sumList)

# Organize numList into a 2 x n/2 grid, creating rows that sum to n
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

# Return the value in numGrid that sums with first to g (MOD n)
def findOther(numGrid, first, total, gVal):
    returnVal = -1
    for wing in numGrid:
        for woop in wing:
            if (woop + first) % total == gVal:
                returnVal = woop
                break
    return returnVal

# Create a constant-sum-partition from supplied partition
def genConstantSumPartition(total, part, g):
    groupList = list()
    group = list()
    numGrid = list(range(total))

    # groupList.append([0, g])
    # numGrid.remove(0)
    # numGrid.remove(g)

    leftList = list(range(0, -1 * (part - 1) * g - 1, -1 * g))
    if len(leftList) == 0:
        leftList.append(0)
    print(str(leftList))
    rightList = list(range(g, part * g + 1, g))
    if len(rightList) == 0:
        rightList.append(g)
    print(str(rightList))

    offsetList = list()
    if g == total // 2:
        for off in range(part + 1):
            offsetList.append(off // 2)
        offsetList.pop(0)

    elif total % part != 0:
        for off in range(part + 3):
            offsetList.append(off // 4)
        offsetList.pop(0)
        offsetList.pop(0)
    else:
        for off in range(part):
            offsetList.append(0)

    print(str(offsetList))

    for v in range(part):
        groupList.append([(leftList[v] + offsetList[v]) % total, (rightList[v] - offsetList[v]) % total])
        # groupList.append([(leftList[v] + offsetList[v]), (rightList[v] - offsetList[v])])



    # Validate results before returning
    checkList = list()
    good = list()
    # groupList.sort()
    for k in groupList:

        # Check for Duplicates in csp
        # k.sort()
        for l in k:
            if l not in checkList:
                checkList.append(l)
            elif "duplicates" not in good:
                good.append("duplicates")

        # Check that all groupings add up to g (MOD n)
        G = sum(k)
        if G % total != g and "sum" not in good:
            good.append("sum")

    # Append a list of the errors found to the csp list
    if len(good) != 0:
        groupList.append(good)

    # Add groupList and numGrid to a returnList
    returnList = list()
    returnList.append(groupList)
    returnList.append(numGrid)
    return returnList

# Storage object for csp data
class gSum():
    def __init__(self, n, g, p, csp, zsp):
        self.n = n
        self.p = p
        self.g = g
        self.csp = csp
        self.zsp = zsp

    def to_string(self):
        message = "n:" + str(self.n) + " p:" + str(self.p) + " g:" + str(self.g) + " csp:" + str(const.csp)
        if len(self.zsp) > 0:
            message += " zsp:" + str(self.zsp)
        return(message)

# Begin Main Program

# Exit if n is odd.
if n % 2 == 1:
    print("This program is only designed for even numbers.")
    exit()

# Calculate a csp for each partition and possible sum
sumList = list()
cspList = list()

# Check each possible p
for p in range(1, n // 2 + 1):
    del sumList
    sumList = findSums(n, p)

    # Check each possible g
    for possibleSum in sumList:
        csp = list(genConstantSumPartition(n, p, possibleSum))
        zsPairList = csp.pop()
        csPairList = csp.pop()
        newConst = gSum(n, possibleSum, p, csPairList, zsPairList)
        cspList.append(newConst)

# Output data
for const in cspList:
    print(const.to_string())
