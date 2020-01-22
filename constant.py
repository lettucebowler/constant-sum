#!/usr/bin/python
import os;
import sys
import subprocess;
import argparse
import itertools

parser = argparse.ArgumentParser(description='A parser')
parser.add_argument("-n", dest='number', default=2, help='the number to partition', type=int)
args = parser.parse_args();
n = args.number

# Returns a set of all partitions of number, made up of only even numbers.
# If number is odd, returns an empty set.
def partition(number):
        a = [0 for i in range(n + 1)]
        k = 1
        a[1] = n
        while k != 0:
            x = a[k - 1] + 1
            y = a[k] - 1
            k -= 1
            while x <= y:
                a[k] = x
                y -= x
                k += 1
            a[k] = x + y
            isEven = True
            for g in a[:k+1]:
                if g % 2 != 0:
                    isEven = False
            if isEven == True:
                yield a[:k + 1]

def all_perms(elements):
    if len(elements) <=1:
        yield elements
    else:
        for perm in all_perms(elements[1:]):
            for i in range(len(elements)):
                # nb elements[0:1] works in both string and list contexts
                yield perm[:i] + elements[0:1] + perm[i:]


# Checks if a partition is constant-sum, and returns boolean.
def checkConstant():
    print("Hello from checkConstant!")

# Create and populate a list of Z up to number.
numList = list()
for k in range(1, n + 1):
    numList.append(k)

partList = list()
for part in partition(n):
    partList.append(part)
# print('%03d' % n + " : " + str(partList))
permList = list()
for perm in all_perms(numList):
    permList.append(perm)
