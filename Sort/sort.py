#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import random

class SortingAlgorithm:
    name = "Not set"
    def __init__(self):
        pass
    def sort(self):
        pass

class BubbleSort(SortingAlgorithm):
    name = "Bubble Sort"
    def __init__(self):
        pass
    def sort(self, numbers):
      for i in range(len(numbers), -1, -1):
            for j in range(1, i):
                if numbers[j-1] > numbers[j]:
                    numbers[j-1], numbers[j] = \
                    numbers[j], numbers[j-1]

class InsertionSort(SortingAlgorithm):
    name = "Insertion Sort"
    def sort(self, numbers):
        for i in range(1, len(numbers)):
            index = numbers[i]
            j = i
            while j > 0 and numbers[j-1] > index:
                numbers[j] = numbers[j-1]
                j=j-1
            numbers[j] = index

class PrintSorter():
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def printit(self, numbers):
        print("===========")
        print("{0}".format(self.algorithm.name))
        print("===========")
        print(numbers)
        self.algorithm.sort(numbers)
        print(numbers)

nums = []

def generate_numbers(length):
    for i in range(0, length):
        nums.append(random.randint(1, 1000))
    return nums

if __name__ == "__main__":
    #numbers = [ 103, 3, 3, 23, 1, 89, 46, 2 ]

    algorithms = []
    algorithms.append(BubbleSort())
    algorithms.append(InsertionSort())
    
    for algorithm in algorithms:
        numbers = generate_numbers(5)
        ps = PrintSorter(algorithm)
        ps.printit(numbers)
    
    sys.exit(0)
