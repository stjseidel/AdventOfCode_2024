#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 06:32:12 2023

@author: stjse
"""

from aoc_class import AOC
from timeit import default_timer as timer
from math import prod

import cv2
import numpy as np

class LineMovement:
    all_instances = []
    quadrant_dict = {}
    def __init__(self, start_pos, speed, grid_size, time=0):
        self.start_pos = start_pos
        self.speed = speed
        self.grid_size = grid_size
        self.time = time
        self.set_position_at_time(time=time)
        
        
        LineMovement.all_instances.append(self)
        
    def set_position_at_time(self, time=None):
        self.time = time or self.time
        if self.time is None:
            self.time = 0
        self.current_position = [((self.start_pos[i] + self.speed[i] * self.time)) % self.grid_size[i] for i in range(2)]
        self.quad = self.get_quadrant_position(time=self.time)
        # print(self.current_position, self)
        
    def get_quadrant_position(self, time=None):
        if time is not None:
            if time != self.time:
                self.time = time
                self.set_position_at_time(time=self.time)
        if self.grid_size not in LineMovement.quadrant_dict.keys():
            LineMovement.get_grid_quadrants(self.grid_size)
        
        return next((key for key, quad_set in LineMovement.quadrant_dict[self.grid_size].items() if tuple(self.current_position) in quad_set), None)
    
    @classmethod
    def get_all_instances(cls):
        return cls.all_instances
    
    @classmethod
    def get_grid_quadrants(cls, grid_size):
        x, y = grid_size
        x1, x2 = [0, x//2], [x//2+1, x]
        y1, y2 = [0, y//2], [y//2+1, y]
        three = set([(x,y) for x in range(*x2) for y in range(*y1)])
        two = set([(x,y) for x in range(*x1) for y in range(*y1)])
        one = set([(x,y) for x in range(*x1) for y in range(*y2)])
        four = set([(x,y) for x in range(*x2) for y in range(*y2)])
        cls.quadrant_dict[grid_size] = {1:one, 2:two, 3:three, 4:four}
    
    @classmethod
    def get_all_quadrant_positions(cls, time=None):
        cls.Quadrant_list = [pos.get_quadrant_position(time=time) for pos in cls.all_instances]
        for obj in cls.all_instances:
            obj.set_position_at_time(time=time)
        cls.Quadrant_counts_dict = {quad:cls.Quadrant_list.count(quad) for quad in set(cls.Quadrant_list) if quad is not None}
        cls.Quadrant_product = prod(cls.Quadrant_counts_dict.values())
        # # print(f'positions per quadrant: {cls.Quadrant_counts_dict}')
        return cls.Quadrant_product 
    
    def __repr__(self):
        return f'Q{self.quad}: LineMovement(start_pos={self.start_pos}, speed={self.speed}, grid_size={self.grid_size}, time={self.time})'
    
class Today(AOC):
    def parse_lines(self, file_path=''):
        LineMovement.all_instances = []
        lines = self.lines
        if self.simple:
            self.grid_size = (7, 11)
        else:
            self.grid_size = (103, 101)
        
        _ = [LineMovement(*self.extract_tuples(line), grid_size=self.grid_size, time=0) for line in self.lines]            
        return lines
    
    def extract_tuples(self, line):
        _, pos, _, speed = line.replace('=', ' ').split()
        pos, speed = [tuple(map(int, values.split(','))) for values in [pos, speed]]
        pos = tuple([pos[1], pos[0]])
        speed = tuple([speed[1], speed[0]])
        return pos, speed
    
    def part1(self):
        _ = self.parse_lines()
        self.print_quadrants()
        # self.print_result_grid()
        LineMovement.get_all_quadrant_positions(time=100)
            
        # self.print_result_grid()
        self.result1 = LineMovement.Quadrant_product
        # breakpoint()
        # self.get_quad_positions
        self.time1 = timer()
        return self.result1
                
    def print_result_grid(self):
        self.grid_make_empty_x_y(self.grid_size[0]-1, self.grid_size[1]-1)
        for obj in LineMovement.all_instances:
            pos = obj.current_position
            present = self.grid[pos[0]][pos[1]]
            if present == '.':
                term = '1'
            else:
                term = str(int(present) + 1)
            self.grid_enter_result(this_list=[pos], term=term)
        # clear the middle rows
        self.grid_enter_result(this_list=[(i, self.grid_size[1]//2) for i in range(self.grid_size[0])], term=' ')
        self.grid_enter_result(this_list=[(self.grid_size[0]//2, i) for i in range(self.grid_size[1])], term=' ')
        self.print_grid()
    
    def part2(self):
        _ = self.parse_lines()
        self.print_quadrants()
        self.minima = 0
        # self.print_result_grid()
        
        # self.print_result_grid()
        self.result2 = self.solve_for_christmas_trees()
        # breakpoint()
        # self.get_quad_positions
        
        self.time2 = timer()
        return self.result2
    
    def solve_for_christmas_trees(self):  
        for time in range(10000):
            _ = [obj.set_position_at_time(time=time) for obj in LineMovement.all_instances]
            positions = [obj.current_position for obj in LineMovement.all_instances]
            if len(set([tuple(pos) for pos in positions])) == len(LineMovement.all_instances):
                result = time
                grid = np.zeros(tuple(self.grid_size))        
                for pos in positions:
                    grid[pos[0], pos[1]] = 255
                cv2.imwrite(f"d14_images/day14_ChristmasTree_{time}.png", grid)
                return result
                    
            
        
        
        
        
    def print_final(self):
        print(f'Part 1 result is: {self.result1}. (time: {round(self.time1 - self.beginning_of_time, 2)})')
        print(f'Part 2 result is: {self.result2} (time: {round(self.time2 - self.time1, 2)})')
        
    def print_quadrants(self):
        quads_dict = LineMovement.quadrant_dict
        quads = quads_dict[self.grid_size]
        self.grid_make_empty_x_y(self.grid_size[0]-1, self.grid_size[1]-1)
        for key, this_list in quads.items():
            self.grid_enter_result(this_list=list(this_list), term=str(key))
        # self.print_grid()

# =============================================================================
#     def get_quad_positions(self):
#         quad_dict = LineMovement.quadrant_dict[today.grid_size]
#         one = quad_dict[1]
#         two = quad_dict[2]
#         three = quad_dict[3]
#         four = quad_dict[4]
#         
#         all_positions = [tuple(obj.current_position) for obj in  LineMovement.all_instances]
#         
#         quarters = [sum([pos in quarter for pos in all_positions]) for quarter in [one, two, three, four]]
# =============================================================================
        
        
if __name__ == '__main__':
# prep
    today = Today(day='', simple=True)
    today.create_txt_files()

# simple part 1
    today.set_lines(simple=True)
    today.part1()
    print(f'Part 1 <SIMPLE> result is: {today.result1}')
    
# # # hard part 1
    today.set_lines(simple=False)
    today.part1()
    print(f'Part 1 <HARD> result is: {today.result1}')
    today.stop()
    
# simple part 2
    # today.set_lines(simple=True) 
    # today.part2()
    # print(f'Part 2 <SIMPLE> result is: {today.result2}')

# hard part 2
    today.set_lines(simple=False)
    today.part2()
    print(f'Part 2 <HARD> result is: {today.result2}')
    today.stop()
    today.print_final()
