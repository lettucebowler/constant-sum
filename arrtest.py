#!/usr/bin/env python3
import os;
import sys
import argparse

# Parser to get base number for computations
parser = argparse.ArgumentParser(description='A parser')
parser.add_argument("-n", dest='number', default=2, help='number to partition', type=int)
args = parser.parse_args();
n = args.number

if n % 2 == 0:
    numList = list(range(n))
    numArray = list()
    tempList = list()
    for x in range(len(numList) // 2):
        del tempList
        tempList = list()
        tempVal = numList.pop(0)
        tempList.append(tempVal)
        if n - tempVal in numList:
            tempList.append(n - tempVal)
        else:
            tempList.append("x")
        numArray.append(tempList)
    del tempList
    tempList = list()
    tempList.append("x")
    tempList.append(n // 2)
    numArray.append(tempList)
    del numList

    for row in numArray:
        print(str(row))
else:
    print("Program only designed for even numbers")
