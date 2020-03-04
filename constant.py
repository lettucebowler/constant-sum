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
    def __init__(self, n, t, p, csp, zsp, odds):
        self.n = n
        self.p = p
        self.t = t
        self.csp = csp
        self.zsp = zsp
        self.odds = odds

    def to_string(self):
        message = "Partitions:{0!r} Sum:{1!r} Odds:{2!r}\n   csp:{3!r}"\
            .format(self.p, self.t, self.odds, self.csp)
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
def getCSP(total, part, t, odds):

    # Skip processing if result is obvious
    if part == 1:
        return gSum(total, t, part, list(range(total)), [], 0)

    # Generate list of left-hand elements in each g-sum pair
    lL = [c for c in range(0, -part * t, -t)]

    # Generate list of right-hand elements in each g-sum pair
    rL = [b for b in range(t, part * t + 1, t)]

    # Generate list of offsets
    lD = lcm(total, t) // (t * 2)
    oL = [(off + lD) // (lD * 2) for off in range(part)]

    # Combine lists with offset applied
    zL = zip(lL, rL, oL)
    tL = [[(l + o) % total, (r - o) % total] for l, r, o in zL]

    # Construct list of remaining zero-sum pairs
    nL = sorted({tuple(sorted((x, total - x))) for x in range(total) \
        if not any(x in s for s in tL)})
    nL = [[x for x in y] for y in nL]

    # Check for errors and output results
    tL += checkListForErrors(tL, total, t)
    return gSum(total, t, part, tL, nL, 0)

def swap(e, zList):
    return 0

# Find next element in cList that can be substituted by a pair in zList
def findNext(n, t, cList, zList):
    z1 = [x[0] for x in zList]
    z2 = [x[1] for x in zList]
    c1 = [x for y in cList for x in y]
    for c in c1:
        if c != n // 2 and c != t:
            for b in z1:
                if c - b in z1:
                    return c
            for b in z2:
                if c - b in z2:
                    return c
    return -1

# Derive possible odd-cardinality csp from a given even-cardinality csp
# I think it will only work if p <= n // 4
def getOdds(const):
    withOdds = [const]
    if const.p == 1:
        return withOdds
    oddCount = [2] + [f for f in range(4, const.p + 1, 2) if const.p <= n // 4]
    c = [b for b in const.csp]
    z = [b for b in const.zsp]
    for o in oddCount:
        if o == 2:
            temp = const.csp[1: -1] + [[const.t], [0] + const.csp[1]]
            temp.sort(key=len)
            withOdds.append(gSum(const.n, const.t, const.p, temp, const.zsp, o))
        else:
            print(str(list(range(o, 2, -2))))
            for q in range(o, 2, -2):
                # Swap pair with element
                # Swap compliment pair with element
                e = findNext(const.n, const.t, c, z)
    return withOdds

# Exit if n is odd.
if n % 2 == 1:
    print("This program is only designed for even numbers.")
    exit()

# Calculate a csp for each partition and possible sum
rL = list(range(2, n // 2 + 1, 2))
pL = [p for p in rL for t in findSums(n, p)]
tL = [t for p in rL for t in findSums(n, p)]
cL = [getCSP(n, p, pSum, 0) for p, pSum in zip(pL, tL)]
oL = [y for x in cL for y in getOdds(x)]

# Output results
for const in oL:
    print(const.to_string())