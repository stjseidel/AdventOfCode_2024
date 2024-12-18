#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 06:32:12 2023

@author: stjse
"""

from aoc_class import AOC
from timeit import default_timer as timer
import numpy as np
import pandas as pd
from scipy.ndimage import label
    
class Today(AOC):

    def parse_lines(self, file_path=''):
        lines = self.lines
        self.Matrix = {(row, col):crop for row, line in enumerate(self.lines) for col, crop in enumerate(line)}
        self.Neighbors = {(row, col):[(row+1, col), (row, col+1), (row-1, col), (row, col-1)] & self.Matrix.keys() for (row, col) in self.Matrix}
        self.Neighbors = {plot:[neigh for neigh in neighs if self.Matrix[neigh] == self.Matrix[plot]] for plot, neighs in self.Neighbors.items()}       
        self.fences = {(row, col):4-len(self.Neighbors[(row, col)]) for (row, col) in self.Matrix}
        # lines = [[int(lin) for lin in line.split(' ') if set(lin) != set('') ] for line in lines]
        return lines
    
    def part1(self):
        _ = self.parse_lines()
        self.fenced = set()     
        self.areas = []
        _ = [self.get_area_fence(plot, crop) for plot, crop in self.Matrix.items()]
        self.get_fencing_cost_from_areas()
        self.result1 = self.fencing_cost
        self.time1 = timer()
        return self.result1
    
    
    def get_area_fence(self, plot, crop, area=[]):
        if plot in self.fenced:
            return None
        matched = [plot]
        area = set([plot])
        while len(matched) > 0:
            self.fenced.update(matched)
            plot = matched[-1]
            matched.pop(-1)
            new = (set([plot for plot in self.Neighbors[plot] if self.Matrix[plot] == crop]) - self.fenced)
            self.fenced.update(new)
            matched.extend(new)
            area.update(new)
        if len(matched) == 0:
            self.areas.append(area)
            return area
        
    def get_fencing_cost_from_areas(self, areas=None):
        areas = areas or self.areas
        self.fencing_cost = sum([sum([self.fences[plot] for plot in area])*len(area)  for area in areas])
        return self.fencing_cost
        
    def part2(self):
        _ = self.parse_lines()
        self.areas = []
        self.fenced = set()     
        _ = [self.get_area_fence(plot, crop) for plot, crop in self.Matrix.items()]
        self.result2 = self.get_bulk_fencing_cost_from_areas()
        self.time2 = timer()
        return self.result2

    def get_bulk_fencing_cost_from_areas(self, areas=None):
        areas = areas or self.areas
        cost = 0
        for area in areas:
            cost += self.count_unbroken_edges(area=area)
        self.fencing_cost = cost
        return self.fencing_cost
                    
    def count_unbroken_edges(self, area):
        return 0
        

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

# =============================================================================
# # hard part 2
#     today.set_lines(simple=False)
#     today.part2()
#     print(f'Part 2 <HARD> result is: {today.result2}')
#     today.stop()
#     today.print_final()
# =============================================================================