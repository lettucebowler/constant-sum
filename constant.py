#!/usr/bin/env python3
import os;
import sys
import argparse

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
        i = 0
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
                i += 1
                yield a[:k + 1]

# n : number program is checking
# part : partition of n to check for potential sums
def findPossibleSums(n, p):
    potentialSumList = list(range(1, n))
    sumList = list()

    # Check each value in potentialSumList for validity as a constant sum
    # If valid, add it to sumList
    for g in potentialSumList:
        if g * p % n == n/2:
            sumList.append(g)

    return sorted(sumList)

# Storage object for csp data
class constantSumPartition():
    def __init__(self, n, g, p, part, csp):
        self.n = n
        self.p = p
        self.g = g
        self.part = part
        self.csp = csp

    def to_string(self):
        message = "n:" + str(self.n) + " g:" + str(self.g) + " p:" + str(self.p) + " part:" + str(self.part) + " csp:" + str(const.csp)
        # message += str(const.csp)
        return(message)

# Create a constant-sum-partition from supplied partition
def genConstantSumPartition(total, part, g):
    groupList = list()
    group = list()
    lista = list()
    listb = list()
    numList = list(range(total))
    allSame = False

    # Populate groupList with empty lists
    del group
    group = list()
    for i in range(len(part)):
        groupList.append(list())

    # Check for trivial case where all p in P are equal
    if all(elem == part[0] for elem in part):
        allSame = True

    # Determine spot to split list
    if allSame:
        testValue = g * 2 // part[0]
    else:
        testValue = g
    # Split numList into two lists containing pairs summing to g (MOD P)
    for j in numList:
        if j > testValue:
            if j not in lista or j not in listb:
                listb.append(j)
        else:
            if j not in lista or j not in listb:
                lista.append(j)

    # Populate each p in P with a pair that sums to g (MOD n)
    for numeral in range(len(part) - 1):
        if allSame:
            limit = part[0] // 2
        elif part[numeral] % 4 == 2:
            limit = 1
        else:
            limit = 0
        for round in range(limit):
            if len(lista) >= 2:
                groupList[numeral].append(lista.pop(0))
                groupList[numeral].append(lista.pop())
            else:
                if len(listb) >= 2:
                    groupList[numeral].append(listb.pop(0))
                    groupList[numeral].append(listb.pop())

    # Combine the remaining elements in lista and listb back into numList
    numList = lista + listb
    numList.sort()

    # Add quartets to each grouping until they are the correct size for given
    # partition.

    quartList = list()
    for integer in range(len(part) - 1):
        if part[integer] % 4 == 0 and len(groupList[integer]) < part[integer]:
            # Add a quartet that sums to g (MOD n)
            quartList = list(findFourElements(numList, n, g, integer, len(part)))
            for v in quartList:
                groupList[integer].append(v)
        if part[integer] > 4:
            for schloop in range((part[integer] - len(groupList[integer])) // 4):
            # while len(groupList[integer]) < part[integer]:
                # Add a quartet that sums to 0 (MOD n)
                quartList = list(findFourElements(numList, n, 0, integer, len(part)))
                if len(quartList) == 0:
                    break
                for v in quartList:
                    groupList[integer].append(v)

    # Add the rest of the numbers in numList to the final grouping, because if
    # if the other groupings are all constant-sum, the remaining numbers are
    # guaranteed to be constant-sum as well.
    groupList[-1] += numList
    del numList

    # Validate results before returning
    checkList = list()
    good = list()
    groupList.sort(key=len)
    for k in groupList:

        # Check for Duplicates in csp
        k.sort()
        for l in k:
            if l not in checkList:
                checkList.append(l)
            elif "duplicates" not in good:
                good.append("duplicates")

        # Check that all groupings add up to g (MOD n)
        G = sum(k)
        if G % total != g and "sum" not in good:
            good.append("sum")

    # Check that each grouping is the write size for given partition of n
    for h in range(len(part)):
        if len(groupList[h]) != part[h] and "length" not in good:
            good.append("length")

    # Append a list of the errors found to the csp list
    if len(good) != 0:
        groupList.append(good)
    return groupList

# Exit if n is odd.
if n % 2 == 1:
    print("This program is only designed for even numbers.")
    exit()

# Populate partition list and filter out irrelevant partitions.
partList = list()
for part in partition(n):
    partList.append(part)
partList.sort(reverse=True, key=len)

# Calculate a csp for each partition and possible sum
sumList = list()
cspList = list()
count = 0
# partList = [[2, 2, 6, 6]]
for part in partList:
    del sumList
    sumList = findPossibleSums(n, len(part))
    # sumList = [6]
    if len(sumList) > 0:
        for possibleSum in sumList:
            csp = list(genConstantSumPartition(n, part, possibleSum))
            cspList.append(constantSumPartition(n, possibleSum, len(part), part, csp))

# Output data
for const in cspList:
    if len(const.csp) > const.p:
        print(const.to_string())
