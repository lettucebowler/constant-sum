#!/usr/bin/env python3
import argparse
import operator
from math import gcd
from copy import deepcopy
from functools import reduce


# Parser to get base number for computations
parser = argparse.ArgumentParser(description='A parser')
parser.add_argument("-n", dest='number', default=2, \
    help='number to partition', type=int)
args = parser.parse_args()
n = args.number

# Calculated possible sums for given p
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
def checkListForErrors(candidate, zandidate, total, t, o):
    good = []
    checkList = reduce(operator.concat, candidate)
    if zandidate != []:
        checkList += reduce(operator.concat, zandidate)
    
    if len(checkList) != total:
        good.append("duplicates")
        
    if any(sum(k) % total != t for k in candidate):
        good.append("sum")
        
    oddCount = [f for f in candidate if len(f) % 2 ==1]
    if len(oddCount) != o:
        good.append("oddsoff")
        
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
    tL += checkListForErrors(tL, nL, total, t, odds)
    return gSum(total, t, part, tL, nL, 0)

def findPairs(n, v, zList):
    rL = []
    for q in zList[:-1]:
        for w in zList[zList.index(q) + 1:]:
            print("q:{}\nz:{}\n\n".format(q, w, zList[zList.index(q) + 1:]))
            if (q[0] + w[0]) % n == v:
                rL = [[q[0], w[0]], [q[1], w[1]]]
                rL = [[q[1], w[1]], [q[0], w[0]]]
                break
            elif (q[1] + w[1]) % n == v: 
                rL = [[q[0], w[0]], [q[1], w[1]]]
                break
    print("{}\n{}\n{}\n".format(v, zList, rL))
    return rL

# Derive possible odd-cardinality csp from a given even-cardinality csp
# I think it will only work if p <= n // 4
def getOdds(const):
    withOdds = [const]
    z = deepcopy(const.zsp)
    oddCount = [2] + [f for f in range(4, const.p + 1, 2) \
        if const.p <= n // 4 and const.t % 2 == 0]
    
    for o in oddCount:
        c = deepcopy(const.csp)
        
        # Fancy substitution currently only works for even t
        if const.t % 2 == 0 and o > 2:
            cR = list(reversed(c))
            if (cR[0][1] + cR[-3][0]) % n == 0:
                cR.insert(-2, cR.pop(0))
            print("p:{}\nt:{}\nz:{}\n{}\n{}\n".format(const.p, const.t, z, cR, o))
            for index in range(0, o - 2, 2):
                print(str(index))
                pL = findPairs(n, cR[index][0], z)
                print(str(pL))
                cR[index] = pL[1] + [cR[index][1]]
                cR[index + 1] = pL[0] + [cR[index + 1][0]]
            c = list(reversed(cR))
        
        # Final easy substitution                     
        c[0] = [c[0][1]]
        c[1].append(0) 
        
        # Generate Zsp list
        temp = reduce(operator.concat, c)
        nL = list(set([tuple(sorted((x, const.n - x))) for x in range(const.n) \
            if x not in temp]))
        nL = [[x for x in y] for y in nL]        

        # Check for errors and output
        # c.sort(key=len)
        c += checkListForErrors(c, nL, const.n, const.t, o)  
        withOdds.append(gSum(const.n, const.t, const.p, c, nL, o)) 
    return withOdds

# Exit if n is odd.
if n % 4 != 0:
    print("This program is only designed for even numbers 0 mod 4")
    exit()

# Calculate a csp for each partition and possible sum
rL = list(range(2, n // 2 + 1, 2))
pL = [p for p in rL if len(findSums(n, p)) != 0]
tL = [findSums(n, p)[0] for p in pL if len(findSums(n, p)) != 0]
cL = [getCSP(n, p, pSum, 0) for p, pSum in zip(pL, tL)]
oL = [y for x in cL for y in getOdds(x)]


# Output results
for const in oL:
    print("{0}\n".format(const.to_string()))
    # if const.p == 4:
    #     print("{0}\n".format(const.to_string()))