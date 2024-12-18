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
        self.path_results = {}
        self.final_results = {}
        
        self.steps = [(row, col) for row, line in enumerate(self.lines) for col, char in enumerate(line)   if char in ['.', 'E', 'S']]
        self.walls = [(row, col) for row, line in enumerate(self.lines) for col, char in enumerate(line)   if char == '#']
        self.start = [(row, col) for row, line in enumerate(self.lines) for col, char in enumerate(line)   if char == 'S'][0]
        self.target = [(row, col) for row, line in enumerate(self.lines) for col, char in enumerate(line)   if char == 'E'][0]
        # breakpoint()
        # self.neighbors = {(row, col):set([(row+1, col), (row, col+1), (row-1, col), (row, col-1)]) & set(self.steps) for (row, col) in self.steps}
        self.neighbors = {(row, col):set([(r, c) for (r,c) in [(row+1, col), (row, col+1), (row-1, col), (row, col-1)] if self.lines[r][c] in ['.', 'E', 'S']]) for (row, col) in self.steps}
        self.paths = []
        self.result_explore = 0
        # self.grid_make_empty()
        # self.grid_enter_result(this_list=self.walls, term='#')
        # self.grid_enter_result(this_list=[self.start], term='S')
        # self.grid_enter_result(this_list=[self.target], term='E')
        # self.print_grid()
        self.traced = {}
        self.max_steps = 82465
        return lines
    
    def part1(self):
        lines = self.parse_lines()
        print('setup done')
        # self.stop()
        self.explore(current=self.start)
        self.result1 = self.result_explore
        self.path_results[self.simple] = self.paths.copy()
        self.final_results[self.simple] = self.result1
        self.time1 = timer()
        return self.result1
    
    def explore(self, current, history=[], turns=1, last_direction=(0,0)):
        # self.grid_enter_result(this_list=[current], term='O', print_grid=True)
        # print("~"*30)
        current_points = len(history)+turns*1000
        if current == self.target:
            self.paths.append([history, turns, current_points])
            if self.max_steps == 0:
                self.max_steps = current_points
            else:
                self.max_steps = min(current_points, self.max_steps) 
            print(f'{len(self.paths)}th result: {turns} turns, points: {current_points }')
            if self.result_explore == 0:
                self.result_explore = current_points 
            else:
                self.result_explore = min(self.result_explore, current_points)
            return None
        elif current in self.walls:
            return None
        if self.max_steps > 0 and current_points > self.max_steps:
            return None
        # if current in self.traced:
        #     if current_points > self.traced[current]:
        #         return None
        #     elif current_points < self.traced[current]:
        #         self.traced[current] = current_points
        #         # print(f'OVERWRITING {len(self.traced)} plots entered. This position: {current} This history has {len(history)} steps. points: {current_points}')
        # else:
        self.traced[current] = current_points
        print(f'{len(self.traced)} plots entered. This position: {current} This history has {len(history)} steps. points: {current_points}')
        # self.traced[current] = current_points
        # else:
        next_positions = self.neighbors[current] - set(history)
        for next_pos in next_positions:
            this_history = history.copy()
            this_history.append(next_pos)
            this_dir = self.get_direction(next_pos, current)
            this_turns = turns
            if not last_direction == (0,0):
                if this_dir != last_direction:
                    this_turns += 1
            self.explore(current=next_pos, history=this_history, turns=this_turns, last_direction=this_dir)
                
            
    def get_direction(self, current, prior):
        return (current[0] - prior[0], current[1] - prior[1])
    
    def print_paths(self):
        for items in self.paths:
            path, turns, points = items[0], items[1], items[2]
            self.grid_make_empty()
            self.grid_enter_result(this_list=self.walls, term='o')
            self.grid_enter_result(this_list=[self.start], term='S')
            self.grid_enter_result(this_list=[self.target], term='E')
            self.grid_enter_result(this_list=path, term='X')
            self.print_grid()
            print(turns, points)
                
    def part2(self):
        # lines = self.parse_lines()
        histories = [path[0] for path in self.path_results[self.simple] if path[-1] == self.final_results[self.simple]]
        print(len(histories), 'valid results')
        valid = []
        for path in histories:
            valid.extend(path)
        
            
        self.result2 = len(set(valid))
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
    # today.stop()
# hard part 1
    today.set_lines(simple=False)
    today.part1()
    print(f'Part 1 <HARD> result is: {today.result1}')
    # today.stop()
    # 614932 too high
    # 610928 too high
    # 149664 too high
    # 93484  high
    # 82460


# simple part 2
    today.set_lines(simple=True) 
    today.part2()
    print(f'Part 2 <SIMPLE> result is: {today.result2}')

# # hard part 2
#     today.set_lines(simple=False)
#     today.part2()
#     print(f'Part 2 <HARD> result is: {today.result2}')
#     today.stop()
#     today.print_final()