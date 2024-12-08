#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 06:32:12 2023

@author: stjse
"""

from aoc_class import AOC
from timeit import default_timer as timer
from itertools import combinations
from collections import defaultdict
    
class Today(AOC):
    print_results = False
    
    def parse_lines(self, file_path=''):
        lines = self.lines
        self.antennas = self.grid_extract_all_character_positions_to_dict(ignore_chars=['.'])
        self.positions_all = self.grid_make_all_positions()
        # lines = [[int(lin) for lin in line.split(' ') if set(lin) != set('') ] for line in lines]
        return lines
    
    def part1(self):
        _ = self.parse_lines()
        self.grid_make_empty()
        self.antinodes = set()
        for antenna, positions in self.antennas.items():
            self.compute_antenna_antinodes(antenna, positions)
        self.result1 = len(self.antinodes)
        self.time1 = timer()
        return self.result1
    
    def compute_antenna_antinodes(self, antenna, positions):
        combos = combinations(positions, 2)
        distance_combos = [(1, 2), (-1, -2), (2, 1), (-2, -1)]
        for comb in combos:
            
            pos1, pos2 = comb[0], comb[1]
            distance = pos1 - pos2
            for distance_combo in distance_combos:
                self.nodes = defaultdict(lambda: 0)
                for i, distance_multiplier in enumerate(distance_combo):
                    position = comb[i]
                    node = position + distance * distance_multiplier
                    if not tuple(node) in self.positions_all:
                        continue
                    # print(f'node {node}: {position} + {distance} * {distance_multiplier}')
                    self.nodes[tuple(node)] += 1
                antinodes = [(node) for node in self.get_keys_with_value_equal_to(input_dict=self.nodes, equal_to=2)]
                self.grid_enter_result(this_list=antinodes, term=antenna, print_grid=self.print_results)
                for node in antinodes:
                    self.antinodes.add(node)
        return None
    
    def get_keys_with_value_equal_to(self, input_dict, equal_to=2):
        return [key for key, value in input_dict.items() if value == equal_to]
                
    def  part2(self):
        _ = self.parse_lines()
        self.grid_make_empty()
        self.antinodes = set()
        for antenna, positions in self.antennas.items():
            self.compute_antenna_antinodes_harmonic(antenna, positions)
        self.result2 = len(self.antinodes)
        self.time2 = timer()
        return self.result2
    
    def compute_antenna_antinodes_harmonic(self, antenna, positions):
        if len(positions) < 2:
            return None
        combos = combinations(positions, 2)
        distance_combos = [(1), (-1)]
        for comb in combos:
            pos1, pos2 = comb[0], comb[1]
            distance = pos1 - pos2
            for distance_combo in distance_combos:
                position = pos1.copy()
                while tuple(position) in self.positions_all:
                    if not tuple(position) in self.antinodes:
                        self.grid_enter_result(this_list=[position], term=antenna, print_grid=self.print_results)
                    self.antinodes.add(tuple(position))
                    position += distance * distance_combo
        return None
    
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