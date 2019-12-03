#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

class FibonacciBase:
    def __init__(self):
        self.name = "Not set"
    def fib(self):
        pass

class FibonacciSimple(FibonacciBase):
    def __init__(self, depth):
        self.name = "Fibonacci - Naive"
        self.depth = depth
    def fib(self):
        return self.fibcalc(self.depth)
    def fibcalc(self, n):
        if n <= 2:
            return 1
        else:
            return self.fibcalc(n-1) + self.fibcalc(n-2)

class FibonacciRecursiveMemorization(FibonacciBase):
    def __init__(self, capacity):
        self.memory = [0 for a in range(capacity+1)]
        self.capacity = capacity
        self.name = "Fibonacci Recursive Memorization"
    def fib(self):
        return self.fibcalc(self.capacity)
    def fibcalc(self, n):
        if self.memory[n]:
            return self.memory[n]
        if n <= 2:
            self.memory[n] = 1
        else:
            self.memory[n] = self.fibcalc(n-1) + self.fibcalc(n-2)
        return self.memory[n]

class FibonacciBottomUpOptimizedRuntime(FibonacciBase):
    def __init__(self, capacity):
        self.memory = [0 for a in range(capacity+1)]
        self.name = "Fibonacci Bottom Up - Optimized runtime"
    def fib(self):
        for i in range(0, len(self.memory)):
            if i == 0:
                self.memory[i] = 0
            elif i <= 2:
                self.memory[i] = 1
            else:
                self.memory[i] = self.memory[i-1] + self.memory[i-2]
        return self.memory[len(self.memory)-1]

class FibonacciBottomUpOptimizedSpace(FibonacciBase):
    def __init__(self, capacity):
        self.memory = [0 for a in range(capacity + 1)]
        self.name = "Fibonacci Bottom Up - Optimized space"
    def fib(self):
        first = 0
        second = 0
        for i in range(1, len(self.memory)):
            if i == 1:
                second = 1
            else:
                first, second = second, first + second
        return second

if __name__ == "__main__":
    depth = 20
    fibalgorithms = []
    fibalgorithms.append(FibonacciSimple(depth))
    fibalgorithms.append(FibonacciRecursiveMemorization(depth))
    fibalgorithms.append(FibonacciBottomUpOptimizedRuntime(depth))
    fibalgorithms.append(FibonacciBottomUpOptimizedSpace(depth))
    
    print("Calculate Fibonacci with depth: {}".format(depth))
    print()
    for fa in fibalgorithms:
        print("Using {}".format(fa.name))
        print(fa.fib())
        print()

    print("Done.")
    print()
    sys.exit(0)
