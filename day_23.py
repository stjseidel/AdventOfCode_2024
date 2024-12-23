#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 06:32:12 2023

@author: stjse
"""

from aoc_class import AOC
from timeit import default_timer as timer
from collections import defaultdict
import pandas as pd
from itertools import combinations
import networkx as nx

class Today(AOC):
        
    def parse_lines(self, file_path=''):
        # self.all_PCs = set()
        self.PCs = defaultdict(list)
        lines = self.lines
        for line in lines:
            pcs = line.split('-')
            
            for i, pc in enumerate(pcs):
                self.PCs[pcs[i]].append(pcs[1-i])
                self.PCs[pcs[i]].append(pcs[i])
# =============================================================================
#         self.all_PCs = sorted(list({pc for line in self.lines for pc in line.split('-')}))
#         self.PCs = {pc:{other_pc:0 for other_pc in self.all_PCs} for pc in self.all_PCs}
#         self.PCs = defaultdict(list)
#             for i, pc in enumerate(pcs):
#                 self.PCs[pcs[i]][pcs[1-i]] = 1
#                 self.PCs[pcs[i]][pcs[i]]  =1
#                 
#         self.PCs['kh'].append('zz') 
#         self.PCs['zz'].append('kh') 
#         self.df = pd.DataFrame(self.PCs)
# =============================================================================
        # self.df.to_excel('output/day_23.xlsx')
        # lines = [[int(lin) for lin in line.split(' ') if set(lin) != set('') ] for line in lines]
        return lines
    
    def part1(self):
        lines = self.parse_lines()
        self.found_networks = set()
        self.checked = set()
        for pc in self.PCs.keys():
            self.trace_connections(pc, size=3, only_t_pcs=True)
        self.result1 = len(self.found_networks)
        self.time1 = timer()
        # for net in self.found_networks:
        #     print(','.join(net))
        return self.result1

    def trace_connections(self, pc, size=3, only_t_pcs=False, break_if_found=False):      
        # pc = 'kh'
        found = 0
        if only_t_pcs:
            if pc[0] != 't':
                return found
        root_connected = self.PCs[pc]
        possible = [combo for combo in combinations(root_connected, size) if len(set(combo)) == size]
        for network in possible:
            if network in self.checked:
                continue
            self.checked.add(network)
            # print(network)
            intersection = set.intersection(*(set(self.PCs[pc]) for pc in network))
            if set(network).issubset(intersection):
                if sum([pc[0]=='t' for pc in network]):
                    self.found_networks.add(tuple(sorted(network)))
                    found += 1
                    if break_if_found:
                        return found
        return found
        # all_in_roots = [r for root in root_connected for r in self.PCs[root]]
        # values = [all_in_roots.count(pc) for pc in set(all_in_roots)]
        
        # counts = root_connected.
        
        
    def part2(self):
        lines = self.parse_lines()
        self.result2 = 0
        graph = nx.Graph()
        connections = [(pc1, pc2) for line in self.lines for pc1, pc2 in [line.split('-')]]
        graph.add_edges_from(connections)
        
        cliques = list(nx.find_cliques(graph))
        network = max(cliques, key=len)
        self.result2 = ','.join(sorted(network))
        
# =============================================================================
#         highest_possibly = max([len(network) for network in self.PCs.values()])
#         likely_culprits = [pc for pc, network in self.PCs.items() if len(network) == highest_possibly]
#         # print('likely culprits are:', likely_culprits)
#         self.highest_network_counts = []
#         for i in range(13, 14):
#         # for i in range(min(13, highest_possibly), 3, -1):
#             self.found_networks = set()
#             today.stop()
#             print(f'running: {i}')
#             self.checked = set()
#             # for pc in self.PCs.keys():
#             for pc in set(likely_culprits):
#                 found = self.trace_connections(pc, size=i, break_if_found=True)
#                 if found > 0:
#                     print(f'found {found} networks with {i} nodes: {self.found_networks}')
#                     self.result2 = ','.join(sorted(list(list(self.found_networks)[0])))
#                     # self.result2 = 'TODO'
#                     self.time2 = timer()
#                     return self.result2
#                     break
#                 self.highest_network_counts.append([i, self.found_networks])
# =============================================================================
            
        # self.result2 = 'TODO'
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
    # not cv,ed,fj,ip,ja,om,qc,qg,qw,ri,ru,tv