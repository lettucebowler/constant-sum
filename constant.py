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

class constant_sum_partition():
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

def find_sums(n, p):
    return sorted(sum for sum in range(1, n) if sum * p % n == n // 2)

def lcm(a, b):
    return a * b // gcd(a, b)  

def check_list_for_errors(candidate, zandidate, total, t, o):
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

def get_csp(total, part, t, odds):
    if part == 1:
        return constant_sum_partition(total, t, part, list(range(total)), [], 0)

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
    pairs += check_list_for_errors(pairs, leftovers, total, t, odds)
    return constant_sum_partition(total, t, part, pairs, leftovers, 0)

def get_odds(const):
    const_copy = deepcopy(const.csp)
    const_copy = [[const_copy[0][1]], [0] + const_copy[1]] + const_copy[2:]
    withOdds = [const, constant_sum_partition(const.n, const.t, const.p, \
        const_copy, const.zsp, 2)]
    return withOdds

# Main Driver Program
if n % 4 != 0:
    print("This program is only designed for even numbers 0 mod 4")
    exit()

csp_list = [get_csp(n, p, p_sum, 0) for p in range(2, n // 2 + 1, 2) \
    for p_sum in find_sums(n, p)]
odd_list = [y for x in csp_list for y in get_odds(x)]

for const in odd_list:
    print("{}".format(const.to_string()))