#!/usr/bin/python
import os;
import sys
import subprocess;
import argparse

parser = argparse.ArgumentParser(description='A parser')
parser.add_argument("--n", default=2, help='the number to partition', type=int)
args = parser.parse_args();
n = args.n

# Returns a set of all partitions of number, made up of only even numbers.
# If number is odd, returns an empty set.
def partition(number):
    answer = set()
    if(number % 2 == 0):
        answer.add((number, ))
        for x in range(2, number):
            for y in partition(number - x):
                if(x % 2 == 0):
                    answer.add(tuple(sorted((x, ) + y)))
    return answer

# Checks if a partition is constant-sum, and returns boolean.
def checkConstant():
    print("Hello from checkConstant!")

answer = partition(n)
print answer
