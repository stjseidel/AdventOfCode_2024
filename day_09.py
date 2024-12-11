#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 06:32:12 2023

@author: stjse
"""

from aoc_class import AOC
from timeit import default_timer as timer
from collections import OrderedDict
from collections import namedtuple
    
class Today(AOC):
        
    def parse_lines(self, file_path=''):
        # lines = self.lines
        # lines = [[int(lin) for lin in line.split(' ') if set(lin) != set('') ] for line in lines]
        return self.lines
    
    def part1(self):
        # _ = self.parse_lines()
        self.parse_disk()
        self.result1 = self.check_sum
        self.time1 = timer()
        return self.result1

    def parse_disk(self):
        # 12345
        # 0..111....22222
        self.line = self.lines[0]
        # self.line = '12345'
        
        self.file_size_total = sum([int(i) for i in self.line[::2]])
        self.file_count_total = len(self.line) // 2
        self.written = 0
        self.file_down = len(self.line)
        self.current_line_pos = -1
        self.check_sum = 0
        self.current_last_file = []
        self.current_file_id = -1
        self.current_last_file_id = self.file_count_total + 1
        self.current_line_pos_back = len(self.line) + len(self.line)  % 2  
        self.disk_pos = -1
        self.this_space = []
        while self.written <= self.file_count_total:
            # self.this_file = self.line[self.current_line_pos]
            self.get_next_file()
            # while len(self.this_space)
            self.get_next_space()
            if len(self.this_space) > 0:
                self.fill_from_back()
        if len(self.current_last_file) > 0:
            self.this_space = list(range(self.disk_pos, self.disk_pos + len(self.current_last_file)))
            self.fill_from_back()
            
                
    def print_status(self):
        print(f'{self.current_line_pos}: disk_pos: {self.disk_pos}; check_sum {self.check_sum}; this_space: {self.this_space}; current_last_file: {self.current_last_file}')
            
    def get_next_file(self):
        self.current_line_pos += 1
        self.current_file_id += 1
        file_size = int(self.line[self.current_line_pos])
        # print(f'fetched file {self.written}: file ID: {self.current_file_id}; size: {file_size}')
        self.next_pos = self.disk_pos + file_size
        for i in range(self.disk_pos, self.next_pos):
            self.disk_pos += 1
            self.check_sum += self.disk_pos* self.current_file_id 
            # self.print_status()
        self.written += 1
        # self.disk_pos = self.next_pos
        
    def get_next_space(self):
        try:
            self.current_line_pos += 1
            self.next_pos = self.disk_pos + int(self.line[self.current_line_pos])
            self.this_space = list(range(self.disk_pos, self.next_pos))
            # self.disk_pos = self.next_pos
            # self.print_status()
            # print(f'fetched SPACE. files written: {self.written}: file ID: {self.current_file_id}; size: {self.this_space}')
        except Exception as e:
            self.this_space =  list(range(self.disk_pos, self.disk_pos + len(self.current_last_file)))
        return self.this_space
        
    def fill_from_back(self):
        while len(self.this_space) > 0:
            if self.current_last_file == []:
                if not self.written <= self.file_count_total:
                    pass
                else:
                    self.get_last_file()
            if len(self.current_last_file) > 0:
                self.disk_pos += 1
                self.check_sum += self.disk_pos * self.current_last_file[0]
                self.current_last_file.pop(0)
                self.this_space.pop(0)
                # self.print_status()
            else:
                return None
            
            
    def get_last_file(self):
        self.current_line_pos_back -= 2
        self.current_last_file_id -= 1
        self.current_last_file = [self.current_last_file_id] * int(self.line[self.current_line_pos_back])
        # self.print_status()
        # print(f'fetched LAST file {self.written}: file position: {self.current_line_pos_back}; size: {self.current_last_file}')
        self.written += 1
        
        
    def part2(self):
        # lines = self.parse_lines()
        files = self.defragment()
        self.calc_checksum(files=files)
        self.result2 = self.check_sum
        self.time2 = timer()
        return self.result2
    
    def defragment(self):    
        files = []
        spaces = []
        Range = namedtuple('Range', ['file_num', 'size', 'start_position', 'file_type', 'overwritten'])
        disk_pos = 0
        for i, num in enumerate(self.lines[0]):
            size = int(num)
            if i % 2 == 0:  # is file
                file_num = i // 2
                files.append(Range(file_num=file_num, size=size, start_position=disk_pos, file_type='file', overwritten='N/A'))
            else:
                file_num = i // 2
                spaces.append(Range(file_num=file_num, size=size, start_position=disk_pos, file_type='space', overwritten=False))
            disk_pos += size
        
        for nth_file in range(len(files)-1, -1, -1):
            file = files[nth_file]
            print(nth_file, file.file_num, file.start_position)
            
            for n, space in enumerate(spaces):
                if space.start_position > file.start_position:
                    break
                elif space.overwritten:
                    continue
                if space.size >= file.size:
                    print('old:', file)
                    files[nth_file] = Range(file_num=file.file_num, size=file.size, start_position=space.start_position, file_type='file', overwritten='N/A')
                    if file.size < space.size:
                        print(spaces[n])
                        spaces[n] = Range(file_num=space.file_num, size=file.size, start_position=space.start_position, file_type=space.file_type + '_split', overwritten=True)
                        spaces.insert(n+1, Range(file_num=space.file_num, size=space.size-file.size, start_position=space.start_position+(space.size-file.size)+1, file_type='new', overwritten=False))
                        print(spaces[n])
                        print('added new space:\n', spaces[n+1])
                    else:
                        spaces[n] = Range(file_num=space.file_num, size=space.size, start_position=space.start_position, file_type='space', overwritten=True)
                    print('new:', files[nth_file])
                    break
        for space in spaces:
            print(space)
        return files
    
    def calc_checksum(self, files):
        # print('check_sum:')
        check_sum = 0
        for file in files:
            for i in range(file.size):
                start_pos = file.start_position
                check_sum += (start_pos + i) * file.file_num
                print(file.file_num, file.start_position+i, file.size, check_sum)
        self.check_sum = check_sum
        
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
    # 6427431214608 too low