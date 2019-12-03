#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def max(a, b):
    if a > b:
        return a
    else:
        return b

def knapsack(capacity, weight_of_items, values, n):
    the_knapsack = [[0 for a in range(max_capacity_of_knapsack+1)] for b in range(n+1)]
    for i in range(0, n+1):
        for j in range(0, capacity+1):
            if i == 0 or j == 0:
                the_knapsack[i][j] = 0
            elif weight_of_items[i-1] <= j:
                the_knapsack[i][j] = max( \
                    values[i-1] + \
                    the_knapsack[i-1][j-weight_of_items[i-1]] \
                    , \
                    the_knapsack[i-1][j] \
                )
            else:
                the_knapsack[i][j] = the_knapsack[i-1][j]
    return the_knapsack[n][max_capacity_of_knapsack]

if __name__ == "__main__":
    values = [60, 100, 120]
    weight_of_items = [10, 20, 30]
    max_capacity_of_knapsack = 50
    
    print("the_knapsacknapsack solution: {0}".format( \
        knapsack( \
            max_capacity_of_knapsack, \
            weight_of_items, \
            values, \
            len(values) \
        )  \
    ))

    print("Done.")
    sys.exit(0)
