#!/usr/bin/env python3
import os;
import sys
import subprocess;
import argparse
import itertools

# Parser to get base number for computations
parser = argparse.ArgumentParser(description='A parser')
parser.add_argument("-n", dest='number', default=2, help='number to partition', type=int)
args = parser.parse_args();
n = args.number

# Returns a set of all partitions of number, made up of only even numbers.
# If number is odd, returns an empty set.
def partition(number):
        a = [0 for i in range(number + 1)]
        k = 1
        a[1] = number
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

# Generate a list of all permutations of provided list.
def all_perms(elements):
    if len(elements) <=1:
        yield elements
    else:
        for perm in all_perms(elements[1:]):
            for i in range(len(elements)):
                # nb elements[0:1] works in both string and list contexts
                yield perm[:i] + elements[0:1] + perm[i:]

# Calculates the sum of each group in a partition, given a permutation.
def checkConstant(calcNum, calcPart, calcPerm):
    start = 0
    end = 0
    sum = 0
    sums = set()
    for group in calcPart:
        sum = 0
        end += group
        for num in calcPerm[start:end]:
            sum += num
        sum = sum % calcNum
        sums.add(sum)
        start += group
    return sums

# ----------------------------Main Program------------------------------------ #

# Create and populate a list of Z up to number.
numList = list()
for k in range(1, n + 1):
    numList.append(k)

# Generate list of all even-cardinality partitions of n
partList = list()
for part in partition(n):
    if len(part) > 1:
        cur = part[0]
        same = True
        for h in part:
            if h != cur:
                same = False
        if same == False:
                partList.append(part)
# print('%03d' % n + " : " + str(partList))

# Generate list of all permutations of 0-(n-1)
permList = list()
for perm in all_perms(numList):
    permList.append(perm)
permList.sort()
# for wiggle in permList:
#     print(str(permList.index(wiggle)) + " : " + str(wiggle))

# # Check if a particular partition is constant-sum
# count = 0
# if len(partList) > 0:
#     print("List of non-obvious constant-sum-partitions of " + str(n) + ":")
# else:
#     print("Provided number has no non-obvious constant-sum-partitions.")
# for part in partList:
#     for perm in permList:
#         sumSet = checkConstant(n, part, perm)
#         if len(sumSet) == 1:
#             count += 1
#             x = min(sumSet)
#             print(str(count) + " : " + 'n : %03d' % n + ", p : " + str(len(part)) + ", part : " + str(part) +" : " + str(perm) + " : " + str(x))
