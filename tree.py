import numpy as np
from collections import deque

def generate_tree(n):
    edges = []
    nodes = list(range(n))
    np.random.shuffle(nodes)
    
    for i in range(1, n):
        parent = np.random.choice(nodes[:i])
        child = nodes[i]
        edges.append((parent, child))
    
    return edges

def bfs(edges, n):
    adjacency_list = {i: [] for i in range(n)}
    for parent, child in edges:
        adjacency_list[parent].append(child)
        adjacency_list[child].append(parent)
    
    start_node = 0
    queue = deque([start_node])
    visited = [False] * n
    visited[start_node] = True
    bfs_order = []
    
    while queue:
        node = queue.popleft()
        bfs_order.append(node)
        for neighbor in adjacency_list[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)
    
    return bfs_order


edge = generate_tree(6)
print(edge)

print(bfs(edge,6))