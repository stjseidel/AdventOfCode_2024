# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 22:48:57 2024

@author: stjse
"""

import heapq

class MazeSolver:        
    def __init__(self):
        pass
    
    def plot_graph(self, lines):
        self.steps = [(row, col) for row, line in enumerate(lines) for col, char in enumerate(line) if char in ['.', 'E', 'S']]
        self.walls = [(row, col) for row, line in enumerate(lines) for col, char in enumerate(line) if char == '#']
        self.origin = [(row, col) for row, line in enumerate(lines) for col, char in enumerate(line) if char == 'S'][0]
        self.target = [(row, col) for row, line in enumerate(lines) for col, char in enumerate(line) if char == 'E'][0]
        # breakpoint()
        # self.Matrix = {(row, col):set([(row+1, col), (row, col+1), (row-1, col), (row, col-1)]) & set(self.steps) for (row, col) in self.steps}
        self.Neighbors = {(row, col):set([(r, c) for (r,c) in [(row+1, col), (row, col+1), (row-1, col), (row, col-1)] if lines[r][c] in ['.', 'E', 'S']]) for (row, col) in self.steps}

        self.graph = {node:{(neigh, (neigh[0]-node[0], neigh[1]-node[1])) for neigh in neighbors} for node, neighbors in self.Neighbors.items()}
        return self.graph
    
    def calculate_weight(self, prev_dir, new_dir):
        # If direction changes, return 1001, else return 1
        return 1 if prev_dir == new_dir else 1001
    
    def dijkstra_with_directions_penalty(self, graph, start, end, direction=None, direction_penalty=0):
        # Priority queue: (cost, current_node, direction)
        pq = [(0, start, direction)]
        visited = set()
    
        # Distance dictionary: (node, direction) -> cost
        dist = {}
        while pq:
            cost, current, direction = heapq.heappop(pq)
            if (current, direction) in visited:
                continue
            visited.add((current, direction))
            if current == end:
                return cost
            for neighbor, neighbor_dir in graph[current]:
                # Calculate the weight based on direction
                if direction_penalty > 0:
                    weight = self.calculate_weight(direction, neighbor_dir) if direction else 1
                else:
                    weight = 1
                new_cost = cost + weight
                # Add to the priority queue if not visited or if found a cheaper path
                if (neighbor, neighbor_dir) not in dist or new_cost < dist[(neighbor, neighbor_dir)]:
                    dist[(neighbor, neighbor_dir)] = new_cost
                    heapq.heappush(pq, (new_cost, neighbor, neighbor_dir))
        # If no path found
        return float('inf')
    
    def dijkstra_with_directions_penalty_all_paths(self, graph, start, end, direction=None):
        # Priority queue: (cost, current_node, direction, path)
        pq = [(0, start, direction, [start])]
        visited = {}  # Track visited nodes with their minimum cost
        # Paths dictionary: (node, direction) -> list of all shortest paths
        paths = {}
        while pq:
            cost, current, direction, path = heapq.heappop(pq)
            # If already visited with a lower cost, skip
            if (current, direction) in visited and cost > visited[(current, direction)]:
                continue
    
            visited[(current, direction)] = cost
    
            # Add the path to the paths dictionary
            if (current, direction) not in paths:
                paths[(current, direction)] = []
            paths[(current, direction)].append(path)
            # If the target is reached, continue to collect other paths
            if current == end:
                continue
            for neighbor, neighbor_dir in graph[current]:
                # Calculate the weight based on direction
                weight = self.calculate_weight(direction, neighbor_dir) if direction else 1
                new_cost = cost + weight
    
                # Add to the priority queue if not visited with a lower cost
                if (neighbor, neighbor_dir) not in visited or new_cost <= visited[(neighbor, neighbor_dir)]:
                    new_path = path + [neighbor]
                    heapq.heappush(pq, (new_cost, neighbor, neighbor_dir, new_path))
    
        # Collect all paths to the end node with the shortest cost
        shortest_paths = []
        min_cost = float('inf')
    
        for (node, direction), node_paths in paths.items():
            if node == end:
                for p in node_paths:
                    if visited[(node, direction)] < min_cost:
                        shortest_paths = [p]
                        min_cost = visited[(node, direction)]
                    elif visited[(node, direction)] == min_cost:
                        shortest_paths.extend(node_paths)
    
        return min_cost, shortest_paths
        
