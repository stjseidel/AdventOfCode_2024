#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 06:32:12 2023

@author: stjse
"""

from aoc_class import AOC
from timeit import default_timer as timer
import numpy as np
    
class Today(AOC):
        
    def parse_lines(self, file_path=''):
        self.lines = [line.replace('#', '1').replace('.', '0') for line in self.lines]
        self.num_lists = [[int(char) for char in line] for line in self.lines]
    
        blocks = [self.num_lists[i:i+7] for i in range(0, len(self.num_lists), 8)]
        self.locks = []
        self.keys = []
        for block in blocks:
            matrix = np.array(block)
            if block[0][0] == 1:  # is_lock
                self.locks.append(matrix)
            else:
                self.keys.append(matrix)
        return self.lines
    
    def part1(self):
        _ = self.parse_lines()
        matching = 0
        for key in self.keys:
            for lock in self.locks:
                if np.max(key + lock) == 1.:
                    matching += 1                    
                
        self.result1 = matching
        self.time1 = timer()
        return self.result1
                
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
    today = Today(day='25', simple=True)
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