#!/usr/bin/env python3
import argparse
from math import gcd
from copy import deepcopy

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
def checkListForErrors(candidate, total, t):
    checkList = [el for em in candidate for el in em]
    checkSet = set(checkList)
    good = []
    if len(checkSet) != len(checkList):
        good.append("duplicates")
    if any(sum(k) % total != t for k in candidate):
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
    l = lcm(total, t) // (t * 2)
    oL = [(off + l) // (l * 2) for off in range(part)]
    if part <= n // 4:
        oL = [2 * f for f in oL]

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

# Swap element in a constant-sum pair for a pair that sums to the element
def swap(pTup, cList):
    p0 = pTup[0]
    p1 = pTup[1]
    for x in cList:
        if p0 in x:
            x.remove(p0)
            x += p1
    return 0

# Derive possible odd-cardinality csp from a given even-cardinality csp
# I think it will only work if p <= n // 4
def getOdds(const):
    withOdds = [const]
    z = deepcopy(const.zsp)
    zR = [b[0] for b in z]
    zL = [b[1] for b in z]
    zL.reverse()

    oddCount = [2] + [f for f in range(4, const.p + 1, 2) if const.p <= n // 4]
    for o in oddCount:
        c = deepcopy(const.csp)
        if const.t % 2 == 0 and o > 2:
            tL = [const.t, const.n - const.t]
            z1 = [[a, b] for a, b in zip(zR, zL) if (a + b) % n not in tL]
            s = [(a + b) % const.n for a, b in z1]
            pL = list(zip(s, z1))
            
            for f in range(o, 2, -2):
                swap(pL.pop(), c)
                swap(pL.pop(0), c)
                    
        c[0] = [c[0][1]]
        if 0 not in c[1]:
            c[1].append(0) 
        
        nL = sorted({tuple(sorted((x, const.n - x))) for x in range(const.n) \
            if not any(x in s for s in c)})
        nL = [[x for x in y] for y in nL]        

        # Check for errors and output
        c.sort(key=len)
        c += checkListForErrors(c, const.n, const.t)  
        withOdds.append(gSum(const.n, const.t, const.p, c, nL, o)) 
    return withOdds

# Exit if n is odd.
if n % 4 != 0:
    print("This program is only designed for even numbers 0 mod 4")
    exit()

# Calculate a csp for each partition and possible sum
rL = list(range(2, n // 2 + 1, 2))
pL = [p for p in rL for t in findSums(n, p)]
tL = [t for p in rL for t in findSums(n, p)]
cL = [getCSP(n, p, pSum, 0) for p, pSum in zip(pL, tL)]
oL = [y for x in cL for y in getOdds(x)]

# Output results
for const in oL:
    print("{0}\n".format(const.to_string()))