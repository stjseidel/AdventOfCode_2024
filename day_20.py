#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 06:32:12 2023

@author: stjse
"""

from aoc_class import AOC
from timeit import default_timer as timer
from mazes import MazeSolver
from collections import defaultdict
import numpy as np
import sys
print(sys.getrecursionlimit())
sys.setrecursionlimit(20000)
class Today(AOC):
    maze_solver = MazeSolver()
        
    def parse_lines(self, file_path=''):
        lines = self.lines
                
        self.steps = [(row, col) for row, line in enumerate(self.lines) for col, char in enumerate(line) if char in ['.', 'E', 'S']]
        self.walls = [(row, col) for row, line in enumerate(self.lines) for col, char in enumerate(line) if char == '#']
        self.origin = [(row, col) for row, line in enumerate(self.lines) for col, char in enumerate(line) if char == 'S'][0]
        self.target = [(row, col) for row, line in enumerate(self.lines) for col, char in enumerate(line) if char == 'E'][0]
        self.wall_neighbors = {(row, col):
                               {(r, c) for (r,c) in [(row+1, col), (row, col+1), (row-1, col), (row, col-1)]} & set(self.steps)
                                     for (row, col) in self.walls}
                    
        # self.Matrix = {(row, col):set([(row+1, col), (row, col+1), (row-1, col), (row, col-1)]) & set(self.steps) for (row, col) in self.steps}
        self.Neighbors = {(row, col):set([(r, c) for (r,c) in [(row+1, col), (row, col+1), (row-1, col), (row, col-1)] if self.lines[r][c] in ['.', 'E', 'S']]) for (row, col) in self.steps}
        self.paths = []
        self.result_explore = 0
        self.grid_make_lines_copy()

        return lines
    
    def part1(self):
        lines = self.parse_lines()
        self.graph = self.maze_solver.plot_graph(lines=self.lines)
        costs, self.paths = self.maze_solver.dijkstra_with_directions_penalty_all_paths(graph=self.graph, start=self.origin, end=self.target, direction=None)
        self.path = self.paths[0]
        self._get_distance_to_target()
        cutoff = 1 if self.simple else 100
        self.result1 = self.get_cheats(radius=2, cutoff=cutoff)
        
        self.time1 = timer()
        return self.result1
                
    def part2(self):
        lines = self.parse_lines()
        self.graph = self.maze_solver.plot_graph(lines=self.lines)
        costs, self.paths = self.maze_solver.dijkstra_with_directions_penalty_all_paths(graph=self.graph, start=self.origin, end=self.target, direction=None)
        self.path = self.paths[0]
        self._get_distance_to_target()
        cutoff = 50 if self.simple else 100
        self.result2 = self.get_cheats(radius=20, cutoff=cutoff)
        self.time2 = timer()
        return self.result2
    
    def _get_distance_to_target(self):
        self.distances = {}
        self._get_neighbor_distance(this=self.target, distance=0)
        
    def get_cheats(self, radius=20, cutoff=100):
        cheats = 0
        self.cheat_results = defaultdict(int)
        for pos in self.path:
            remaining_time = self.distances[pos]
            circle_dict = self._get_circle_around_pos(pos, radius=radius)
            for cheat_end, cheat_duration in circle_dict.items():
                savings = remaining_time - self.distances[cheat_end] - cheat_duration
                if savings >= cutoff:
                    cheats += 1
                    self.cheat_results[savings] += 1
                    
        return cheats
        
    def _get_neighbor_distance(self, this, distance=0):
        self.distances[this] = distance
        for neigh in self.Neighbors[this]:
            if neigh not in self.distances.keys():
                self._get_neighbor_distance(neigh, distance=distance+1)
            
    def _get_circle_around_pos(self, pos, radius=20):    
        circle = list(set([(row, col) for row in range(pos[0]-radius, pos[0]+radius+1) for col in range(pos[1]-radius, pos[1]+radius+1) if (abs(row-pos[0]) + abs(col-pos[1])) <= radius]) & set(self.steps))
        
        circle_dict = {(row, col):(abs(row-pos[0]) + abs(col-pos[1])) for (row, col) in circle}
        return circle_dict
    
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
