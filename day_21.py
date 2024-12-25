#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 06:32:12 2023

@author: stjse
"""

from aoc_class import AOC
from timeit import default_timer as timer

    
class Today(AOC):
    numpad_list = [[7, 8, 9], [4, 5, 6], [1, 2, 3], [None, 0, 'A']][::-1]
    numpad = {
         str(button): (row, col)
         for row, line in enumerate(numpad_list)
         for col, button in enumerate(line[::-1])
         if button is not None  # Exclude None as a button
         }
    
    dirpad_list = [['<', 'v', '>'], [None, '^', 'A']]
    
    dirpad = {
         str(button): (row, col)
         for row, line in enumerate(dirpad_list)
         for col, button in enumerate(line[::-1])
         if button is not None  # Exclude None as a button
         }
    
    pad_maps = {'door_numpad':numpad,
                  'dirpad_1':dirpad,           
                  'dirpad_2':dirpad,               
                  'dirpad_3':dirpad}
        
    def parse_lines(self, file_path=''):
        lines = self.lines
        # self.reset_robots()
        # lines = [[int(lin) for lin in line.split(' ') if set(lin) != set('') ] for line in lines]
        # Directional  _^A/<v>
        # Directional  _^A/<v>
        # numerical 789/456/123/_0A
        return lines
    
    
    def robot_to_pad(self, button, robot):
        pad_map = self.pad_maps[robot]
        old_pos = self.robots[robot]
        new_pos = pad_map[button]
        self.robots[robot] = new_pos
        offset_x = new_pos[1] - old_pos[1]
        offset_y = new_pos[0] - old_pos[0]
        history = ''
        if offset_x < 0:
            history += '>' * abs(offset_x)
        

        if offset_y > 0:
            history += '^' * offset_y
        elif offset_y < 0:
            history += 'v' * abs(offset_y)

        if offset_x > 0:
            history += '<' * offset_x
        
        history += 'A'
        print(f'{robot}: [{button}]. Moving from {old_pos} to {new_pos}. {history}')
        return history
        
    def reset_robots(self):
        self.robots = {'door_numpad':(0, 0),
                        'dirpad_1':(1, 0),           
                        'dirpad_2':(1, 0),               
                        'dirpad_3':(1, 0)}   
    
    def part1(self):
        lines = self.parse_lines()
        results = {}
        self.reset_robots()
        for line in lines:
            robot1 = ''.join([self.robot_to_pad(char, robot='door_numpad') for char in line])
            
            robot2 = ''.join([self.robot_to_pad(char, robot='dirpad_1') for char in robot1])
            robot3 = ''.join([self.robot_to_pad(char, robot='dirpad_2') for char in robot2])
            results[line] = robot3
            if line == '029A':
                print(robot1 == '<A^A>^^AvvvA')
                print(robot2 == 'v<<A>>^A<A>AvA<^AA>A<vAAA>^A')
                print(robot3 == '<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A')
                
        
        result1 = 0
        command_lengths = [68, 60, 68, 64, 64]
        for i, (code, history) in enumerate(results.items()):
            print(code, len(history), history)
            print(f'should: {command_lengths[i]}, is: {len(history)} {command_lengths[i] == len(history)}')
            result1 += int(code[:-1]) * len(history)
            
        self.result1 = result1
        self.time1 = timer()
        return self.result1
                
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
    # 169612 too high
    # 168780 too high

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