#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 08:39:05 2024

@author: stjseidel
"""

import re
from timeit import default_timer as timer
import sys
from pathlib import Path
from datetime import datetime
from shutil import copy2

from math import gcd 
from functools import reduce 
import pandas as pd
import requests
from bs4 import BeautifulSoup
from dotenv import get_key


class AOC():
    def __init__(self, day='', simple=True):
        if day == '':
            try:
                day = Path(sys.modules[self.__module__].__file__).stem
            except Exception as e:
                print('Tried to set day from __file__: ', e)
                day = str(datetime.today().day).zfill(2)
        day = str(day).zfill(2)
        print('Working on day: ', day)
        self.template = Path('template.py')
        self.beginning_of_time = timer()
        self.day = day
        self.start()
        self.input_folder = Path('input')
        self.input = self.input_folder / f'{self.day}.txt'
        self.input_simple = self.input_folder  / f'{self.day}_simple.txt'
        self.simple = simple
        self.passed_days = min(datetime.now(), datetime(2024, 12, 24)).day
        if int(self.day) <= int(self.passed_days):        
            self.create_txt_files()
            self.read_both_files()
            self.set_lines(simple=simple)
        
        
    def start(self):
        self.beginning = timer()
        
    def stop(self):
        self.end = timer()
        print(f"{round(self.end - self.beginning, 2)} Seconds needed for execution")
        self.start()

    def read_both_files(self):
        file_path = self.input_folder / f'{self.day}_simple.txt'
        if not file_path.exists():
            print('no such file: ', file_path)
            self.lines_simple = []
        else:
            self.lines_simple = self.read_lines(file_path) 
        file_path = self.input_folder / f'{self.day}.txt'
        if not file_path.exists():
            print('no such file: ', file_path)
            self.lines_real = []
        else:
            self.lines_real = self.read_lines(file_path) 
    
    def set_lines(self, simple=False):
        if simple:
            self.lines = self.lines_simple
        else:
            self.lines = self.lines_real
    
    def read_lines(self, file_path=''):
        file_path = Path(file_path) 
        if not file_path.exists():
            file_path = self.input_folder / file_path
        with open(file_path) as fp:
            lines = fp.readlines()
        self.lines = [line.replace('\n', '') for line in lines]
        self.lines = [re.sub(' +', ' ', line) for line in self.lines]  # trim doubled spaces
        return self.lines

    def chunk_lines(self, n):
        self.lines = [self.chunk_line(line, n) for line in self.lines]
        
    def chunk_line(self, line, n):
        """Yield successive n-sized chunks from lst."""
        return [line[i:i + n] for i in range(0, len(line), n)]
            
# =============================================================================
#         for i in range(0, len(line), n):
#             yield line[i:i + n]
# =============================================================================

    def extract_numbers_from_lines(self, lines):
        # pattern = re.compile('\d+\.[.\d]+')
        return [str(''.join(filter(str.isdigit, line))) for line in lines]        
    
    def extract_numbers_from_string(self, line):
        # pattern = re.compile('\d+\.[.\d]+')
        return str(''.join(filter(str.isdigit, line)))

    def replace_with_dict(self, text, conversion_dict, before=None):
        before = before or str.lower
        t = before(text)
        for key, value in conversion_dict.items():
            t = t.replace(key, value)
        return t
    
    def create_txt_files(self):
        if not self.input.exists():
            self.fetch_input(int(self.day))
        if not self.input_simple.exists():
            self.fetch_input_simple(int(self.day))
                
    def get_soup(self, url):
        """Helper function to fetch the BeautifulSoup object for the day's page."""
        # url = f"https://adventofcode.com/2024/day/{day}"
        session_cookie = get_key('.env', 'SESSION_COOKIE')
        # Set up the headers with the session cookie
        HEADERS = {
            'Cookie': f'session={session_cookie}'
        }
        response = requests.get(url, headers=HEADERS)
        session_cookie = None
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
        else:
            print(f"Failed to fetch page for day {day}: {response.status_code}")
            return None        
    
    def fetch_input_simple(self, day: int):
        """Fetch and store the code from the <code> tag into 'day_simple.txt'."""
        url = f"https://adventofcode.com/2024/day/{day}"
        soup = self.get_soup(url)
        if soup:
            code_tag = soup.find('code')
            if code_tag:
                code_content = code_tag.get_text()
                
                file_path = self.input_simple
                with open(file_path, 'w') as file:
                    file.write(code_content)
                print(f"Saved simple code for day {day} to {file_path}")
            else:
                print(f"No <code> tag found for day {day}")
            
    def fetch_input(self, day: int):
        """Fetch and store the input from the <pre> tag into 'day.txt'."""
        url = f"https://adventofcode.com/2024/day/{day}/input"
        soup = self.get_soup(url)
        if soup:
            file_path = self.input
            with open(file_path, 'w') as file:
                file.write(soup.text)
            print(f"Saved input for day {day} to {file_path}")
        else:
            print(f"No input found for day {day}")

    
    def copy_template(self):
        this_file = Path(f'{str(self.day).zfill(2)}.py')
        if not this_file.exists():
            copy2(self.template, this_file)
                
    def lcm(self, denominators):
        # return least common denominator of a list of integers
        return reduce(lambda a,b: a*b // gcd(a,b), denominators)
    
    def transpose_lines(self, lines):
        lines_split = [[char for char in line] for line in lines]  # split lines into chars
        lines_T = pd.DataFrame(lines_split).T.values.tolist() 
        lines_T = [''.join(line) for line in lines_T]  # combine the split chars to strings
        return lines_T
    
    def border_coordinates(self, x_max, y_max):
        """Return a list of all coordinates at the border of a rectangle x,y (length of lines, line)"""
        border = []
    
        # Top and bottom borders
        for x in range(x_max):
            border.append((x, 0))            # Top border
            border.append((x, y_max - 1))    # Bottom border
    
        # Left and right borders (excluding corners to avoid duplicates)
        for y in range(1, y_max - 1):
            border.append((0, y))            # Left border
            border.append((x_max - 1, y))    # Right border
        return border
    
    def border_coordinates_of_lines(self, lines=''):
        lines = lines or self.lines
        return self.border_coordinates(len(lines[0]), len(lines))

                
if __name__ == '__main__':
    days = [str(i).zfill(2) for i in range(1, 25)]
    
    for day in days:
        today = AOC(day=day)
        today.copy_template()
       
    # day = '02'
    # today = AOC(day=day)
    # today.create_txt_files()
    # today.start()
    # today.stop