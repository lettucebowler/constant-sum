#!/usr/bin/env python3
import argparse
from math import gcd

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

def lcm(a, b):
    return a * b // gcd(a, b)

# Storage object for csp data
class gSum():
    def __init__(self, n, t, p, csp, zsp):
        self.n = n
        self.p = p
        self.t = t
        self.csp = csp
        self.zsp = zsp

    def to_string(self):
        message = "Partitions:{0!r} Sum:{1!r}\n   csp:{2!r}"\
            .format(self.p, self.t, self.csp)
        if len(self.zsp) > 0:
            message += "\n   zsp:{0!r}".format(self.zsp)
        return message

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
def getCSP(total, part, t, odd):

    # Generate list of left-hand elements in each g-sum pair
    lL = [c for c in range(0, -part * t, -t)]

    # Generate list of right-hand elements in each g-sum pair
    rL = [b for b in range(t, part * t + 1, t)]

    # Generate list of offsets
    lD = lcm(total, t) // (t * 2)
    oL = [(off + lD) // (lD * 2) for off in range(part)]

    # Combine lists with offset applied
    zL = zip(lL, rL, oL)
    tL = [((l + o) % total, (r - o) % total) for l, r, o in zL]

    # Construct list of remaining zero-sum pairs
    nL = list({tuple(sorted((x, total - x))) for x in range(total) \
        if not any(x in s for s in tL)})

    # Check for errors and output results
    tL += checkListForErrors(tL, total, t)
    return gSum(total, t, part, tL, nL)

# Derive possible odd-cardinality csp from a given even-cardinality csp
# I think it will only work if p <= n // 4
def getOdds(const):
    if const.p <= const.n // 4:
        oddCount = [v for v in range(0, const.p + 1, 2)]
    else:
        oddCount= [0, 2]
    return oddCount

# Exit if n is odd.
if n % 2 == 1:
    print("This program is only designed for even numbers.")
    exit()

# Calculate a csp for each partition and possible sum
# p : number of groups in a partition
# t : constant sum of each group
pL = [p for p in range(1, n // 2 + 1) for t in findSums(n, p)]
tL = [t for p in range(1, n // 2 + 1) for t in findSums(n, p)]
cL = [getCSP(n, p, pSum, 0) for p, pSum in zip(pL, tL)]
oL = [getOdds(x) for x in cL]

# Output results
for const in cL:
    print(const.to_string())