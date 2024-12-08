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
        # lines = [[int(lin) for lin in line.split(' ') if set(lin) != set('') ] for line in lines]
        self.rows = len(lines)
        self.cols = len(lines[0])
        return lines
    
    def part1(self):
        self.term = 'XMAS'
        self.part = 1
        lines = self.parse_lines()
        self.found = 0
        self.lines = lines
        self.grid_make_empty()
        
        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if char == 'X':
                    self.check_from_row_col(row, col)
                    
                    
        self.result1 = self.found
        self.time1 = timer()
        return self.result1
    
    def check_from_row_col(self, row, col):
        lines = self.lines
        
        # check right
        self.check_slice(self.get_slice(self.make_list_of_coords(row, col, row_step=0, col_step=1)))  # right
        self.check_slice(self.get_slice(self.make_list_of_coords(row, col, row_step=0, col_step=-1)))  # left
        self.check_slice(self.get_slice(self.make_list_of_coords(row, col, row_step=-1, col_step=0)))  # up
        self.check_slice(self.get_slice(self.make_list_of_coords(row, col, row_step=1, col_step=0)))  # down
        self.check_slice(self.get_slice(self.make_list_of_coords(row, col, row_step=1, col_step=1)))  # down right
        self.check_slice(self.get_slice(self.make_list_of_coords(row, col, row_step=-1, col_step=1)))  # up right
        self.check_slice(self.get_slice(self.make_list_of_coords(row, col, row_step=1, col_step=-1)))  # down left
        self.check_slice(self.get_slice(self.make_list_of_coords(row, col, row_step=-1, col_step=-1)))  # up left
            
            
        
    def check_slice(self, this):
        if type(this) == list:
            this = ''.join(list)
        if this == self.term or this == self.term[::-1]:
            self.found += 1
            if self.part == 1:
                self.grid_enter_result(self.this_list)
    
    def get_slice(self, list_of_coords):
        try:
            string = ''
            for pair in list_of_coords:
                string += self.lines[pair[0]][pair[1]]
            return string
        except:
            return ''
        
    def make_list_of_coords(self, row, col, row_step, col_step):
        range_len = len(self.term)
        
        self.this_list = [[row+i*row_step, col+i*col_step] for i in range(range_len)]
        items = self.flatten_lists(self.this_list)
        if min(items) < 0:
            self.this_list = []
        return self.this_list
        
        
        
    def part2(self):
        self.term = 'MAS'
        self.part = 2
        lines = self.parse_lines()
        self.lines = lines
        self.grid_make_empty()
        xmasses = 0
        for row, line in enumerate(lines[1:-1], 1):
            for col, char in enumerate(line[1:-1], 1):
                # print(row, col, char)
                if char == 'A':
                    self.found = 0
                    list_down_right = self.make_list_of_coords(row-1, col-1, row_step=1, col_step=1)
                    list_up_right = self.make_list_of_coords(row+1, col-1, row_step=-1, col_step=1)
                    self.check_slice(self.get_slice(list_down_right))  # down right
                    self.check_slice(self.get_slice(list_up_right))  # up right
                    if self.found == 2:
                        xmasses += 1
                        # print(row, col, list_down_right, list_up_right)
                        self.grid_enter_result(list_down_right)
                        # self.grid_print()
                        self.grid_enter_result(list_up_right)
                        # self.grid_print()
        
                    
                    
        self.result2 = xmasses
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

# hard part 2
    today.set_lines(simple=False)
    today.part2()
    print(f'Part 2 <HARD> result is: {today.result2}')
    today.stop()
    today.print_final()