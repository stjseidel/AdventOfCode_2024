#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 06:32:12 2023

@author: stjse
"""

from aoc_class import AOC
from timeit import default_timer as timer

    
class Today(AOC):
        
    def parse_lines(self, file_path=''):
        lines = self.lines
        self.map_lines_maze()
        self.grid_make_empty()
        # lines = [[int(lin) for lin in line.split(' ') if set(lin) != set('') ] for line in lines]
        return lines
    
    def part1(self):
        lines = self.parse_lines()
        self.current_position = self.get_start_pos()
        self.mapped_positions = set()
        self.directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        self.direction = 0
        self.traversed = set([self.start_pos])
        self.set_direction_offset()
        self.out_of_map = False
        while not self.out_of_map:
            self.step()
        self.result1 = len(self.traversed)
        self.time1 = timer()
        return self.result1
                
    def get_start_pos(self):
        lines = self.lines
        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if char == '^':
                    # print(f'start_pos is {row}, {col}')
                    self.start_pos = (row, col)
                    return self.start_pos
                
    
    def set_direction_offset(self, direction=None):
        direction = direction or self.direction
        self.offset = self.directions[direction % 4]
        # print('new offset:', self.offset)
        return self.offset
    
    def turn_around(self):
        old_direction = self.direction
        self.direction = (old_direction + 1) % 4
        # print(old_direction, self.direction)
        self.offset = self.set_direction_offset()
        
    def map_lines_maze(self, lines=None, start_char='^', block_char='#'):
        lines = lines or self.lines
        start_char = start_char or '^'
        block_char = block_char or '#'
        free = set()
        blocked = set()
        start_pos = (0, 0)
        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if char == block_char:
                    blocked.add((row, col))
                elif char == start_char:
                    start_pos = (row, col)
                    free.add((row, col))
                else:
                    free.add((row, col))
        self.start_pos = start_pos
        self.free = free
        self.blocked = blocked
        
    def get_next_pos(self, this_pos=None, offset=None):
        this_pos = this_pos or self.current_position
        offset = offset or self.offset
        next_pos = tuple(a + b for a, b in zip(this_pos, offset))
        self.next_pos = next_pos
        return next_pos
    
    def step(self):
        this_pos = self.current_position
        next_pos = self.get_next_pos()
        # print(this_pos, next_pos, len(self.traversed))
        if next_pos in self.blocked:
            self.turn_around()
        elif next_pos in self.free:
            self.current_position = next_pos
            self.traversed.add(self.current_position)
        else:
            # print(len(self.traversed), ' positions traversed.')
            self.out_of_map = True
            return None
        self.grid_enter_result(this_list=[self.current_position], term=['X'])
        # self.print_grid()
        return True
            
        
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