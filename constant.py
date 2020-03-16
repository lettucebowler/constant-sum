#!/usr/bin/env python3
import argparse
import operator
from math import gcd
from copy import deepcopy
from functools import reduce

# Parser to get base number for computations
parser = argparse.ArgumentParser(description='Generates a constant-sum partition with \
    each grouping having an even number of elements.')
parser.add_argument("-n", dest='number', default=4, type=int)
args = parser.parse_args()
n = args.number

class gSum():
    def __init__(self, n, t, p, csp, zsp, orders, odds):
        self.n = n
        self.p = p
        self.t = t
        self.csp = csp
        self.zsp = zsp
        self.orders = orders
        self.odds = odds

    def to_string(self):
        message = "Partitions:{0!r} Sum:{1!r} Odds:{2!r}\n   csp:{3!r}"\
            .format(self.p, self.t, self.odds, self.csp)
        if len(self.zsp) > 0:
            message += "\n   zsp:{0!r}".format(self.zsp)
        return message

def findSums(n, p):
    return sorted(sum for sum in range(1, n) if sum * p % n == n // 2)

def get_order_t(n, t):
    return n * t // gcd(n, t) // t

def get_order_list(n, t, d):
    order_t = [d]
    i = (t + d) % n
    while i != d:
        order_t.append(i)
        i = (i + t) % n
    return order_t   

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

def getCSP(total, part, t, odds):
    if part == 1:
        return gSum(total, t, part, list(range(total)), [], 0)
    o_num = 2 * part // get_order_t(n, t) - 1
    lefts = get_order_list(n, t, t)[:get_order_t(n, t) // 2]
    rights = get_order_list(n, n - t, 0)[:get_order_t(n, t) // 2] 
    pairs = [[lefty, righty] for lefty, righty in zip(lefts, rights)]
    for offset in range(1, o_num // 2 + 1):
        lefts = get_order_list(n, t, offset)
        rights = get_order_list(n, n - t, (-1 * offset) % t)
        pairs.extend([[lefty, righty] for lefty, righty in zip(lefts, rights)])
    unused_orders = [v for v in range(1, t) if v >= o_num + 1]
    leftovers = sorted({tuple(sorted((x, total - x))) for x in range(total) \
        if not any(x in s for s in pairs)})
    pairs += checkListForErrors(pairs, leftovers, total, t, odds)
    return gSum(total, t, part, pairs, leftovers, unused_orders, 0)

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

# Main Driver Program
if n % 4 != 0:
    print("This program is only designed for even numbers 0 mod 4")
    exit()

cL = [getCSP(n, p, pSum, 0) for p in range(2, n // 2 + 1, 2) for pSum in findSums(n, p)]
# oL = [y for x in cL for y in getOdds(x)]

for const in cL:
    print("{}\n".format(const.to_string()))