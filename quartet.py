#!/usr/bin/env python3
import os;
import sys
import subprocess;
import argparse
import itertools
import math
import random

def findFourElements(A, total, X):
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

def getSumpairs(total, part, g):
    groupList = list()
    group = list()
    lista = list()
    listb = list()
    numList = list(range(total))
    allSame = False

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
    for numeral in range(total // 2 - 1):
        groupList.append(list())
        if len(lista) >= 2:
            groupList[numeral].append(lista.pop(0))
            groupList[numeral].append(lista.pop())

        elif len(listb) >= 2:
                groupList[numeral].append(listb.pop(0))
                groupList[numeral].append(listb.pop())

    # Combine the remaining elements in lista and listb back into numList
    numList = lista + listb
    numList.sort()

    return groupList

def all_combs(seq, parts, indexes=None, res=[], cur=0):
    if indexes is None: # indexes to use for combinations
        indexes = range(len(seq))

    if cur >= len(parts): # base case
        yield [[seq[i] for i in g] for g in res]
        return

    for x in itertools.combinations(indexes, r=parts[cur]):
        set_x = set(x)
        new_indexes = [i for i in indexes if i not in set_x]
        for comb in all_combs(seq, parts, new_indexes, res=res + [x], cur=cur + 1):
            yield comb

n = 20
partition = [2, 2, 4, 4, 4, 4]
g = 15
numList = list(range(n))
pairList = getSumpairs(n, partition, g)
numPairs = len(pairList)
numChoose = 8
numTimes = math.factorial(numPairs) // math.factorial(numChoose) // math.factorial(numPairs - numChoose)
for a in pairList:
    for b in a:
        numList.remove(b)
print(str(pairList))
print(str(numList))

tempList = list()
quartet = list()
it = all_combs(pairList, [3])
count = 0
for z in range(1, numTimes + 1):
    for w in next(it):
        del tempList
        tempList = list()
        tempList += numList
        for y in w:
            tempList += y
        del quartet
        quartet = findFourElements(tempList, n, g)
        # print(str(findFourElements(tempList, n, g)))
        if len(quartet) > 0:
            if sum(quartet) % n == g and sum(tempList) % n == g:
                count += 1
                print(str(quartet) + " " + str(tempList))
print(str(count))
        # print(str(z) + " " + str(w))
