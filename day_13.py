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
        results = df.apply(self.solve_system, axis=1)
        self.result1 = 'TODO'
        self.time1 = timer()
        return self.result1
    
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
        lines = self.parse_lines()
        self.result2 = 'TODO'
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
    
# =============================================================================
# # hard part 1
#     today.set_lines(simple=False)
#     today.part1()
#     print(f'Part 1 <HARD> result is: {today.result1}')
#     today.stop()
# =============================================================================


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