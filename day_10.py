#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 06:32:12 2023

@author: stjse
"""

from aoc_class import AOC
from timeit import default_timer as timer
from collections import namedtuple
    
MapCoord = namedtuple('MapCoord', ['row', 'col', 'height', 'position', 'id_num'])

class Today(AOC):
        
    
    def parse_lines(self, file_path=''):
        lines = self.lines
        self.all_positions = []
        id_num = -1
        for row, line in enumerate(self.lines):
            for col, height in enumerate(line):
                if height == '.':
                    pass
                else:
                    height = int(height)
                    if height == 0:
                        position = 'start'
                    elif height == 9:
                        position = 'target'
                    else:
                        position = False
                    id_num += 1
                    self.all_positions.append(MapCoord(row=row, col=col, height=height, position=position, id_num=id_num))
        self.start_positions = list(filter(self.is_start, self.all_positions))
        self.target_positions = list(filter(self.is_target, self.all_positions))
        # lines = [[int(lin) for lin in line.split(' ') if set(lin) != set('') ] for line in lines]
        print(f'starts: {len(self.start_positions)}; targets: {len(self.target_positions)}; total_positions: {len(self.all_positions)}')
        return lines
    
    def is_start(self, coord):
        return coord.position == 'start'
    
    def is_target(self, coord):
        return coord.position == 'target'
    
    def is_not_id_num(self, coord, id_num):
        return coord.id_num != id_num
    
    def is_adjacent_and_increasing(self, coord, reference):
        # print(f'checking: {self.print_coords(coord)}, {self.print_coords(reference)}')
        coord_diff = ((coord.row - reference.row), (coord.col - reference.col))
        allowed_diffs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        result = (coord_diff in allowed_diffs) &  ((coord.height - reference.height) in [1, 0])
        # if result:
        #     print('FOUND A MATCH!')
        return result
        
    def print_coords(self, coord):
        print(f'[{coord.row}, {coord.col}, {coord.height}]')
    
    def part1(self):
        lines = self.parse_lines()
        self.scout_all_paths_starts()
        self.result1 = self.total_score
        self.time1 = timer()
        return self.result1
                
    def scout_all_paths_starts(self):
        self.total_score = 0
        
        for start in self.start_positions:
            self.scout_from_start(start)
    
    def scout_from_start(self, start):
        self.grid_make_empty()
        score = 0
        start.id_num
        remaining_positions = list(filter(lambda coord: self.is_not_id_num(coord, start.id_num), self.all_positions))
        newly_added = [start]
        self.grid_enter_result(this_list=[(start.row, start.col)], term=str('*'), print_grid=False)
        # print(f'starting at start: {self.print_coords(start)}')
        pop_list = []
        while len(newly_added) > 0:
            this_set = newly_added.copy()
            newly_added = []
            for this_start in this_set:
                for i, coord in enumerate(remaining_positions):
                    if not i in pop_list:
                        if self.is_adjacent_and_increasing(coord, this_start):
                            pop_list.append(i)
                            self.grid_enter_result(this_list=[(coord.row, coord.col)], term=str(coord.height), print_grid=False)
                            # print('')
                            if self.is_target(coord):
                                score += 1
                                # print(f'[score: {score}] from <{start.row}, {start.col}>, reached target <{coord.row}, {coord.col}>')
                            else:
                                newly_added.append(coord)
                _ = [remaining_positions.pop(i) for i in sorted(pop_list, reverse=True)]
                pop_list = []
        self.print_grid()
        self.total_score += score
        print(f'starting at start: {self.print_coords(start)}: Score {score} / {self.total_score}')
        
    
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
    # 1413 too high

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