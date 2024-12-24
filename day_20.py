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
        # self.valid_cheats = [wall for wall, neighbors in self.wall_neighbors.items() if len(neighbors) >= 2]
        self.valid_cheats = []  # valid are only walls with at least 3 neighboring steps, or 2 neighboring steps that are on opposite sides of the wall
        for wall, neighbors in self.wall_neighbors.items():
            neighbors = list(neighbors)
            if len(neighbors) > 3:
                self.valid_cheats.append(wall)
            elif len(neighbors) == 2:
                one, two = neighbors[0], neighbors[1]
                if (abs(one[0]-two[0]) == 2) or abs(one[1]-two[1]) == 2:
                    self.valid_cheats.append(wall)
                    
        # self.Matrix = {(row, col):set([(row+1, col), (row, col+1), (row-1, col), (row, col-1)]) & set(self.steps) for (row, col) in self.steps}
        self.Neighbors = {(row, col):set([(r, c) for (r,c) in [(row+1, col), (row, col+1), (row-1, col), (row, col-1)] if self.lines[r][c] in ['.', 'E', 'S']]) for (row, col) in self.steps}
        self.paths = []
        self.result_explore = 0
        self.grid_make_lines_copy()

        # lines = [[int(lin) for lin in line.split(' ') if set(lin) != set('') ] for line in lines]
        return lines
    
    def part1(self):
        lines = self.parse_lines()
        graph = self.maze_solver.plot_graph(lines=self.grid)
        original_time = self.maze_solver.dijkstra_with_directions_penalty(graph=graph, start=self.origin, end=self.target)
        self.cheat_results = defaultdict(int)
        print('original time: ', original_time)
        counting = 0
        for i, cheat in enumerate(self.valid_cheats):
            self.grid[cheat[0]][cheat[1]] = '.'
            self.maze_solver.plot_graph(lines=self.grid)
            
            graph = self.maze_solver.plot_graph(lines=self.grid)
            this_time = self.maze_solver.dijkstra_with_directions_penalty(graph=graph, start=self.origin, end=self.target)
            saved = original_time - this_time
            # self.cheat_results[cheat] = saved
            self.cheat_results[saved] += 1
            self.grid[cheat[0]][cheat[1]] = '#'
            if saved >= 100:
                counting += 1
            print(f'[{i} / {len(self.valid_cheats)}: {i/len(self.valid_cheats)*100:.2f}%]{cheat}, saved: {saved}. >= 100: {counting}')
        
        self.result1 = sum([cheats for time, cheats in self.cheat_results.items() if time >= 100])
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