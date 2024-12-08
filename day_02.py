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
        lines = [[int(lin) for lin in line.split(' ') if set(lin) != set('') ] for line in lines]
        return lines
    
    def part1(self):
        lines = self.parse_lines()
        results = []
        for line in lines:
            result = self.check_line(line)
            results.append(result)
        self.result1 = sum(results)
        self.time1 = timer()
        return self.result1
                
    def check_line(self, line):
        direction = line[0] > line[1]
        if not self.step_height_safe(line[0], line[1]):
            return False
        prior = line[1]
        for element in line[2:]:
            down = prior > element
            if down != direction:
                return False
            if not self.step_height_safe(prior, element):
                return False
            prior = element
        return True

    def step_height_safe(self, a, b, step=3):
        if abs(a - b) > 3:
            return False
        elif a == b:
            return False
        else:
            return True
        
    def part2(self):
        lines = self.parse_lines()
        results = []
        for line in lines:
            result = self.check_line_with_dampener(line)
            results.append(result)
        self.result2 = sum(results)
        self.time2 = timer()
        return self.result2

    def check_line_with_dampener(self, line):
        is_safe = self.check_line(line)
        if is_safe:
            return True
        for n in range(len(line)):
            line_slice = line[:n] + line[n+1:]
            is_safe = self.check_line(line_slice)
            if is_safe:
                return True
        return False
        

    def print_final(self):
        print(f'Part 1 result is: {self.result1}. (time: {round(self.time1 - self.beginning_of_time, 2)})')
        print(f'Part 2 result is: {self.result2} (time: {round(self.time2 - self.time1, 2)})')
        

if __name__ == '__main__':
# prep
    today = Today(day='2', simple=True)
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

#       today.stop()
    today.set_lines(simple=False)
    today.part2()
    print(f'Part 2 <HARD> result is: {today.result2}')
    today.stop()
    today.print_final()