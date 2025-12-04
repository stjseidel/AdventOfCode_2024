#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 06:32:12 2023

@author: stjse
"""

from aoc_class import AOC
from timeit import default_timer as timer
import re


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
        results = [self.solve_hard(sys) for sys in self.systems]
        self.result1 = sum(results)
        self.time1 = timer()
        return self.result1

    def part2(self):
        _ = self.parse_lines()
        for i, system in enumerate(self.systems):
            self.systems[i]['Z1'] += 10000000000000
            self.systems[i]['Z2'] += 10000000000000
        results = [self.solve_hard(sys) for sys in self.systems]

        self.result2 = sum(results)
        self.time2 = timer()
        return self.result2

    def solve_hard(self, system):
        X1 = system['X1']
        X2 = system['X2']
        Y1 = system['Y1']
        Y2 = system['Y2']
        Z1 = system['Z1']
        Z2 = system['Z2']
        denominator = X1 * Y2 - Y1 * X2
        if denominator == 0:
            return 0  # No unique solution

        b_numerator = X1 * Z2 - Y1 * Z1
        a_numerator = Z1 * Y2 - Z2 * X2

        if b_numerator % denominator != 0 or a_numerator % denominator != 0:
            return 0  # No integer solution

        B = b_numerator // denominator
        A = a_numerator // denominator

        if A < 0 or B < 0:
            return 0  # No non-negative solution

        return A * 3 + B

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
# simple part 2
    today.set_lines(simple=True) 
    today.part2()
    print(f'Part 2 <SIMPLE> result is: {today.result2}')
# =============================================================================

# =============================================================================
# hard part 2
    today.set_lines(simple=False)
    today.part2()
    print(f'Part 2 <HARD> result is: {today.result2}')
    today.stop()
    today.print_final()
# =============================================================================
