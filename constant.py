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

def get_order_t(n, t):
    return n * t // gcd(n, t) // t 

def gen_orders(n, t):
    order_t = [0]
    i = t
    while i != 0:
        order_t.append(i)
        i = (i + t) % n

    orders = dict()
    for i, num in enumerate(range(n // len(order_t))):
        orders.update({i: [num + i for num in order_t]})
    return orders

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

def checkListForErrors(candidate, zandidate, total, t, o):
    errors = []
    checkList = reduce(operator.concat, candidate)
    if zandidate != []:
        checkList += reduce(operator.concat, zandidate)
    if len(checkList) != total:
        errors.append("duplicates")
    if any(sum(k) % total != t for k in candidate):
        errors.append("sum")
    oddCount = [f for f in candidate if len(f) % 2 == 1]
    if len(oddCount) != o:
        errors.append("oddsoff")
    return errors

def get_order_list(n, t, d):
    order_t = [d]
    i = t + d
    while i != d:
        order_t.append(i)
        i = (i + t) % n
    return order_t

# Create a constant-sum-partition from supplied partition
def getCSP(total, part, t, odds):
    if part == 1:
        return gSum(total, t, part, list(range(total)), [], 0)
    o_num = 2 * p // get_order_t(n, t) - 1
    left = get_order_list(n, t, t)
    right = get_order_list(n, n - t, 0)  
    pairs = [[lefty, righty] for lefty, righty in zip(left, right)][:get_order_t(n, t) // 2]
    for offset in range(1, o_num // 2 + 1):
        left = get_order_list(n, t, offset)
        right = get_order_list(n, n - t, (-1 * offset) % t)
        pairs += [[lefty, righty] for lefty, righty in zip(left, right)]
    leftovers = sorted({tuple(sorted((x, total - x))) for x in range(total) \
        if not any(x in s for s in pairs)})
    pairs += checkListForErrors(pairs, leftovers, total, t, odds)
    return gSum(total, t, part, pairs, leftovers, 0)

def findPairs(n, sum, searchList):
    for i, q in enumerate(searchList):
        for w in searchList[i + 1:]:
            if (q + w) % n == sum:
                rT = [q, w,n - q, n - w]
                rL = {(q + w) % n: [q, w], (2 * n - q - w) % n: [n - q, n - w]}
                for rem in rT:
                    searchList.remove(rem)
                return rL
    return rL

# Derive possible odd-cardinality csp from a given even-cardinality csp
def getOdds(const):
    c = deepcopy(const.csp)
    c = [[c[0][1]], [0] + c[1]] + c[2:]
    zT = [bingo for bango in const.zsp for bingo in bango]
    withOdds = [const, gSum(const.n, const.t, const.p, c, const.zsp, 2)]
    oddCount = [f for f in range(4, const.p - 1, 2) \
        if const.p <= n // 4 and const.t % 2 == 0]
    for o in oddCount:
        c = deepcopy(const.csp)
        zL = deepcopy(zT)
        sumDict = {v[0]: c.index(v) for v in c}
        sumDict.update({v[1]: c.index(v) for v in c})
        for index in range(-1, -1 * (o - 3) - 1, -2):
            pL = findPairs(n, c[index][0], zL)
            for key in pL:
                c[sumDict[key]].remove(key)
                c[sumDict[key]] += pL[key]
        c = [[c[0][1]], [0] + c[1]] + c[2:]
        nL = list(set([tuple(sorted((x, const.n - x))) for x in range(const.n) \
            if not any(x in f for f in c)]))
        c = sorted([sorted(k) for k in c]) + checkListForErrors(c, nL, const.n, const.t, o) 
        withOdds.append(gSum(const.n, const.t, const.p, c, nL, o)) 
    return withOdds

# Exit if n is odd.
if n % 4 != 0:
    print("This program is only designed for even numbers 0 mod 4")
    exit()

# Calculate a csp for each partition and possible sum
cL = [getCSP(n, p, pSum, 0) for p in range(2, n // 2 + 1, 2) for pSum in findSums(n, p)]
# oL = [y for x in cL for y in getOdds(x)]

# Output results
for const in cL:
    print("{}\n".format(const.to_string()))