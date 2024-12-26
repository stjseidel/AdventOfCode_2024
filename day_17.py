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
        # lines = [[int(lin) for lin in line.split(' ') if set(lin) != set('') ] for line in lines]
        self.reg_a = int(self.lines[0].split(':')[-1])
        self.reg_b = int(self.lines[1].split(':')[-1])
        self.reg_c = int(self.lines[2].split(':')[-1])
        self.program = [int(char) for char in self.lines[-1].split(':')[-1].split(',')]
        # self.operations = self.chunk_line(line=self.program, n=2)
        return lines
    
    def part1(self):
        self.part = 1
        lines = self.parse_lines()
        self.run_program()            
        self.result1 = self.get_result()
        self.time1 = timer()
        return self.result1
            
    def run_program(self):
        self.jumper = 0
        self.output = []
        # self.print_status()
        self.end_project_run = False
        while self.jumper < len(self.program):
            if self.end_project_run:  # for 2nd part
                return None
            opcode, value = self.program[self.jumper:self.jumper+2]
            self.run_up(opcode, value)
            # print(f'{self.jumper}, [{opcode}, {value}]. {self.reg_a}, {self.reg_b}, {self.reg_c}. Output: <{self.output}>')
        # self.print_output()
        
    def run_up(self, opcode, value):
        # print(f'{opcode}, {value}')
        match opcode:
            case 0:
                return self.adv(value)
            case 1:
                return self.bxl(value)
            case 2:
                return self.bst(value)
            case 3:
                return self.jnz(value)
            case 4:
                return self.bxc(value)
            case 5:
                return self.out(value)
            case 6:
                return self.bdv(value)
            case 7:
                return self.cdv(value)
        self.jumper += 2
        return None
                
    def adv(self, value):
        """The adv instruction (opcode 0) performs division.
        The numerator is the value in the A register.
        The denominator is found by raising 2 to the power of the instruction's combo operand.
        (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.)
        The result of the division operation is truncated to an integer and then written to the A register."""
        self.reg_a = self.reg_a // (2**self.combo(value))
        self.jump()
    
    def bxl(self, value):
        """The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, 
        then stores the result in register B."""
        self.reg_b ^= value
        self.jump()
        
    def bst(self, value):
        """The bst instruction (opcode 2) calculates the value of its
        combo operand modulo 8 (thereby keeping only its lowest 3 bits), 
        then writes that value to the B register."""
        self.reg_b = self.combo(value) % 8
        self.jump()
        
    def jnz(self, value):
        """The jnz instruction (opcode 3) does nothing if the A register is 0. 
        However, if the A register is not zero, it jumps by setting the instruction 
        pointer to the value of its literal operand; if this instruction jumps, 
        the instruction pointer is not increased by 2 after this instruction."""
        if self.reg_a == 0:
            self.jump()
        else:
            self.jump(value)
        
        
    def bxc(self, value):
        """The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C,
        then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)"""
        self.reg_b ^= self.reg_c
        self.jump()
        
    def out(self, value):
        """The out instruction (opcode 5) calculates the value of its combo operand modulo 8,
        then outputs that value. (If a program outputs multiple values, they are separated by commas.)"""
        self.output.append(self.combo(value) % 8)
        if self.part == 2:
            if self.output == self.program[:len(self.output)]:
                pass
            else:
                self.end_project_run = True
        self.jump()
        
    def bdv(self, value):
        """The bdv instruction (opcode 6) works exactly like the adv instruction
        except that the result is stored in the B register.
        (The numerator is still read from the A register.)"""
        self.reg_b = self.reg_a // (2**self.combo(value))
        self.jump()
        
    def cdv(self, value):
        """The cdv instruction (opcode 7) works exactly like the adv instruction 
        except that the result is stored in the C register.
        (The numerator is still read from the A register.)"""
        self.reg_c = self.reg_a // (2**self.combo(value))
        self.jump()
        
    def jump(self, value=None):
        if value is None:
            self.jumper += 2
        else:
            self.jumper = value
        
    def combo(self, value):
        if value in [0, 1, 2, 3]:
            return value
        match value:
            case 4:
                return self.reg_a
            case 5:
                return self.reg_b
            case 6:
                return self.reg_c
            case 7:
                return None # invalid!
        return None # not happening?
            
    def print_output(self):
        print('~'*30)
        print('result output: ')
        print(','.join([str(out) for out in self.output]))
        
    def get_result(self):
        return ','.join([str(out) for out in self.output])
            
    def part2(self):
        self.part = 2
        lines = self.parse_lines()
        self.scan_reg_a()
        # self.result2 = 'TODO'
        self.time2 = timer()
        return self.result2
    
    def scan_reg_a(self):
        found = False
        
        # digit = -1
        digit = 70026359
        if self.simple:
            reg_b = 0
            reg_c = 0
            program = [0,3,5,4,3,0]
            
        else:
            reg_b = self.reg_b
            reg_c = self.reg_c
            program = self.program
            
        while not found:
            digit += 1
            # print(f'run {digit}')
            self.reg_a = digit
            self.reg_b, self.reg_c = reg_b, reg_c
            self.program = program
            self.run_program()
            if self.output == self.program:
                found = True
                self.result2 = digit
            
    
    def print_final(self):
        print(f'Part 1 result is: {self.result1}. (time: {round(self.time1 - self.beginning_of_time, 2)})')
        print(f'Part 2 result is: {self.result2} (time: {round(self.time2 - self.time1, 2)})')
        
        
        
    def test_1(self):
        """If register C contains 9, the program 2,6 would set register B to 1."""
        self.reg_a = 0
        self.reg_b = 0
        self.reg_c = 9
        self.program = [2, 6]
        self.run_program()
        assert self.reg_b == 1
        
    def test_2(self):
        """If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2."""
        self.reg_a = 10
        self.reg_b = 0
        self.reg_c = 0
        self.output = []
        self.program = [5, 0, 5, 1, 5, 4]
        self.run_program()
        assert self.output == [0, 1, 2]

    def test_3(self):
        """If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A."""
        self.reg_a = 2024
        self.reg_b = 0
        self.reg_c = 0
        self.program = [0, 1, 5, 4, 3, 0]
        self.run_program()
        assert self.output == [4,2,5,6,7,7,7,7,3,1,0]
        assert self.reg_a == 0

    def test_4(self):
        """If register B contains 29, the program 1,7 would set register B to 26."""
        self.reg_a = 0
        self.reg_b = 29
        self.reg_c = 0
        self.program = [1, 7]
        self.run_program()
        assert self.reg_b == 26
        
    def test_5(self):
        """If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354."""
        self.reg_a = 0
        self.reg_b = 2024
        self.reg_c = 43690
        self.program = [4, 0]
        self.run_program()
        assert self.reg_b == 44354
        
    def print_status(self):
        print('~'*30)
        print(f'Simple run: {self.simple}')
        print(f'Register A: {self.reg_a}')
        print(f'Register B: {self.reg_b}')
        print(f'Register C: {self.reg_c}\n')
        print(f'Program: {self.program}. Jumper: {self.jumper}')

if __name__ == '__main__':
# prep
    today = Today(day='', simple=True)
    today.part = 1
    today.create_txt_files()

    today.set_lines(simple=True)
    today.test_1()
    today.test_2()
    today.test_3()
    today.test_4()
    today.test_5()
    

# simple part 1
    today.set_lines(simple=True)
    today.part1()
    print(f'Part 1 <SIMPLE> result is: {today.result1}')
    
# hard part 1
    today.set_lines(simple=False)
    today.part1()
    print(f'Part 1 <HARD> result is: {today.result1}')
    today.stop()
    # 413324647
    # 4,1,3,3,2,4,6,4,7


# simple part 2
    today.set_lines(simple=True) 
    today.part2()
    print(f'Part 2 <SIMPLE> result is: {today.result2}')

# # # hard part 2
# # brute force ain't gonna be helping here
#     today.set_lines(simple=False)
#     today.part2()
#     print(f'Part 2 <HARD> result is: {today.result2}')
#     today.stop()
#     today.print_final()
#     # 70026359
    # 477097999