#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse
import itertools
import math

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

def calcGroups(calcTop, calcBottom):
    tempCalc = math.factorial(calcTop)
    for h in calcBottom:
        tempCalc /= math.factorial(h)
    return tempCalc
n = 24
part = [2, 2, 2, 2, 2, 2, 2, 2, 4, 4]
numGroup = int(calcGroups(n, part))
numList = list(range(1, n+1))
partSet = set()
groupSet = set()
# it = all_combs(numList, part)
# for i in range(numGroup):
#     del(groupSet)
#     groupSet = set()
#     for g in next(it):
#         groupSet.add(frozenset(g))
#         # print(list(g))
#     partSet.add(frozenset(groupSet))
print(str(numGroup))
