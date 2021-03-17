#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
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
        return numbers

class InsertionSort(SortingAlgorithm):
    name = "Insertion Sort"
    def sort(self, numbers):
        for i in range(1, len(numbers)):
            index = numbers[i]
            j = i-1
            while j > 0 and numbers[j-1] > index:
                numbers[j] = numbers[j-1]
                j=j-1
            numbers[j+1] = index
        return numbers

class MergeSort(SortingAlgorithm):
    name = "Merge Sort"
    def __init__(self):
        pass
    def sort(self, numbers):
        if len(numbers) > 1:
            middle = int(len(numbers) / 2)        
            left = numbers[:middle]
            right = numbers[middle:]
            self.sort(left)
            self.sort(right)
            a = 0
            b = 0
            c = 0
            while a < len(left) and b < len(right):
                if left[a] < right[b]:
                    numbers[c] = left[a]
                    a+=1
                else:
                    numbers[c] = right[b]
                    b+=1
                c+=1
            while a < len(left):
                numbers[c] = left[a]
                a+=1
                c+=1
            while b < len(right):
                numbers[c] = right[b]
                b+=1
                c+=1
        return numbers

class QuickSort(SortingAlgorithm):
    name = "Quick Sort"
    def __init__(self):
        pass
    def sort(self, numbers):
        pass
    #def quicksort(self, left, right):
        #if right - left <= 0
                        

class PrintSorter():
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def printit(self, numbers, print_numbers):
        print("===========")
        print("{0}".format(self.algorithm.name))
        if print_numbers:
            print("===========")
            print(numbers)
        
        start_time = time.time()
        self.algorithm.sort(numbers)
        end_time = time.time()
        
        if print_numbers:
            print(numbers)
            print("===========")
            print("Elapsed time: {} seconds".format(end_time - start_time))
            print("===========")
        else:
            print("Elapsed time: {} seconds".format(end_time - start_time))

nums = []

def generate_numbers(length):
    nums = []
    for i in range(0, length):
        nums.append(random.randint(1, 100000))
    return nums

if __name__ == "__main__":
    #numbers = [ 103, 3, 3, 23, 1, 89, 46, 2 ]

    algorithms = []
    algorithms.append(BubbleSort())
    algorithms.append(InsertionSort())
    algorithms.append(MergeSort())
    for algorithm in algorithms:
        numbers = generate_numbers(1000)
        ps = PrintSorter(algorithm)
        ps.printit(numbers, False)
    
    sys.exit(0)
