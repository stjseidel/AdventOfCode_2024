#!/usr/bin/env python3
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
        # lines = [[int(lin) for lin in line.split(' ') if set(lin) != set('') ] for line in lines]
        return lines
    
    def part1(self):
        lines = self.parse_lines()
        self.result1 = sum([self.get_nth_secret(secret=int(line), nth=2000) for line in self.lines])
        self.time1 = timer()
            
        # self.get_nth_secret(secret=123, nth=10)
        return self.result1
                
    def part2(self):
        lines = self.parse_lines()
        self.monkeys = {}
        sequences = defaultdict(int)
        # get the monkey values and the sequences for first 7, 8, 9 values of each
        for monk, line in enumerate(lines):
            self.secret = int(line)
            prices = [int(str(self.get_next_secret())[-1]) for _ in range(2000)]
            differences = [prices[i]-prices[i-1] if i > 0 else 0 for i in range(len(prices))]
            diff_string = ''.join([str(val) for val in differences])
            prices[:4] = [0, 0, 0, 0]
            self.monkeys[monk] = {'prices':prices, 'differences':differences, 'diff_string':diff_string}
            for num in [7, 8, 9]:
                indices = [i for i in range(len(prices)) if prices[i] == num]
                for index in indices:
                    sequence = tuple(differences[index-3: index+1])
                    sequences[sequence] += num
        # sort by highest values per sequence, then pick the 3 best ones
        sorted_by_values = sorted(sequences.items(), key=lambda item: item[1], reverse=True)
        
        picked_sequences = [seq[0] for seq in sorted_by_values[:100]]
        picked = defaultdict(int)
        highest = 0
        for sequence in picked_sequences:
            # print(sequence)
            seq = ''.join([str(val) for val in sequence])
            for monk, monk_dict in self.monkeys.items():
                diff_string = monk_dict['diff_string']
                if seq in diff_string:
                    reference = diff_string.index(seq)
                    if seq[0] != '-':
                        if diff_string[reference-1] == '-':
                            continue
                    index = len([char for char in diff_string[:reference] if char != '-']) + 3
                    try:
                        picked[sequence] += monk_dict['prices'][index]
                    except:
                        pass
            # print(sequence, picked[sequence], 'current maxima:', highest)
            if picked[sequence] > highest:
                highest = picked[sequence]
                # print('New maxima at sequence', sequence, '. the max: ', highest)
        # picked_values = sorted(picked.items(), key=lambda item: item[1], reverse=True)
        
        self.result2 = highest
        
        self.time2 = timer()
        return self.result2
        
    def print_final(self):
        print(f'Part 1 result is: {self.result1}. (time: {round(self.time1 - self.beginning_of_time, 2)})')
        print(f'Part 2 result is: {self.result2} (time: {round(self.time2 - self.time1, 2)})')
        
    def get_next_secret(self, secret=None):
        secret = secret or self.secret
        secret = (secret ^ (secret * 64) % 16777216)
        secret = (secret ^ (secret // 32) % 16777216)
        secret = (secret ^ (secret * 2048) % 16777216)
        self.secret = secret
        return secret

    def get_nth_secret(self, secret, nth):
        for i in range(nth):
            secret = self.get_next_secret(secret)
        return secret

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
