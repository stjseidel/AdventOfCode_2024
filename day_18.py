#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 06:32:12 2023

@author: stjse
"""

from aoc_class import AOC
from timeit import default_timer as timer
from day_16 import Today as day16
    
class Today(AOC):
    day16 = day16()    
    def parse_lines(self, file_path=''):
        
        if self.simple:
            grid = (6, 6)
        else:
            grid = (70, 70)
        lines = self.lines
        # self.steps = [tuple([int(c) for c in line.split(',')]) for line in self.lines]
        self.byte_list = [(int(line.split(',')[1]), int(line.split(',')[0])) for line in self.lines]
        self.steps = self.grid_get_position_tuple_list_x_y(*grid)
        # self.steps = [(int(line.split(',')[0]), grid[1]-int(line.split(',')[1])) for line in self.lines]
        # lines = [[int(lin) for lin in line.split(' ') if set(lin) != set('') ] for line in lines]
        self.grid_make_empty_x_y(*grid)
        self.day16.grid = self.grid
        self.start = (0, 0)
        self.target = grid
        self.grid_enter_result(this_list=[self.start], term='S')
        self.grid_enter_result(this_list=[self.target], term='E', print_grid=True)
        self.drop_count = 0
        
        number = 12 if self.simple else 1024
        self.day16.walls = []
        self.day16.steps = []
        self.drop_bytes(number=number)
        self.day16.steps = [(row, col) for row, line in enumerate(self.grid) for col, char in enumerate(line)   if char in ['.', 'E', 'S']]
        self.day16.walls = [(row, col) for row, line in enumerate(self.grid) for col, char in enumerate(line)   if char == '#']
        self.day16.start = [(row, col) for row, line in enumerate(self.grid) for col, char in enumerate(line)   if char == 'S'][0]
        self.day16.target = [(row, col) for row, line in enumerate(self.grid) for col, char in enumerate(line)   if char == 'E'][0]
        # self.day16.neighbors = {(row, col):set([(r, c) for (r,c) in list(set([(row+1, col), (row, col+1), (row-1, col), (row, col-1))] & set(self.steps)) if self.grid[r][c] in ['.', 'E', 'S']]) for (row, col) in self.steps}
        self.day16.neighbors = {
                (row, col): set(
                    [
                        (r, c)
                        for (r, c) in {(row + 1, col), (row, col + 1), (row - 1, col), (row, col - 1)}
                        if (r, c) in self.steps and self.grid[r][c] in ['.', 'E', 'S']
                    ]
                )
                for (row, col) in self.steps
            }
        self.day16.paths = []
        self.day16.result_explore = 0
        # self.grid_make_empty()
        # self.grid_enter_result(this_list=self.walls, term='#')
        # self.grid_enter_result(this_list=[self.start], term='S')
        # self.grid_enter_result(this_list=[self.target], term='E')
        # self.print_grid()
        self.day16.traced = {}
        self.day16.max_steps = 0
        return lines

    def part1(self):
        self.part = 1
        _ = self.parse_lines()
        self.day16.explore(current=self.start)
        self.day16.print_paths()
        results = [int(str(path[-1])[-3:]) for path in self.day16.paths]
        print(results)
        
        self.result1 = min(results)
        self.time1 = timer()
        return self.result1
    
    def drop_bytes(self, number):
        to_drop = self.byte_list[self.drop_count:self.drop_count+number+1]
        self.drop_count += number
        self.day16.walls.extend(to_drop)
        # self.day16.walls = self.walls
        self.day16.steps = list(set(self.day16.steps) - set(self.day16.walls))
        self.grid_enter_result(this_list=to_drop, term='#')
        self.print_grid()
    
            
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
    # self.day16.print_grid()
# hard part 1
    today.set_lines(simple=False)
    today.part1()
    print(f'Part 1 <HARD> result is: {today.result1}')
    # today.stop()


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