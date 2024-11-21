#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import yaml

from ortools.linear_solver import pywraplp

def solveit():

    # 0. Read settings
    with open(r'settings.yml') as file:
        settings = yaml.load(file, Loader=yaml.FullLoader)
        data_sm = settings['entity1']
        data_bm = settings['entity2']
        data_hm = settings['entity3']

    # 1. Solver
    solver = pywraplp.Solver(
            'Maximize army power', 
            pywraplp.Solver.GLOP_LINEAR_PROGRAMMING
    )

    # 2. Variables
    swordsmen = solver.IntVar(0, solver.infinity(), data_sm[0])
    bowmen = solver.IntVar(0, solver.infinity(), data_bm[0])
    horsemen = solver.IntVar(0, solver.infinity(), data_hm[0])

    # 3. Constraints
    # Food
    solver.Add(swordsmen*data_sm[1] + bowmen*data_sm[2] + horsemen*data_sm[3] <= data_sm[4])
    
    # Wood
    solver.Add(swordsmen*data_bm[1] + bowmen*data_bm[2] <= data_bm[3])
    
    # Gold
    solver.Add(bowmen*data_hm[1]+ horsemen*data_hm[2] <= data_hm[3])

    # 4. Objective (maximize) ax + bx + cz + d
    solver.Maximize(swordsmen*70 + bowmen*95 + horsemen*230)

    # 5. Optimize
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print('================= Solution =================')
        print(f'Solved in {solver.wall_time():.2f} milliseconds in {solver.iterations()} iterations')
        print()
        print(f'Optimal power = {solver.Objective().Value():.2f} 💪power')
        print('Army:')
        print(f' - 🗡️{data_sm[0]} = {swordsmen.solution_value():.2f}')
        print(f' - 🏹{data_bm[0]} = {bowmen.solution_value():.2f}')
        print(f' - 🐎{data_hm[0]} = {horsemen.solution_value():.2f}')
    else:
        print('The solver could not find an optimal solution.')

if __name__ == "__main__":    
    print("Start it:")
    
    solveit()

    print("Done.")
    sys.exit(0)

