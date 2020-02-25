#!/usr/bin/env python3
import os
import sys
import argparse

# Parser to get base number for computations
parser = argparse.ArgumentParser(description='A parser')
parser.add_argument("-n", dest='number', default=2, help='number to partition', type=int)
args = parser.parse_args()
n = args.number

# n : number program is checking
# part : partition of n to check for potential sums
def findSums(n, p):
    potentialSumList = list(range(1, n))
    return sorted(sum for sum in potentialSumList if sum * p % n == n // 2)

def gcd(a,b):
    while b > 0:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b / gcd(a, b)

# Validate list for constant-sum property
def checkListForErrors(candidate, total, g):
    checkList = list()
    good = list()
    candidate.sort()
    for k in candidate:
        for l in k:
            if l not in checkList:
                checkList.append(l)
            elif "duplicates" not in good:
                good.append("duplicates")

        G = sum(k)
        if G % total != g and "sum" not in good:
            good.append("sum")
    return good

# Create a constant-sum-partition from supplied partition
def genConstantSumPartition(total, part, g):

    # Generate list of left-hand elements in each g-sum pair
    leftList = [c for c in range(0, -1 * (part - 1) * g - 1, -1 * g)]

    # Generate list of right-hand elements in each g-sum pair
    rightList = [b for b in range(g, part * g + 1, g)]

    # Generate list of offsets
    lcmDiv = int(lcm(total, g) // g // 2)
    offsetList = [(off + lcmDiv) // (lcmDiv * 2) for off in range(part)]

    # Combine lists with offset applied
    groupList = [((left + offset) % total, (right - offset) % total) for left, right, offset in zip(leftList, rightList, offsetList)]

    # Construct list of remaining zero-sum pairs
    numGrid = list({tuple(sorted((x, total - x))) for x in range(total) if not any(x in subList for subList in groupList)})

    # Append a list of the errors found to the csp list
    groupList += checkListForErrors(groupList, total, g)

    return [groupList, numGrid]

# Storage object for csp data
class gSum():
    def __init__(self, n, g, p, csp, zsp):
        self.n = n
        self.p = p
        self.g = g
        self.csp = csp
        self.zsp = zsp

    def to_string(self):
        message = "n:" + str(self.n) + " p:" + str(self.p) + " g:" + str(self.g) + " csp:" + str(self.csp)
        if len(self.zsp) > 0:
            message += " zsp:" + str(self.zsp)
        return(message)

# Exit if n is odd.
if n % 2 == 1:
    print("This program is only designed for even numbers.")
    exit()

cspList = list()

# Calculate a csp for each partition and possible sum
for p in range(1, n // 2 + 1):
    for possibleSum in findSums(n, p):
        csp = list(genConstantSumPartition(n, p, possibleSum))
        newConst = gSum(n, possibleSum, p, csp[0], csp[1])
        cspList.append(newConst.to_string())

# Output results
print(*cspList, sep='\n')
