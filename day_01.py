# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 06:32:12 2023

@author: stjse
"""

from aoc_class import AOC
from timeit import default_timer as timer
from collections import defaultdict
    
class Today(AOC):
        
    def parse_lines(self, file_path=''):
        lines = self.lines
        lines = [[int(lin) for lin in line.split(' ') if set(lin) != set('') ] for line in lines]
        left, right = zip(*lines)
        left = sorted(left)
        right = sorted(right)
        return lines, left, right
    
    def part1(self):
        lines, left, right = self.parse_lines()
        self.result1 = sum([abs(left[i]-right[i]) for i in range(len(lines))])
        self.time1 = timer()
        return self.result1
                
    def part2(self):
        lines, left, right = self.parse_lines()
        sim = defaultdict(lambda: 0)
        occurrence_left = defaultdict(lambda: 0)
        lefts = set(left)
        for entry in left:
            occurrence_left[entry] += 1
        
        for entry in right:
            if entry in lefts:
                sim[entry] += 1
        sim_index = [(entry * occurrence) * occurrence_left[entry] for entry, occurrence in sim.items()]
        
        self.result2 = sum(sim_index)
        self.time2 = timer()
        return self.result2
        
    def print_final(self):
        print(f'Part 1 result is: {self.result1}. (time: {round(self.time1 - self.beginning_of_time, 2)})')
        print(f'Part 2 result is: {self.result2} (time: {round(self.time2 - self.time1, 2)})')
        

if __name__ == '__main__':
# prep
    today = Today(day='1', simple=True)
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