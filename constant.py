#!/usr/bin/env python3
import os;
import sys
import subprocess;
import argparse
import itertools
import math

# Parser to get base number for computations
parser = argparse.ArgumentParser(description='A parser')
parser.add_argument("-n", dest='number', default=2, help='number to partition', type=int)
args = parser.parse_args();
n = args.number

# Returns a list of all partitions of number, made up of only even numbers.
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

# n : number program is checking
# part : partition of n to check for potential sums
def findPossibleSums(n, part):
    p = len(part)
    potentialSumList = list(range(1, n))
    sumList = list()

    for g in potentialSumList:
        if g * p % n == n/2:
            sumList.append(g)
    return sorted(sumList)

# def all_combs(seq, parts, indexes=None, res=[], cur=0):
#     if indexes is None: # indexes to use for combinations
#         indexes = range(len(seq))
#
#     if cur >= len(parts): # base case
#         yield [[seq[i] for i in g] for g in res]
#         return
#
#     for x in itertools.combinations(indexes, r=parts[cur]):
#         set_x = set(x)
#         new_indexes = [i for i in indexes if i not in set_x]
#         for comb in all_combs(seq, parts, new_indexes, res=res + [x], cur=cur + 1):
#             yield comb
#
# #Calculate number of groups of a partition.
# def calcGroups(calcTop, calcBottom):
#     tempCalc = math.factorial(calcTop)
#     for h in calcBottom:
#         tempCalc //= math.factorial(h)
#     return tempCalc
#
# # Calculates the sum of each group in a partition, given a permutation.
# def checkConstant(calcNum, calcGroup):
#     sums = set()
#     for a in calcGroup:
#         sums.add(sum(a) % calcNum)
#     return sums

class csp():
    def __init__(self, base, partNum, sum, part, perm):
        self.base = base
        self.partNum = partNum
        self.sum = sum
        self.part = part
        self.perm = perm

    def to_string(self):
        return("p=" + str(self.partNum) + ", g=" + str(self.sum) + ", part=" + str(self.part) + ", group=" + str(self.perm))

# ----------------------------Main Program------------------------------------ #
partList = list()

# Populate partition list and filter out irrelevant partitions.
for part in partition(n):
    partList.append(part)
partList.sort(reverse=True, key=len)

# Print partition and possible sums
for part in partList:
    # print(str(part))
    print("Partition : " + str(part) + " Possible g : " + str(findPossibleSums(n, part)))
