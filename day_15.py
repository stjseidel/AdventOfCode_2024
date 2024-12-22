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
        command_lines = self.lines[split+1:]
        self.walls = {(r, c) for r, rows in enumerate(grid_lines) for c, char in enumerate(rows) if char == '#'}
        self.floor = {(r, c) for r, rows in enumerate(grid_lines) for c, char in enumerate(rows) if char != '#'}
        self.boxes = {(r, c) for r, rows in enumerate(grid_lines) for c, char in enumerate(rows) if char == 'O'}
        self.robot = [(r, c) for r, rows in enumerate(grid_lines) for c, char in enumerate(rows) if char == '@'][0]
       
        self.commands = [char for char in ''.join(command_lines) if char in '<^>v']
        self.lines = grid_lines
        self.directions = {'<':(0, -1), '^':(-1, 0), '>':(0, 1), 'v':(1, 0)}
        self.storage = grid_lines.copy()
        self.grid_make_empty()
        # self.print_grid()
        self.grid_enter_result(this_list=list(self.walls), term='#')
        # self.print_grid()
        self.grid_enter_result(this_list=list(self.boxes), term='O')
        # self.print_grid()
        self.grid_enter_result(this_list=[self.robot], term='@')
        # lines = [[int(lin) for lin in line.split(' ') if set(lin) != set('') ] for line in lines]
        # self.print_grid()
        return lines
    
    def parse_lines_2(self, file_path=''):
        lines = self.lines
        split = self.lines.index('')
        grid_lines_single = self.lines[:split]
        grid_lines = []
        for grid_line in grid_lines_single:
            line = ''
            for char in grid_line:
                if char == 'O':
                    line += '[]'
                elif char == '@':
                    line += '@.'
                else:
                    line+= char*2
            grid_lines.append(line)
        command_lines = self.lines[split+1:]
        self.walls = {(r, c) for r, rows in enumerate(grid_lines) for c, char in enumerate(rows) if char == '#'}
        self.floor = {(r, c) for r, rows in enumerate(grid_lines) for c, char in enumerate(rows) if char != '#'}
        self.boxes_left = {(r, c) for r, rows in enumerate(grid_lines) for c, char in enumerate(rows) if char == '['}
        self.boxes_right = {(r, c) for r, rows in enumerate(grid_lines) for c, char in enumerate(rows) if char == ']'}
        self.robot = [(r, c) for r, rows in enumerate(grid_lines) for c, char in enumerate(rows) if char == '@'][0]
       
        self.commands = [char for char in ''.join(command_lines) if char in '<^>v']
        self.lines = grid_lines
        self.directions = {'<':(0, -1), '^':(-1, 0), '>':(0, 1), 'v':(1, 0)}
        self.storage = grid_lines.copy()
        self.grid_make_empty()
        # self.print_grid()
        self.grid_enter_result(this_list=list(self.walls), term='#')
        # self.print_grid()
        self.grid_enter_result(this_list=list(self.boxes_left), term='[')
        self.grid_enter_result(this_list=list(self.boxes_right), term=']')
        # self.print_grid()
        self.grid_enter_result(this_list=[self.robot], term='@')
        # lines = [[int(lin) for lin in line.split(' ') if set(lin) != set('') ] for line in lines]
        self.print_grid()
        return lines
    
    def part1(self):
        lines = self.parse_lines_2()
        self.print_grid()
        result = sum([self.try_to_move(from_pos=self.robot, offset=self.directions[com], com=com) for com in self.commands])
        self.result_boxes = {(r, c) for r, rows in enumerate(self.grid) for c, char in enumerate(rows) if char == 'O'}
        
        self.result1 = sum([pos[0]*100+pos[1] for pos in self.result_boxes])
        self.time1 = timer()
        return self.result1
                
    def try_to_move(self, from_pos, offset, com=None):
        # if com is not None:
            # print(com)
        next_pos = self.add_tuple(from_pos, offset)
        next_char = self.grid[next_pos[0]][next_pos[1]]
        if next_char == '.':
            if next_pos != self.robot:  # only overwrite if we moved
                self.grid[next_pos[0]][next_pos[1]] = 'O'
            self.move_robot(offset)
            return True
        elif next_char == '#':
            return False
        else:
            self.try_to_move(next_pos, offset, com=None)   
            return False
    
    @staticmethod
    def add_tuple(one, two, steps=1):
        return tuple([one[i]+two[i]*steps for i in range(len(one))])
    
    def move_robot(self, offset):
        self.grid[self.robot[0]][self.robot[1]] = '.'
        self.robot = self.add_tuple(self.robot, offset)
        self.grid_enter_result(this_list=[self.robot], term='.')
        self.grid[self.robot[0]][self.robot[1]] = '@'
        self.grid_enter_result(this_list=[self.robot], term='@', print_grid=False)
    
    def part2(self):
        lines = self.parse_lines_2()
        self.print_grid()
        result = sum([self.try_to_move_2(from_pos=self.robot, offset=self.directions[com], com=com) for com in self.commands])
        self.result_boxes = {(r, c) for r, rows in enumerate(self.grid) for c, char in enumerate(rows) if char == 'O'}
        
        self.result2 = sum([pos[0]*100+pos[1] for pos in self.result_boxes])
        self.time2 = timer()
        return self.result2
    
            
    def try_to_move_2(self, from_pos, offset, com=None):
        # if com is not None:
            # print(com)
        next_pos = self.add_tuple(from_pos, offset)
        next_char = self.grid[next_pos[0]][next_pos[1]]
        # cases where we simply move the robot
        if self.robot == from_pos:
            self.moving = {}
            if next_char == '#':
                return None
            elif next_char == '.':
                self.move_robot(offset)
                return True
        # moving boxes east or west
                    
        if next_char == '.':
            if next_pos != self.robot:  # only overwrite if we moved
                self.grid[next_pos[0]][next_pos[1]] = 'O'
            self.move_robot(offset)
            return True
        elif next_char == '#':
            return False
        else:
            self.try_to_move(next_pos, offset, com=None)   
            return False
    
    def set_new_box_positions(self, moving, offset):
        for pos in moving.keys():
            self.grid[pos] = '.'
        for pos, char in moving.items():
            self.grid[self.add_tuple(pos, offset)] = char
        
            
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
    # 1528704 too high

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