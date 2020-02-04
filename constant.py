#!/usr/bin/env python3
import os;
import sys
import subprocess;
import argparse
import itertools
import math
import random

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

# https://www.geeksforgeeks.org/find-four-numbers-with-sum-equal-to-given-sum/
# This code is contributed by shreyanshi_arun
# This code if modified by Grant Montgomery
# A naive solution to print all combination
# of 4 elements in A[] with sum equal to X
def findFourElements(A, total, X, groupIndex, parts):
    tempList = list()
    a = len(A)
    B = list()

    # Fix the first element and find
    # other three
    for i in range(0,a-3):

        # Fix the second element and
        # find other two
        for j in range(i+1,a-2):

            # Fix the third element
            # and find the fourth
            for k in range(j+1,a-1):

                # find the fourth
                for l in range(k+1,a):
                    tempList = [A[i], A[j], A[k], A[l]]
                    if sum(tempList) % total == X:
                        for tempVal in tempList:
                            A.remove(tempVal)
                        return tempList
                    else:
                        del tempList
                        tempList = list()
    return tempList


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

    # for each grouping in a partition:
    #   1. If the groupings in the partition are all equal:
    #     a. fill each grouping with pairs that sum to (g * 2 / |grouping|) (MOD n)
    #   2. If the grouping = 2 (MOD 4)
    #     a. add a pair that sums to g
    #     b. fill the rest of the grouping with groups of 4 that add to 0 (MOD 16), such that when possible, no pair from the quartet sums to 0 (MOD 16)
    #   3. if the grouping = 0 (MOD 4)
    #     a. first fill the grouping with a quartet that sums to g (MOD n)
    #     b. for any remaining spots in the grouping, fill it with quartets that sum to 0 (MOD n)


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
    # return groupList


        # print(str(part) + " " + str(numList))

        # temp = list()
        # for fill in range(len(part)):
        #     if fill == len(part) - 1:
        #             groupList[-1] += numList
        #     else:
        #         if len(groupList[fill]) < part[fill]:
        #     # Add to groupList[fill] in groups of 2 that sum to 0 (MOD N)
        #             if part[fill] % 4 == 0:
        #                 for gah in range(part[fill] // 2 - 1):
        #                     if len(numList) > 0:
        #                         print(str(numList))
        #                         # print(str(groupList[fill]) + " " +    str(part[fill]))
        #                         del temp
        #                         temp = smallestNSum(numList, n, 0)
        #                         for el in temp:
        #                             groupList[fill].append(el)
        #     # Add to groupList[fill] in groups of 4 that sum to 0 (MOD N)
        #             else:
        #                 for guh in range(part[fill // 4 ]):
        #                     if len(numList) > 1 and len(groupList[fill])  < part[fill]:
        #                         temp = list()
        #                         curNum1 = 0
        #                         curNum2 = 0
        #                         while len(temp) == 0:
        #                             tempTotal = 0
        #                             del temp
        #                             temp = list()
        #                             curNum1 = random.choice(numList)
        #                             curNum2 = random.choice(numList)
        #                             while curNum2 == curNum1:
        #                                 curNum2 = random.choice(numList)
        #                             tempTotal = curNum1 + curNum2
        #                             tempList = list()
        #                             for e in numList:
        #                                 if e != curNum1 and e != curNum2:
        #                                     tempList.append(e)
        #                             temp = smallestNSum(tempList, n, (total - tempTotal) % n)
        #                         temp.append(curNum1)
        #                         temp.append(curNum2)
        #                         print(str(curNum1) + " " + str(curNum2))
        #                         print(str(temp) + " " + str(numList))
        #                         for u in temp:
        #                             numList.remove(u)
        #                         groupList[fill] += temp

                                # print(str(numList))
                                # del temp
                                # temp = list()
                                # tempSum = 0
                                # curNum = random.choice(numList)
                                # groupList[fill].append(curNum)
                                # numList.remove(curNum)
                                # tempSum += curNum
                                # curNum = random.choice(numList)
                                # groupList[fill].append(curNum)
                                # numList.remove(curNum)
                                # tempSum += curNum
                                # print(str(tempSum))
                                # temp = smallestNSum(numList, n, total - tempSum % n)
                                # print(str(temp))
                                # for el in temp:
                                #     groupList[fill].append(el)




        # for y in groupList:










    # if len(groupList[0]) == 0:
    # #     for y in range(total):
    # #         del group
    # #         group = list()
    # #         groupList.append(group)
    # #         if (g + y) % total in numList and total - y in numList and g + y != total - y:
    # #             if y < len(part):
    # #                 if len(groupList[y]) == 0 and g + y < (g + total) / 2:
    # #                     groupList[y].append((g + y) % total)
    # #                     groupList[y].append(total - y)
    #
    #
    #     for a in range(len(part)):
    #         v = groupList[a]





    #         groupList = groupList[:len(part)]
    #         for get in groupList:
    #             if len(get) == 0:
    #                 temp = numList[0]
    #                 get.append(temp)
    #                 get.append(g - temp)
    #                 numList.remove(temp)
    #                 numList.remove(g - temp)

    #     for set in groupList:
    #         for item in set:
    #             if item in numList:
    #                 numList.remove(item)

    #     for z in range(len(groupList)):
    #         if part[z] > 2:
    #             group = groupList[z]
    #             for h in numList:
    #                 if len(group) < part[z]:
    #                     if (total - h) in numList and (total - h) != h:
    #                         group.append(h)
    #                         group.append(total - h)
    #                         numList.remove(h)
    #                         numList.remove(total - h)
    #                     if z == len(groupList) - 1:
    #                         for b in numList:
    #                             groupList[z].append(b)

    # Validate results before returning
    # groupList.sort(key=len)
    checkList = list()
    good = list()
    # groupList.sort(key=len)
    for k in groupList:
        k.sort()
        for l in k:
            if l not in checkList:
                checkList.append(l)
            elif "duplicates" not in good:
                good.append("duplicates")

        G = sum(k)

        if G % total != g and "sum" not in good:
            good.append("sum")

    for h in range(len(part)):
        if len(groupList[h]) != part[h] and "length" not in good:
            good.append("length")
    # Append a list of the
    if len(good) != 0:
        groupList.append(good)
    return groupList

# ----------------------------Main Program------------------------------------ #
partList = list()
partCount = 0

# Exit if n is odd.
if n % 2 == 1:
    print("This program is only designed for even numbers.")
    exit()

# Populate partition list and filter out irrelevant partitions.
for part in partition(n):
    partCount += 1
    partList.append(part)
partList.sort(reverse=True, key=len)

# Calculate a csp for each partition and possible sum
sumList = list()
cspList = list()
count = 0
# partList = [[2, 2, 6, 6]]
for part in partList:
    # if True:
    if len(part) % 2 == 0:
        del sumList
        sumList = findPossibleSums(n, len(part))
        # sumList = [6]
        if len(sumList) > 0:
            for possibleSum in sumList:
                csp = list(genConstantSumPartition(n, part, possibleSum))
                cspList.append(constantSumPartition(n, possibleSum, len(part),  part, csp))
                # else:
                #     print("Algorithm Failure")
                #     exit()

# Output data
for const in cspList:
    print(const.to_string())
