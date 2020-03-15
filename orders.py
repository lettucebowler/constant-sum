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

sums = findSums(n, p)
print("{}".format(gen_orders(n, sums[0])))