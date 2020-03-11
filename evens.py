#!/usr/bin/env python3
import argparse
import operator
from math import gcd
from copy import deepcopy
from functools import reduce

# Parser to get base number for computations
parser = argparse.ArgumentParser(description='A parser')
parser.add_argument("-n", dest='number', default=2, type=int)
args = parser.parse_args()
n = args.number

def findSums(n, p):
    return sorted(sum for sum in range(1, n) if sum * p % n == n // 2)

def lcm(a, b):
    return a * b // gcd(a, b)

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

def checkListForErrors(candidate, zandidate, total, t):
    good = []
    checkList = reduce(operator.concat, candidate)
    if zandidate != []:
        checkList += reduce(operator.concat, zandidate)
    
    if len(checkList) != total:
        good.append("duplicates")
        
    if any(sum(k) % total != t for k in candidate):
        good.append("sum")
        
    return good

# Create a constant-sum-partition from supplied partition
def getCSP(total, part, t):
    if part == 1:
        return gSum(total, t, part, list(range(total)), [], 0)

    # Generate list of left-hand elements in each g-sum pair
    lefts = [c for c in range(0, -part * t, -t)]
    rights = [b for b in range(t, part * t + 1, t)]

    # Generate list of offsets
    order = lcm(total, t) // (t * 2)
    offsets = [(off + order) // (order * 2) for off in range(part)]

    # Glue it all together
    zipped = zip(lefts, rights, offsets)
    pairs = [[(l + o) % total, (r - o) % total] for l, r, o in zipped]
    leftovers = sorted({tuple(sorted((x, total - x))) for x in range(total) \
        if not any(x in s for s in pairs)})

    # Check for errors
    pairs += checkListForErrors(pairs, leftovers, total, t)
    return gSum(total, t, part, pairs, leftovers, 0)

# Exit if n is odd.
if n % 4 != 0:
    print("This program is only designed for even numbers 0 mod 4")
    exit()

# Calculate a csp for each partition and possible sum
nums = range(2, n // 2 + 1, 2)
cL = [getCSP(n, p, pSum) for p in nums for pSum in findSums(n, p)]

# Output results
for const in cL:
    print("{}\n".format(const.to_string()))