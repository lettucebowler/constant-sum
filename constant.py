#!/usr/bin/env python3
import os
import sys
import argparse

# Parser to get base number for computations
parser = argparse.ArgumentParser(description='A parser')
parser.add_argument("-n", dest='number', default=2, \
    help='number to partition', type=int)
args = parser.parse_args()
n = args.number

# n : number program is checking
# part : partition of n to check for potential sums
def findSums(n, p):
    return sorted(sum for sum in range(1, n) if sum * p % n == n // 2)

def gcd(a,b):
    while b > 0:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b / gcd(a, b)

# Validate list for constant-sum property
def checkListForErrors(candidate, total, g):
    checkList = [el for em in candidate for el in em]
    checkSet = set(checkList)
    good = []
    if len(checkSet) != len(checkList):
        good.append("duplicates")
    if any(sum(k) % total != g for k in candidate):
        good.append("sum")
    return good

# Create a constant-sum-partition from supplied partition
def getCSP(total, part, g):

    # Generate list of left-hand elements in each g-sum pair
    lL = [c for c in range(0, -part * g, -g)]

    # Generate list of right-hand elements in each g-sum pair
    rL = [b for b in range(g, part * g + 1, g)]

    # Generate list of offsets
    lD = int(lcm(total, g) // g // 2)
    oL = [(off + lD) // (lD * 2) for off in range(part)]

    # Combine lists with offset applied
    zL = zip(lL, rL, oL)
    gL = [((l + o) % total, (r - o) % total) for l, r, o in zL]

    # Construct list of remaining zero-sum pairs
    nL = list({tuple(sorted((x, total - x))) for x in range(total) \
        if not any(x in s for s in gL)})

    # Check for errors and output results
    gL += checkListForErrors(gL, total, g)
    return gSum(total, g, part, gL, nL)

# Storage object for csp data
class gSum():
    def __init__(self, n, g, p, csp, zsp):
        self.n = n
        self.p = p
        self.g = g
        self.csp = csp
        self.zsp = zsp

    def to_string(self):
        message = "Partitions:{0!r} Sum:{1!r}\n   csp:{2!r}"\
            .format(self.p, self.g, self.csp)
        if len(self.zsp) > 0:
            message += "\n   zsp:{0!r}".format(self.zsp)
        return message

# Exit if n is odd.
if n % 2 == 1:
    print("This program is only designed for even numbers.")
    exit()

# Calculate a csp for each partition and possible sum
pL = [p for p in range(1, n // 2 + 1) for sum in findSums(n, p)]
gL = [sum for p in range(1, n // 2 + 1) for sum in findSums(n, p)]
cL = [getCSP(n, p, pSum).to_string() for p, pSum in zip(pL, gL)]

# Output results
print(*cL, sep='\n')
