#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 06:32:12 2023

@author: stjse
"""

from aoc_class import AOC
from timeit import default_timer as timer
from itertools import product

    
class Today(AOC):
        
    def parse_lines(self, file_path=''):
        lines = self.lines
        self.lines = {int(line.split(':')[0]): [int(val) for val in line.split(':')[1].strip().split(' ')] for line in lines}
        # lines = [[int(lin) for lin in line.split(' ') if set(lin) != set('') ] for line in lines]
        return self.lines
    
    def part1(self):
        lines = self.parse_lines()
        self.operations = ['+', '*']
        self.result1 = self.check_operations()
        self.time1 = timer()
        return self.result1

    def check_operations(self, operations=None):
        operations = operations or self.lines
        lines_result = 0
        for result, values in operations.items():
            lines_result += self.check_operation(result, values)
        return lines_result

    def part2(self):
        lines = self.parse_lines()
        self.operations = ['+', '*', '||']
        self.result2 = self.check_operations()
        self.time2 = timer()
        return self.result2

    def check_operation(self, result, values):
        combos = product(self.operations, repeat=len(values)-1)
        for combo in product(self.operations, repeat=len(values)-1):
            line_result = 0
            for i, value in enumerate(values):
                if i == 0:
                    line_result = value
                elif combo[i-1] == '||':
                    line_result = int(str(line_result) + str(values[i]))
                else:
                    line_result = eval(f'{line_result} {combo[i-1]} {value}')
            if line_result == result:
                return result
        return 0
            
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

# simple part 2
    today.set_lines(simple=True) 
    today.part2()
    print(f'Part 2 <SIMPLE> result is: {today.result2}')

# hard part 2
    today.set_lines(simple=False)
    today.part2()
    print(f'Part 2 <HARD> result is: {today.result2}')
    today.stop()
    today.print_final()