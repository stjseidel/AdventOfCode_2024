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
        lines = self.lines
        self.path_results = {}
        self.final_results = {}
        
        self.steps = [(row, col) for row, line in enumerate(self.lines) for col, char in enumerate(line) if char in ['.', 'E', 'S']]
        self.walls = [(row, col) for row, line in enumerate(self.lines) for col, char in enumerate(line) if char == '#']
        self.origin = [(row, col) for row, line in enumerate(self.lines) for col, char in enumerate(line) if char == 'S'][0]
        self.target = [(row, col) for row, line in enumerate(self.lines) for col, char in enumerate(line) if char == 'E'][0]
        # self.Matrix = {(row, col):set([(row+1, col), (row, col+1), (row-1, col), (row, col-1)]) & set(self.steps) for (row, col) in self.steps}
        self.Neighbors = {(row, col):set([(r, c) for (r,c) in [(row+1, col), (row, col+1), (row-1, col), (row, col-1)] if self.lines[r][c] in ['.', 'E', 'S']]) for (row, col) in self.steps}
        self.paths = []
        self.result_explore = 0
        # self.grid_make_empty()
        # self.grid_enter_result(this_list=self.walls, term='#')
        # self.grid_enter_result(this_list=[self.origin], term='S')
        # self.grid_enter_result(this_list=[self.target], term='E')
        # self.print_grid()
        self.traced = {}
        self.max_steps = None
        return lines
    
    def part1(self):
        lines = self.parse_lines()
        self.graph = self.maze_solver.plot_graph(lines=self.lines)
        shortest_path_cost  = self.maze_solver.dijkstra_with_directions_penalty(graph=self.graph, start=self.origin, end=self.target, direction=(0, 1))
        
        self.result1 = shortest_path_cost
        self.time1 = timer()
        return self.result1
    
    def get_direction(self, current, prior):
        return (current[0] - prior[0], current[1] - prior[1])
    
# =============================================================================
#     def print_paths(self):
#         for items in self.paths:
#             path, turns, points = items[0], items[1], items[2]
#             self.grid_make_empty()
#             self.grid_enter_result(this_list=self.walls, term='o')
#             self.grid_enter_result(this_list=[self.origin], term='S')
#             self.grid_enter_result(this_list=[self.target], term='E')
#             self.grid_enter_result(this_list=path, term='X')
#             self.print_grid()
#             # print(turns, points)
# =============================================================================
                
    def part2(self):
        lines = self.parse_lines()
# =============================================================================
#         histories = [path[0] for path in self.path_results[self.simple] if path[-1] == self.final_results[self.simple]]
#         # print(len(histories), 'valid results')
#         valid = []
#         for path in histories:
#             valid.extend(path)
#         
#         self.Matrix = {(row, col): int(char) for row, line in enumerate(self.lines) for col, char in enumerate(line)}
#         self.Neighbors = {(row, col):{(row+1, col),(row, col+1),(row-1, col),(row, col-1)} & self.Matrix.keys() for (row, col) in self.Matrix}
#         
#         traverse = lambda coord: [coord] if self.Matrix[coord] == 9 else sum([traverse(neighbor) for neighbor in self.Neighbors[coord] if self.Matrix[neighbor] == self.Matrix[coord] + 1], [])
#         
#         result = sum(len(traverse(start)) for start in self.Matrix.keys() if self.Matrix[start] == 0)
# =============================================================================
        self.graph = self.maze_solver.plot_graph(lines=self.lines)
        self.paths = self.maze_solver.dijkstra_with_directions_penalty_all_paths(graph=self.graph, start=self.origin, end=self.target, direction=(0, 1))
        self.best_spots = set([spot for path in self.paths[-1] for spot in path])
            
        self.result2 = len(self.best_spots)
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
    today.stop()
# hard part 1
    today.set_lines(simple=False)
    today.part1()
    print(f'Part 1 <HARD> result is: {today.result1}')
    today.stop()

# simple part 2
    today.set_lines(simple=True) 
    today.part2()
    print(f'Part 2 <SIMPLE> result is: {today.result2}')

# # hard part 2
    today.set_lines(simple=False)
    today.part2()
    print(f'Part 2 <HARD> result is: {today.result2}')
    today.stop()
    today.print_final()