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
        self.stone_lists = [[int(chars) for chars in line.split(' ')] for line in lines]
        # lines = [[int(lin) for lin in line.split(' ') if set(lin) != set('') ] for line in lines]
        return lines
    
    def part1(self):
        lines = self.parse_lines()
        self.process_stones(blinks=25)
        self.result1 = self.total_stones
        # print(self.blink_result_list)
        self.time1 = timer()
        return self.result1

    def process_stones(self, blinks=25):
        self.blinks = blinks        
        self.total_stones = 0
        self.blink_result_list = []
        for stones in self.stone_lists:
            for stone in stones:
                self.blink_stone(stone=stone, current_blink=0)
                
                
    def blink_stone(self, stone, current_blink):
        """Process a stone recursively until the max blinks have been reached
        If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
        If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
        If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.
        """
        if current_blink >= self.blinks:
            self.total_stones += 1
            # self.blink_result_list.append(stone)
            return None
        if stone == 0:
            self.blink_stone(1, current_blink+1)
            return None
        stone_chars = str(stone) 
        stone_char_length = len(stone_chars)
        if stone_char_length % 2 == 0:
            left, right = int(stone_chars[stone_char_length // 2:]), int(stone_chars[:stone_char_length // 2])
            self.blink_stone(stone=left, current_blink=current_blink+1)
            self.blink_stone(stone=right, current_blink=current_blink+1)
            return None
        self.blink_stone(stone=stone*2024, current_blink=current_blink+1)
        return None
        
    def part2(self):
        lines = self.parse_lines()
        self.process_stones(blinks=75)
        self.result2 = self.total_stones
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