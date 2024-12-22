#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 06:32:12 2023

@author: stjse
"""

from aoc_class import AOC
from timeit import default_timer as timer
from math import prod

class LineMovement:
    all_instances = []
    quadrant_dict = {}
    def __init__(self, start_pos, speed, grid_size, time=0):
        self.start_pos = start_pos
        self.speed = speed
        self.grid_size = grid_size
        self.time = time
        self.current_position = self.set_position_at_time(time=time)
        
        
        LineMovement.all_instances.append(self)
        
    def set_position_at_time(self, time=None):
        self.time = time or self.time
        self.current_position = [((self.start_pos[i] + self.speed[i] * self.time)) % self.grid_size[i] for i in range(2)]
        self.quad = self.get_quadrant_position(time=self.time)
        print(self.current_position, self)
        
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
        print(*range(*x1))
        print(*range(*x2))
        print(*range(*y1))
        print(*range(*y2))
        one = set([(x,y) for x in range(*x2) for y in range(*y1)])
        two = set([(x,y) for x in range(*x1) for y in range(*y1)])
        three = set([(x,y) for x in range(*x1) for y in range(*y2)])
        four = set([(x,y) for x in range(*x2) for y in range(*y2)])
        cls.quadrant_dict[grid_size] = {1:one, 2:two, 3:three, 4:four}
    
    @classmethod
    def get_all_quadrant_positions(cls, time=None):
        cls.Quadrant_list = [pos.get_quadrant_position(time=time) for pos in cls.all_instances]
        cls.Quadrant_counts_dict = {quad:cls.Quadrant_list.count(quad) for quad in set(cls.Quadrant_list) if quad is not None}
        cls.Quadrant_product = prod(cls.Quadrant_counts_dict.values())
        print(f'positions per quadrant: {cls.Quadrant_counts_dict}')
        return cls.Quadrant_product 
    
    def __repr__(self):
        return f'Q{self.quad}: LineMovement(start_pos={self.start_pos}, speed={self.speed}, grid_size={self.grid_size}, time={self.time})'
    
class Today(AOC):
    def parse_lines(self, file_path=''):
        lines = self.lines
        if self.simple:
            self.grid_size = (11, 7)
        else:
            self.grid_size = (101, 103)
        
        objs = [LineMovement(*self.extract_tuples(line), grid_size=self.grid_size, time=0) for line in self.lines]            
        
        # lines = [[int(lin) for lin in line.split(' ') if set(lin) != set('') ] for line in lines]
        return lines
    
    def extract_tuples(self, line):
        _, pos, _, speed = line.replace('=', ' ').split()
        pos, speed = [tuple(map(int, values.split(','))) for values in [pos, speed]]
        return pos, speed
    
    def part1(self):
        lines = self.parse_lines()
        # for i in range(1, 6):
        #     print('~'*30)
        #     LineMovement.get_all_quadrant_positions(time=i)
        LineMovement.get_all_quadrant_positions(time=100)
            
            
        self.result1 = LineMovement.Quadrant_product
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
    
# # hard part 1
#     today.set_lines(simple=False)
#     today.part1()
#     print(f'Part 1 <HARD> result is: {today.result1}')
#     today.stop()
# 246824500 too high
# 235271232 too high
# 205650900 too low
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