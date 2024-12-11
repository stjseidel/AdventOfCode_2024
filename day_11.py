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
        self.memo = {}
        return lines
    
    def part1(self):
        _ = self.parse_lines()
        total_stones = self.process_stones(blinks=25)
        self.result1 = total_stones 
        self.time1 = timer()
        return self.result1

    def process_stones(self, blinks):
         """
         Initialize the recursive process for the given number of blinks.
         """
         self.blinks = blinks
         self.memo = {}  
         initial_stones = self.stone_lists[0]
    
         total_result = 0
         for stone in initial_stones:
             total_result += self.blink_stone(stone, blinks)
    
         return total_result
  
    def blink_stone(self, stone, remaining_blinks):
        """
        Process a stone recursively, summing up results for the remaining blinks.
        """
        if remaining_blinks == 0:
            return 1

        if (stone, remaining_blinks) in self.memo:
            return self.memo[(stone, remaining_blinks)]

        if stone == 0:
            result = self.blink_stone(1, remaining_blinks - 1)
        else:
            stone_chars = str(stone)
            stone_char_length = len(stone_chars)

            if stone_char_length % 2 == 0:
                midpoint = stone_char_length // 2
                left = int(stone_chars[:midpoint]) 
                right = int(stone_chars[midpoint:])
                result = (
                    self.blink_stone(left, remaining_blinks - 1)
                    + self.blink_stone(right, remaining_blinks - 1)
                )
            else:
                result = self.blink_stone(stone * 2024, remaining_blinks - 1)

        self.memo[(stone, remaining_blinks)] = result
        return result


    def part2(self):
        _ = self.parse_lines()
        total_stones = self.process_stones(blinks=75)
        self.result2 = total_stones 
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

# hard part 2
    today.set_lines(simple=False)
    today.part2()
    print(f'Part 2 <HARD> result is: {today.result2}')
    today.stop()
    today.print_final()