#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 06:32:12 2023

@author: stjse
"""

from aoc_class import AOC
from timeit import default_timer as timer
import re
from collections import defaultdict
    
class Today(AOC):
        
    def parse_lines(self, file_path=''):
        lines = self.lines
        self.options = self.lines[0].split(', ')
        self.patterns = self.lines[2:]
        # lines = [[int(lin) for lin in line.split(' ') if set(lin) != set('') ] for line in lines]
        return lines
    
    def part1(self):
        _ = self.parse_lines()
        self.result1 = 0
        
        for i, pattern in enumerate(self.patterns):
            self.solved = False
            self.memo = defaultdict(list)
            if not self.is_solvable(pattern):
                continue
            _ = self.decode_pattern(pattern=pattern, done='')
            if self.solved:
                self.result1 += 1
        self.time1 = timer()
        return self.result1
                
    def decode_pattern(self, pattern, done, last_pattern=None):
        if self.solved:
            return 1
        remaining = pattern[len(done):]
        options = [pat for pat in self.options if re.match(pat, remaining)]
        if last_pattern is not None:
            if last_pattern in  self.memo[done]:
                return 0
            self.memo[done].append(last_pattern)
        if not self.is_solvable(pattern, options=options):
            return 0
        for opt in options:
            this_done = f'{done}{opt}'
            if this_done == pattern:
                self.solved = True
                return 1
            else:
                self.decode_pattern(pattern, done=this_done, last_pattern=opt)
        return 0
    
    def is_solvable(self, pattern, options=None):
        options = options or self.options
        pattern_chars = set(pattern)
        option_chars = set(''.join(self.options))
        if len(pattern_chars - option_chars) > 0:
            return False
        return True
    
    def part2(self):
        _ = self.parse_lines()
        self.solved_total = 0
        for i, pattern in enumerate(self.patterns):
            result = 0
            self.solved = False
            self.memo = defaultdict(list)
            if not self.is_solvable(pattern):
                continue
            result = self.solve_last_nth(pattern=pattern)
            self.solved_total += result
        self.time2 = timer()
        self.result2 = self.solved_total
        return self.solved_total
                
    def solve_last_nth(self, pattern):
        """move backwards and use memoization"""
        end_memo = defaultdict(int)
        end_options = defaultdict(list)
        match_results = {pattern[i:]:[opt for opt in self.options if opt == pattern[i:i+len(opt)]] for i in range(len(pattern)-1, -1, -1)}
        for i in range(len(pattern)-1, -1, -1):
            string = pattern[i:]
            string_length = len(string)
            options = match_results[string]
            this_branch = 0

            for opt in options:
                if opt in end_options[string_length]:
                    this_branch += end_memo[opt]
                else:
                    remaining_after_opt = len(string) - len(opt)
                    
                    if remaining_after_opt == 0:
                        end_memo[string_length] += 1
                        end_options[string_length].append(opt)
                    elif remaining_after_opt in end_memo.keys():
                        end_memo[string_length] += end_memo[remaining_after_opt]
                        end_options[string_length].append(opt)
                    else:
                        pass
            
        return end_memo[len(pattern)]
        
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
    6
# hard part 1
    today.set_lines(simple=False)
    today.part1()
    print(f'Part 1 <HARD> result is: {today.result1}')
    today.stop()

# # simple part 2
    today.set_lines(simple=True) 
    today.part2()
    print(f'Part 2 <SIMPLE> result is: {today.result2}')

# hard part 2
    today.set_lines(simple=False)
    today.part2()
    print(f'Part 2 <HARD> result is: {today.result2}')
    today.stop()
    today.print_final()
