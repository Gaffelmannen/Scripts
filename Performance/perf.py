#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from time import perf_counter as pc

def benchmark():
    MAX = 1000001
    #MAX = 1001
    model_name = input("Model name: ")

    while True:
        tic = pc()

        for n in range(MAX):
            print("\033c")
            print(n)
    
        toc = pc()

        elapsed = round(toc-tic, 4)

        print()
        print(model_name, elapsed, "seconds")
        print()
        sys.exit(0)

if __name__ == "__main__":
    benchmark()
    #print("Hej")
