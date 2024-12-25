#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 06:32:12 2023

@author: stjse
"""

from aoc_class import AOC
from timeit import default_timer as timer
from mazes import MazeSolver
    
class Today(AOC):
    maze_solver = MazeSolver()
    def parse_lines(self, file_path=''):
        
        if self.simple:
            grid = (6, 6)
        else:
            grid = (70, 70)
        lines = self.lines
        self.byte_list = [(int(line.split(',')[1]), int(line.split(',')[0])) for line in self.lines]
        self.steps = self.grid_get_position_tuple_list_x_y(*grid)
        self.origin = (0, 0)
        self.target = grid
        self.init_grid()
        
        self.walls = []
        self.max_steps = 299
        return lines

    def init_grid(self):
        if self.simple:
            grid = (6, 6)
        else:
            grid = (70, 70)
        self.grid_make_empty_x_y(*grid)
        self.grid_enter_result(this_list=[self.origin], term='S')
        self.grid_enter_result(this_list=[self.target], term='E', print_grid=False)
        self.drop_count = 0
        
    def part1(self):
        self.part = 1
        _ = self.parse_lines()
        self.init_grid()
        self.drop_bytes(number=12 if self.simple else 1024)
        graph = self.maze_solver.plot_graph(lines=self.grid)
        cost = self.maze_solver.dijkstra_with_directions_penalty(graph=graph, start=self.origin, end=self.target, direction=None, direction_penalty=0)
        
        self.result1 = cost
        self.time1 = timer()
        return self.result1
        
    def drop_bytes(self, number):
        to_drop = self.byte_list[self.drop_count:self.drop_count+number]
        self.drop_count += number
        self.walls.extend(to_drop)
        self.steps = list(set(self.steps) - set(self.walls))
        self.grid_enter_result(this_list=to_drop, term='#')
        return to_drop
            
    def part2(self):
        _ = self.parse_lines()
        initial_drop = 12 if self.simple else 1024
        
        step_sizes = [size for size in [2**i for i in range(10, 0, -1)] if size < len(self.byte_list) - initial_drop]
        for step_size in step_sizes:
            print(f'running step_size: {step_size}')
            drop_count, to_drop = self.drop_until_blocked(step_size=step_size, number=max(self.drop_count, initial_drop))
            drop_count -= step_size
            self.drop_count = drop_count
            
        self.result2 = f'{to_drop[0][1]},{to_drop[0][0]}'
        self.time2 = timer()
        return self.result2
        
    def drop_until_blocked(self, step_size=1, number=0):
        self.init_grid()
        self.drop_bytes(number)
        free = True
        
        while free and self.drop_count < len(self.byte_list):
            to_drop = self.drop_bytes(step_size)
            print(f'[{self.drop_count} / {len(self.byte_list)}: {(self.drop_count / len(self.byte_list) * 100):.2F}%] {self.drop_count}')
            graph = self.maze_solver.plot_graph(lines=self.grid)
            free = self.maze_solver.dijkstra_with_directions_penalty(graph=graph, start=self.origin, end=self.target, direction=None, direction_penalty=0)
        if step_size == 1:
            pass
        return [self.drop_count, to_drop]
        
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
