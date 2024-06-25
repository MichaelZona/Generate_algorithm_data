import numpy as np
import pandas as pd
import os
import argparse

class Tarjan:
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n)]
        self.ids = [-1] * n
        self.low = [-1] * n
        self.visited = [False] * n
        self.is_articulation = [False] * n
        self.id = 0
        self.out_edge_count = 0

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def dfs(self, u, parent, out_edge_count):
        self.visited[u] = True
        self.ids[u] = self.low[u] = self.id
        self.id += 1

        for v in self.graph[u]:
            if v == parent:
                continue
            if not self.visited[v]:
                self.dfs(v, u, out_edge_count + 1)
                self.low[u] = min(self.low[u], self.low[v])
                
                if parent == -1:
                    out_edge_count += 1
                    if out_edge_count > 1:
                        self.is_articulation[u] = True
                else:
                    if self.low[v] >= self.ids[u]:
                        self.is_articulation[u] = True
            else:
                self.low[u] = min(self.low[u], self.ids[v])

    def find_articulation_points(self):
        for i in range(self.n):
            if not self.visited[i]:
                self.out_edge_count = 0
                self.dfs(i, -1, self.out_edge_count)
        return [i for i, is_articulation in enumerate(self.is_articulation) if is_articulation]

def generate_graph(n, m):
    edges = set()
    while len(edges) < m:
        u, v = np.random.choice(n, 2, replace=False)
        edges.add((min(u, v), max(u, v)))
    return list(edges)

def main(args):
    data_size = args.data_size
    nodes = args.nodes
    edges_count = args.edges
    file_dir = "./data/tarjan/"
    
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    file_name = os.path.join(file_dir, f"tarjan_data_{nodes}_{edges_count}.csv")
    print(file_name)
    df = None
    for _ in range(data_size):
        n = nodes
        m = edges_count
        edges = generate_graph(n, m)
        
        tarjan = Tarjan(n)
        for u, v in edges:
            tarjan.add_edge(u, v)
        
        articulation_points = tarjan.find_articulation_points()
        
        instance = {
            "nodes": n,
            "edges": " ".join([f"{u}-{v}" for u, v in edges]),
            "articulation_points": " ".join(map(str, articulation_points))
        }
        
        for key, val in instance.items():
            instance[key] = [val, ]
        
        tmp_df = pd.DataFrame(instance)
        df = pd.concat([df, tmp_df], ignore_index=True) if df is not None else tmp_df

        if len(df) >= 1000:
            if not os.path.exists(file_name):
                df.to_csv(file_name, index=False)
            else:
                result_df = pd.read_csv(file_name)
                result_df = pd.concat([result_df, df], ignore_index=True)
                result_df.to_csv(file_name, index=False)
                if result_df.shape[0] >= data_size:
                    exit()
            df = None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_size", type=int, default=1000)
    parser.add_argument("--nodes", type=int, default=10)
    parser.add_argument("--edges", type=int, default=15)
    args = parser.parse_args()
    
    main(args)
