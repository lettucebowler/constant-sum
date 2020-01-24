#!/usr/bin/env python3
import os;
import sys
import subprocess;
import argparse
import itertools

def F(seq, parts, indexes=None, res=[], cur=0):
    if indexes is None: # indexes to use for combinations
        indexes = range(len(seq))

    if cur >= len(parts): # base case
        yield [[seq[i] for i in g] for g in res]
        return

    for x in itertools.combinations(indexes, r=parts[cur]):
        set_x = set(x)
        new_indexes = [i for i in indexes if i not in set_x]
        for comb in F(seq, parts, new_indexes, res=res + [x], cur=cur + 1):
            yield comb

n = 8
part = [2, 3, 3]
numList = list(range(1, 8))
it = F(numList, part)
# for i in range(10):
curTotal = n
numGroups = 0:
for s in part:

for g in next(it):
    print(g, end='')
print('')
