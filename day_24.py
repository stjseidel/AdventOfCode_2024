#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 06:32:12 2023

@author: stjse
"""

from aoc_class import AOC
from timeit import default_timer as timer
from collections import defaultdict
    
class Today(AOC):
        
    def parse_lines(self, file_path=''):
        lines = self.lines
        # lines = [[int(lin) for lin in line.split(' ') if set(lin) != set('') ] for line in lines]
        self.wires_base = defaultdict()
        split = lines.index('')
        wires, operations = [lines[:split], lines[split+1:]]
        for wire in wires:
            self.wires_base[wire.split(':')[0]] = int(wire.split(':')[1])
        self.operations = [[op for op in operation.split(' ') if op != '->'] for operation in operations]
        
        self.z_wires = []
        for op in self.operations:
            wires = [op[i] for i in [0, 2, 3]]
            for wire in wires:
                if wire[0] == 'z':
                    self.z_wires.append(wire)
        for z_wire in self.z_wires:
            if z_wire not in self.wires_base:
                self.wires_base[z_wire] = None
        self.wires_current = self.wires_base.copy()
        return lines
    
    
    
    def part1(self):
        lines = self.parse_lines()
        self.run_operations()
        # self.print_all_wires()
        self.result_decimal = int(self.result_binary, 2)
        self.result1 = self.result_decimal
        self.time1 = timer()
        return self.result1

    def run_operations(self):
        solved = False
        while not solved:
            for op in self.operations:
                self.run_op(*op)
                solved = self.is_solved()
                
    def run_op(self, in_one, op, in_two, output):
        for key in [in_one, in_two, output]:
            if key not in self.wires_current:
                self.wires_current[key] = None
        in_one = self.wires_current[in_one]
        in_two = self.wires_current[in_two]
        result = None
        if in_one is None or in_two is None:
            return None
        try:
            if op == 'XOR':
                result = in_one ^ in_two
            elif op == 'OR':
                result =  in_one or in_two
            elif op == 'AND':
                result = in_one and in_two
            self.wires_current[output] = result
        except ValueError:
            pass
        return result
        
    def get_result(self, kind='z'):
        values = {}
        values = [None] * sum([wire[0] == kind for wire in self.wires_current])
        for wire, value in self.wires_current.items():
            if wire[0] == kind:
                # print(wire, value)
                values[int(wire[1:])] = value
                # print(values)
        self.result_binary = ''.join([str(val) for val in values[::-1]])
        # print(f'binary: {self.result_binary}; decimal: {self.result_decimal}')
        
    def print_all_wires(self):
        wires_sorted = sorted(list(self.wires_current.keys()))
        for wire in wires_sorted:
            print(wire, self.wires_current[wire])
            
    def is_solved(self):
        for wire in self.z_wires:
            if self.wires_current[wire] is None:
                return False
        self.get_result()    
        
        return True
        
    def part2(self):
        lines = self.parse_lines()
        self.get_result(kind='x')
        x_binary = self.result_binary
        x_decimal = int(x_binary, 2)
        self.get_result(kind='y')
        y_binary = self.result_binary
        y_decimal = int(y_binary, 2)
        self.run_operations()
        self.get_result(kind='z')
        z_binary = self.result_binary
        z_decimal = int(y_binary, 2)
        
        print(f'{x_binary} + {y_binary} = {z_binary}')
        print(f'{x_decimal} + {y_decimal} = {z_decimal}')
        
        
        expected_result_binary = bin(x_decimal + y_decimal)[2:]
        
        print(f'expected: {expected_result_binary}; returned result: {z_binary}')
        expected_result_binary = str(expected_result_binary).zfill(len(str(z_binary)))
        z_binary = str(z_binary).zfill(len(str(expected_result_binary)))
        
        [char if char == z_binary[i] else 'X' for i, char in enumerate(expected_result_binary)]
        
        # self.print_all_wires()
        self.result2 = z_decimal
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


# simple part 2
    today.set_lines(simple=True) 
    today.part2()
    print(f'Part 2 <SIMPLE> result is: {today.result2}')

# =============================================================================
# # hard part 2
#     today.set_lines(simple=False)
#     today.part2()
#     print(f'Part 2 <HARD> result is: {today.result2}')
#     today.stop()
#     today.print_final()
# =============================================================================