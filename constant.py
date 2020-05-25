#!/usr/bin/env python3
import argparse
import operator
from math import gcd
from copy import deepcopy
from functools import reduce

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

def check_list_for_errors(constant_pairs, unused_numbers, total, t, o):
    errors = []
    check_list = reduce(operator.concat, constant_pairs)
    if unused_numbers != []:
        for pair in unused_numbers:
            check_list.append(pair)

    # If there are no duplicates, then check_list will have n elements
    if len(check_list) != total:
        errors.append("duplicates")

    # All pairs should sum to 0 (MOD n)
    if any(sum(pair) % total != t for pair in constant_pairs):
        errors.append("sum")
    return errors

def get_csp(total, part, t, odds):
    if part == 1:
        return constant_sum_partition(total, t, part, list(range(total)), [], 0)

    # Generate list of left-hand elements in each g-sum pair
    lefts = list(range(0, -part * t, -t))
    rights = list(range(t, part * t + 1, t))

    # Generate list of offsets
    order = lcm(total, t) // (t * 2)
    offsets = [(off + order) // (order * 2) for off in range(part)]

    # Combine elements from each list to form constant pairs
    zipped = zip(lefts, rights, offsets)
    leftovers = list(range(total))
    pairs = []
    for left_elem, right_elem, offset in zipped:
        pairs.append([(left_elem + offset) % total, (right_elem - offset) % total])
        for element in pairs[-1]:
            leftovers.remove(element)

    # Group remaining numbers into pairs summing to 0
    zero_sum_pairs = [sorted([h, total - h]) for h in leftovers][::2]

    # Check for errors
    pairs += check_list_for_errors(pairs, leftovers, total, t, odds)
    return constant_sum_partition(total, t, part, pairs, zero_sum_pairs, 0)

def get_odds(const):
    const_copy = deepcopy(const.csp)

    # Shift zero to make some odd-cardinality groupings
    const_with_2_odds = [[const_copy[0][1]], [0] + const_copy[1]].extend(const_copy[2:])
    return(constant_sum_partition(const.n, const.t, const.p, \
        const_copy, const.zsp, 2))

# Parser to get base number for computations
parser = argparse.ArgumentParser(description='Generates a constant-sum partition with \
    each grouping having an even number of elements.')
parser.add_argument("-n", dest='number', default=4, type=int)
args = parser.parse_args()
n = args.number

# Main Driver Program
if n % 4 != 0:
    print("This program is only designed for even numbers 0 mod 4")
    exit()

for p in range(2, n // 2 + 1, 2):
    for p_sum in find_sums(n, p):
        csp = get_csp(n, p, p_sum, 0)
        print("{}\n{}".format(csp.to_string(), get_odds(csp).to_string()))