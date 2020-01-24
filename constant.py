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

# Generate a list of all permutations of provided list.
def all_perms(elements):
    if len(elements) <=1:
        yield elements
    else:
        for perm in all_perms(elements[1:]):
            for i in range(len(elements)):
                # nb elements[0:1] works in both string and list contexts
                yield perm[:i] + elements[0:1] + perm[i:]

# def all_combs(combPart, combNumList):
#     combSet = set()
#     if len(elements) <=1:
#         yield elements
#     else:
#         for a in combPart:
#             for b in itertools.combinations(combNumList, a):
#                 curNumList -= set(b)

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

class csp():
    def __init__(self, base, partNum, sum, part, perm):
        self.base = base
        self.partNum = partNum
        self.sum = sum
        self.part = part
        self.perm = perm

    def to_string(self):
        return(str(self.base) + " : " + str(self.partNum) + " : " + str(self.sum) + " : " + str(self.part) + " : " + str(self.perm))

# ----------------------------Main Program------------------------------------ #
cspList = list()
numList = list(range(1, n+1))

# Populate partition list and filter out irrelevant partitions.
partList = list()
for part in partition(n):
    if len(part) > 0:
    # if len(part) > 0:
        cur = part[0]
        isBad = False
        # isBad = True
        # for h in part:
        #     if h != cur:
        #         isBad = False
        # if(n/2 % 2 == 1):
        #     if len(part) % 2 == 0:
        #         isBad = True
        if isBad == False:
                partList.append(part)

# Generate list of all permutations of 0-(n-1)
permList = list()
for perm in all_perms(numList):
    permList.append(perm)
permList.sort()
# for wiggle in permList:
#     print(str(permList.index(wiggle)) + " : " + str(wiggle))

# Check if a particular partition is constant-sum
count = 0
for part in partList:
    if len(part) > 1:
        for perm in permList:
            sumSet = checkConstant(n, part, perm)
            if len(sumSet) == 1:
                x = min(sumSet)
                cspList.append(csp(n, len(part), min(sumSet), part, perm))
                # print(str(count) + " : " + 'n : %03d' % n + ", p : " + str(len(part)) + ", part : " + str(part) +" : " + str(perm) + " : " + str(x))

# Print Results
print(str(list(itertools.combinations(numList, 2))))
# if len(partList) > 0:
#     print("Partitions of " + str(n) + " tested : " + str(partList))
# if len(cspList) > 0:
#     print("Non-obvious constant-sum-partitions of " + str(n) + ":")
# else:
#     print("Provided number has no non-obvious constant-sum-partitions.")
# for const in cspList:
#     count += 1
#     print(str(count) + " : " + const.to_string())
