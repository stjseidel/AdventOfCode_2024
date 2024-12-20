#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 06:32:12 2023

@author: stjse
"""

from aoc_class import AOC
from timeit import default_timer as timer

class Box:
    all_instances = []
    directions = {'<':(0, -1), '^':(1, 0), '>':(0, 1), 'v':(-1, 0)}
    robot = None
    
    @classmethod
    def get_all_instances(cls):
        return cls.all_instances
    
    def __init__(self, x, y, is_robot=False):
        self.position = (x, y)
        Box.all_instances.append(self)
        self.is_robot = is_robot
        Box.robot = self
        
        
    @classmethod
    def get_positions_dict(cls):
        cls.positions_dict = {obj.position for obj in cls.all_instances} 
    
        
    
    
    
class Today(AOC):
        
    def parse_lines(self, file_path=''):
        lines = self.lines
        split = self.lines.index('')
        grid_lines = self.lines[:split]
        self.walls = {(r, c) for r, rows in enumerate(grid_lines) for c, char in enumerate(rows) if char == '#'}
        self.floor = {(r, c) for r, rows in enumerate(grid_lines) for c, char in enumerate(rows) if char != '#'}
        self.commands = [char for char in ''.join(self.lines[split:])]
        # lines = [[int(lin) for lin in line.split(' ') if set(lin) != set('') ] for line in lines]
        return lines
    
    def part1(self):
        lines = self.parse_lines()
        self.result1 = 'TODO'
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