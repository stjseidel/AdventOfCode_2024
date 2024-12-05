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
        read_orders = True
        order, updates = {}, []
        order = defaultdict(lambda: [])
        for line in lines:
            if line == '' or line == ' ':
                read_orders = False
            elif read_orders:
                page, before = line.split('|')
                order[page].append(before)
            else:
                updates.append(line.split(','))
        self.order = order
        self.updates = updates
        # lines = [[int(lin) for lin in line.split(' ') if set(lin) != set('') ] for line in lines]
        return lines
    
    def part1(self):
        lines = self.parse_lines()
        self.result1 = 0
        for update in self.updates:
            self.result1 += self.check_update(update)
        self.time1 = timer()
        return self.result1
                
    def check_update(self, update):
        # if any later_pa
        # for i, page in enumerate(update[::-1]):  ## stepping through backwards, so earlier and later pages are swapped
        for i in range(len(update)-1, -1, -1):    
            page = update[i]
            earlier_pages  = update[:i]
            
            for earlier_page in earlier_pages:
                if earlier_page in self.order[page]:
                    return 0
        middle_page_index = (len(update)) // 2        
        return int(update[middle_page_index])
        
    def part2(self):
        lines = self.parse_lines()
        self.result2 = 0
        self.incorrect_orders = []
        for update in self.updates:
            if self.check_update(update) == 0:
                self.incorrect_orders.append(update)
        
        for update in self.incorrect_orders:
            self.result2 += self.order_update(update)
        self.time2 = timer()
        return self.result2
        
    def order_update(self, update):
        # for i in range(len(update)-1, -1, -1):    
        #     page = update[i]
        #     earlier_pages  = update[:i]
        #     # print(earlier_pages, page)
        this_dict = {}
        for page in update:
            this_dict[page] = [earlier for earlier in self.order[page] if earlier in update]
            # for earlier_page in earlier_pages:
            #     if earlier_page in self.order[page]:
        orders = {page:len(earlier) for page, earlier in this_dict.items()}
        
        middle_page_index = (len(update)) // 2  
        for key, order in orders.items():
            if str(order) == str(middle_page_index):
                return int(key)
        return 0
        # return int(update[middle_page_index])
        
    def print_final(self):
        print(f'Part 1 result is: {self.result1}. (time: {round(self.time1 - self.beginning_of_time, 2)})')
        print(f'Part 2 result is: {self.result2} (time: {round(self.time2 - self.time1, 2)})')
        

if __name__ == '__main__':
# prep
    today = Today(day='05', simple=True)
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