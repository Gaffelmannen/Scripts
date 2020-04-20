#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import yaml

class KnapsackSolver:
    def __init__(self):
        pass

    def max(self, a, b):
        if a > b:
            return a
        else:
            return b

    def solve(self, capacity, weight_of_items, values, n):
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
    with open(r'settings.yml') as file:
        settings = yaml.load(file, Loader=yaml.FullLoader)
        values = settings['values']
        weight_of_items = settings['weights']
        max_capacity_of_knapsack = settings['max_cap']
    ks = KnapsackSolver()
    print("the_knapsacknapsack solution: {0}".format( \
        ks.solve( \
            max_capacity_of_knapsack, \
            weight_of_items, \
            values, \
            len(values) \
        )  \
    ))

    print("Done.")
    sys.exit(0)

