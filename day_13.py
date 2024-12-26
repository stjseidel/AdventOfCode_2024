#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 06:32:12 2023

@author: stjse
"""

from aoc_class import AOC
from timeit import default_timer as timer
import re
import pandas as pd
import numpy as np
from scipy.optimize import linprog
# import sympy 
from sympy import symbols
from sympy.solvers.diophantine import diophantine
    
class Today(AOC):
        
    def parse_lines(self, file_path=''):
        lines = self.lines
        blocks = [self.lines[i:i+3] for i in range(0, len(self.lines), 4)]
        systems = []
        for block in blocks:
            system = {}
            X1 = int(re.search(r'X\+(\d+)', block[0])[1])
            X2 = int(re.search(r'X\+(\d+)', block[1])[1])
            Y1 = int(re.search(r'Y\+(\d+)', block[0])[1])
            Y2 = int(re.search(r'Y\+(\d+)', block[1])[1])
            Z1 = int(re.search(r'X=(\d+)', block[2])[1])
            Z2 = int(re.search(r'Y=(\d+)', block[2])[1])
            system = {'X1': X1, 'X2':X2, 'Y1':Y1, 'Y2':Y2, 'Z1':Z1, 'Z2':Z2}
            systems.append(system)
        self.systems = systems
        
        
        return lines
    
    def part1(self):
        lines = self.parse_lines()        
        df = pd.DataFrame(self.systems)
        # for system in self.systems:
        #     self.solve_brute(system)
        results = [self.solve_brute(sys) for sys in self.systems]
        # results = df.apply(self.solve_system, axis=1)
        
        # for i in range(1, 5400//67):
        #     print (i, (5400 - (67*i)) % 34 == 0)
        
        # for i in range(1,8400//22):
        #     print (i, (8400- (22*i)) % 94 == 0)
        
        
        
        self.result1 = sum(results)
        self.time1 = timer()
        return self.result1
    
    def solve_brute(self, system, simple=True):
        X1 = system['X1']
        X2 = system['X2']
        Y1 = system['Y1']
        Y2 = system['Y2']
        Z1 = system['Z1']
        Z2 = system['Z2']
        
        if simple:
            solutions_X = set([i for i in range(0, min(100, Z1//X2)) if ((Z1 - (X2*i)) % X1 == 0)])
            solutions_Y = set([i for i in range(0, min(100, Z2//Y2)) if ((Z2 - (Y2*i)) % Y1 == 0)])
        else:
            solutions_X = set([i for i in range(0, Z1//X2) if ((Z1 - (X2*i)) % X1 == 0)])
            solutions_Y = set([i for i in range(0, Z2//Y2) if ((Z2 - (Y2*i)) % Y1 == 0)])
        # solutions = solutions_X & solutions_Y
        solutions = solutions_X.union(solutions_Y)
        if len(solutions) == 0:
            
            return 0
        if len(solutions) > 1:
            pass
        
        # costs = [sol + 3 * ((Z1 - sol*X2) // X1) for sol in solutions]
        # return min(costs)
        costs = []
        for sol in solutions:
            B = sol
            A = (Z1 - B*X2) // X1
            
            if (Z2 - (A*Y1) - B*Y2 == 0) and (Z1 - (A*X1) - B*X2 == 0):
                if simple:
                    if (A < 100 and B < 100) and (A > 0 and B > 0):
                        cost = A*3 + B
                        costs.append(cost)
                        # print(cost, A, B, system)
                else:
                    if (A > 0 and B > 0):
                        cost = A*3 + B
                        costs.append(cost)
                        # print(cost, A, B, system)
        if len(costs) == 0:
            return 0
        return min(costs)
   
         
    @staticmethod
    def solve_system(row):
        bounds = [(0, None), (0, None)]
        coefficients = np.array([[row['X1'], row['Y1']], [row['X2'], row['Y2']]])
        result = np.array([row['Z1'], row['Z2']])
        # try:
        #     solution = np.linalg.solve(coefficients, result)
        #     return pd.Series({'a': solution[0], 'b': solution[1]})
        # except np.linalg.LinAlgError:
        #     return pd.Series({'a': None, 'b': None})
        x, y, z = symbols("x, y, z", integer=True)
        diophantine(row['X1']*x + row['X2']*y  - row['Z1'])
        
        objective = [0, 0]
        res = linprog(objective, A_eq=coefficients, b_eq=result, bounds=bounds, method='highs')
        
        if res.success:
            solution = res.x
            if np.all(np.abs(solution - np.round(solution)) < 1e-6):
                integer_solution = np.round(solution).astype(int)
                print("Integer solution:", integer_solution)
            else:
                print("No integer solution exists.")
        else:
            print("No feasible solution found.")
            
    def part2(self):
        _ = self.parse_lines()
        # df = pd.DataFrame(self.systems)
        for i, system in enumerate(self.systems):
            self.systems[i]['Z1'] += 10000000000000
            self.systems[i]['Z2'] += 10000000000000
        # for system in self.systems:
        #     self.solve_brute(system)
        results = [self.solve_brute(sys, simple=False) for sys in self.systems]
        # results = df.apply(self.solve_system, axis=1)
        
        # for i in range(1, 5400//67):
        #     print (i, (5400 - (67*i)) % 34 == 0)
        
        # for i in range(1,8400//22):
        #     print (i, (8400- (22*i)) % 94 == 0)
        
        
        
        self.result2 = sum(results)
        self.time2 = timer()
        return self.result2
        
    def print_final(self):
        print(f'Part 1 result is: {self.result1}. (time: {round(self.time1 - self.beginning_of_time, 2)})')
        print(f'Part 2 result is: {self.result2} (time: {round(self.time2 - self.time1, 2)})')
        

if __name__ == '__main__':
# prep
    today = Today(day='', simple=True)
    today.create_txt_files()

# simple part 1
    today.set_lines(simple=True)
    today.part1()
    print(f'Part 1 <SIMPLE> result is: {today.result1}')
    
# hard part 1
    today.set_lines(simple=False)
    today.part1()
    print(f'Part 1 <HARD> result is: {today.result1}')
    today.stop()


# =============================================================================
# # simple part 2
#     today.set_lines(simple=True) 
#     today.part2()
#     print(f'Part 2 <SIMPLE> result is: {today.result2}')
# =============================================================================

# =============================================================================
# # hard part 2
#     today.set_lines(simple=False)
#     today.part2()
#     print(f'Part 2 <HARD> result is: {today.result2}')
#     today.stop()
#     today.print_final()
# =============================================================================

