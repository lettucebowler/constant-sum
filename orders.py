#!/usr/bin/env python3
import argparse
import operator
from math import gcd
from copy import deepcopy
from functools import reduce

# Parser to get base number for computations
parser = argparse.ArgumentParser(description='A parser')
parser.add_argument("-n", dest='number', default=2, type=int)
parser.add_argument("-p", dest='partitions', default=2, type=int)
parser.add_argument("-t", dest='sum', default=2, type=int)
args = parser.parse_args()
n = args.number
p = args.partitions
t = args.sum

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

def findSums(n, p):
    return sorted(sum for sum in range(1, n) if sum * p % n == n // 2)

def get_order_t(n, t):
    return n * t // gcd(n, t) // t

def get_order_list(n, t, d):
    order_t = [d]
    i = t + d
    while i != d:
        order_t.append(i)
        i = (i + t) % n
    return order_t

def get_orders(n, t):
    order_t = [0]
    i = t
    while i != 0:
        order_t.append(i)
        i = (i + t) % n

    orders = dict()
    for i, num in enumerate(range(n // len(order_t))):
        orders.update({i: [num + i for num in order_t]})
    return orders

# def getCSP(total, part, t, odds):
#     if part == 1:
#         return gSum(total, t, part, list(range(total)), [], 0)

#     return gSum(total, t, part, pairs, leftovers, 0)

sums = findSums(n, p)
# print("{}".format(gen_orders(n, sums[0])))
for d in range(0, n // get_order_t(n, t)):
    print("{}".format(get_order_list(n, t, d)))