#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import numpy as np

N = 10

grid = np.random.randint(2, size=(N, N))


print('\033[H\033[J')

for t in range(100):

    next_grid = np.zeros(grid.shape)

    for i in range(len(grid)):
        for j in range(len(grid[i])):

            if grid[i, j] == 1:
                print('*'),
            else:
                print(' '),

            count = -grid[i,j]
            for k in (-1,0,1):
                for l in (-1,0,1):
                    count = count + grid[(i+k)%N,(l+j)%N]

            if count == 3:
                next_grid[i,j] = 1
            if grid[i,j] == 1 and count == 2:
                next_grid[i,j] = 1

        print('')

    time.sleep(0.2)

    grid = next_grid

    print('\033[H\033[J')
