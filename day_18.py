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
        
        if self.simple:
            grid = (6, 6)
        else:
            grid = (70, 70)
        lines = self.lines
        # self.steps = [tuple([int(c) for c in line.split(',')]) for line in self.lines]
        self.byte_list = [(int(line.split(',')[1]), int(line.split(',')[0])) for line in self.lines]
        self.steps = self.grid_get_position_tuple_list_x_y(*grid)
        # self.steps = [(int(line.split(',')[0]), grid[1]-int(line.split(',')[1])) for line in self.lines]
        # lines = [[int(lin) for lin in line.split(' ') if set(lin) != set('') ] for line in lines]
        self.grid_make_empty_x_y(*grid)
        self.grid = self.grid
        self.origin = (0, 0)
        self.target = grid
        self.grid_enter_result(this_list=[self.origin], term='S')
        self.grid_enter_result(this_list=[self.target], term='T', print_grid=True)
        self.drop_count = 0
        
        number = 12 if self.simple else 1024
        self.walls = []
        self.steps = []
        self.drop_bytes(number=number)
        self.steps = [(row, col) for row, line in enumerate(self.grid) for col, char in enumerate(line)   if char in ['.', 'S', 'T']]
        self.walls = [(row, col) for row, line in enumerate(self.grid) for col, char in enumerate(line)   if char == '#']
        self.origin = [(row, col) for row, line in enumerate(self.grid) for col, char in enumerate(line)   if char == 'S'][0]
        self.target = [(row, col) for row, line in enumerate(self.grid) for col, char in enumerate(line)   if char == 'T'][0]
        # self.neighbors = {(row, col):set([(r, c) for (r,c) in list(set([(row+1, col), (row, col+1), (row-1, col), (row, col-1))] & set(self.steps)) if self.grid[r][c] in ['.', 'E', 'S']]) for (row, col) in self.steps}
        self.neighbors = {
                (row, col): set(
                    [
                        (r, c)
                        for (r, c) in {(row + 1, col), (row, col + 1), (row - 1, col), (row, col - 1)}
                        if (r, c) in self.steps and self.grid[r][c] in ['.', 'E', 'S', 'T']
                    ]
                )
                for (row, col) in self.steps
            }
        self.paths = []
        self.result_explore = 0
        # self.grid_make_empty()
        # self.grid_enter_result(this_list=self.walls, term='#')
        # self.grid_enter_result(this_list=[self.origin], term='S')
        # self.grid_enter_result(this_list=[self.target], term='E')
        # self.print_grid()
        self.traced = {}
        self.max_steps = 299
        return lines

    def part1(self):
        self.part = 1
        _ = self.parse_lines()
        self.explore(current=self.origin, history=[], target=self.target)
        results = [len(path)-1 for path in self.paths]
        print(results)
        
        # Matrix = {(row, col): int(char) for row, line in enumerate(self.grid) for col, char in enumerate(line)}
        # Matrix = {coord: '.' for coord in self.steps}
        # Matrix[self.origin] = 'S'
        # Matrix[self.target] = 'T'
        # Neighbors = {(row, col):{(row+1, col),(row, col+1),(row-1, col),(row, col-1)} & Matrix.keys() for (row, col) in Matrix}
        
        # traverse = lambda coord: [coord] if Matrix[coord] == 'T' else sum([traverse(neighbor) for neighbor in Neighbors[coord] if Matrix[neighbor] in ['.', 'T']], [])
        
        # result = sum(len(traverse(origin)) for origin in Matrix.keys() if Matrix[origin] == 'S')
        
        self.result1 = min(results)
        self.time1 = timer()
        return self.result1
        
    def explore(self, current, history, target, stop_at_first_target=False):
        # self.grid_enter_result(this_list=[current], term='O', print_grid=True)
        # print("~"*30)
        distance = 500
        if current in history:
            return None
        history= history + [current]
        current_points = len(history)
        if current == target:
            if current_points < self.max_steps:
                self.paths = []
            self.paths.append(history)
            if self.max_steps == 0:
                self.max_steps = current_points
            else:
                self.max_steps = min(current_points, self.max_steps) 
            # print(f'{len(self.paths)}th result: points: {current_points }')
            if self.result_explore == 0:
                self.result_explore = current_points 
            else:
                self.result_explore = min(self.result_explore, current_points)
            return None
        elif current in self.walls:
            return None

        # if not self.result_explore == 0:  # check if we can still even reach the target sooner than previously:
        distance = abs(current[0] - target[0]) + abs(current[1] - target[1])
        max_dist = self.result_explore if  self.result_explore > 0 else 299
        if distance + current_points > max_dist:
            return None
        
        if self.max_steps > 0 and current_points > self.max_steps:
            return None
        if current in self.traced:
            if current_points >= self.traced[current]:
                return None
            elif current_points < self.traced[current]:
                self.traced[current] = current_points
                print(f'OVERWRITING {len(self.traced)} plots entered. This position: {current} This history has {len(history)} steps. points: {self.result_explore}. Remaining distance: {distance}')
        else:
            self.traced[current] = current_points
            self.grid_enter_result(this_list=[current], term='O', print_grid=True)
            print(f'{len(self.traced)} plots entered. This position: {current} This history has {len(history)} steps. current_shortest_route: {self.result_explore}. Remaining distance: {distance}')
        # self.traced[current] = current_points
        # else:
        # next_positions = self.neighbors[current] - set(history)
        next_positions = sorted(
                self.neighbors[current] - set(history),
                key=lambda pos: abs(pos[0] - target[0]) + abs(pos[1] - target[1])
            )
# =============================================================================
#         next_positions = sorted(
#             self.neighbors[current] - set(history),
#             key=lambda pos: (
#                 -1 if pos[0] > current[0] else 0,  # Prioritize southern positions (row index increases)
#                 abs(pos[0] - target[0]) + abs(pos[1] - target[1])  # Then sort by distance
#             )
#         )
# =============================================================================
# =============================================================================
#         next_positions = sorted(
#             self.neighbors[current] - set(history),
#             key=lambda pos: (
#                 -max(abs(pos[0] - target[0]), abs(pos[1] - target[1])),  # Greatest distance first
#                 -1 if pos[0] > current[0] else (1 if pos[0] < current[0] else 0),  # South first, then North
#                 -1 if pos[1] > current[1] else (1 if pos[1] < current[1] else 0)   # East first, then West
#             )
#         )
# =============================================================================
        for next_pos in next_positions:
            if next_pos == target:
                # breakpoint()
                pass
            # this_history = history.copy()
            # this_history.append(next_pos)
            self.explore(current=next_pos, history=history, target=target)
                
    
    def drop_bytes(self, number):
        to_drop = self.byte_list[self.drop_count:self.drop_count+number+1]
        self.drop_count += number
        self.walls.extend(to_drop)
        # self.walls = self.walls
        self.steps = list(set(self.steps) - set(self.walls))
        self.grid_enter_result(this_list=to_drop, term='#')
        self.print_grid()
    
            
    def part2(self):
        # lines = self.parse_lines()
        # breakpoint()
        blocked = False
        dropped = 12 if self.simple else 1024
        dropping = (byte for byte in self.byte_list[dropped:])
        path = set(self.paths[0])
        while not blocked:
            byte = next(dropping)
            if byte in path:
                blocked = True
                self.result2 = byte
                
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
    # self.print_grid()
    


# simple part 2
    today.set_lines(simple=True) 
    today.part2()
    print(f'Part 2 <SIMPLE> result is: {today.result2}')
# hard part 1
    today.set_lines(simple=False)
    today.part1()
    print(f'Part 1 <HARD> result is: {today.result1}')
    today.stop()
    # 522 too high\
    # 299 too high

# hard part 2
    today.set_lines(simple=False)
    today.part2()
    print(f'Part 2 <HARD> result is: {today.result2}')
    today.stop()
    today.print_final()