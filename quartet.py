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

numList = [8, 9, 10, 19, 20, 21, 22, 23]
n = len(numList)
print(str(findFourElements(numList, 24, 18)))
