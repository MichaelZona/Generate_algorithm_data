import numpy as np
import pandas as pd
import os
import argparse

def generate_tree(n):
    edges = []
    nodes = list(range(n))
    np.random.shuffle(nodes)
    
    for i in range(1, n):
        parent = np.random.choice(nodes[:i])
        child = nodes[i]
        edges.append((parent, child))
    
    return edges

def inorder(adjacency_list, node, visited, inorder_order):
    visited[node] = True
    children = adjacency_list[node]
    
    if len(children) == 1:
        if not visited[children[0]]:
            inorder(adjacency_list, children[0], visited, inorder_order)
        inorder_order.append(node)
    elif len(children) > 1:
        if not visited[children[0]]:
            inorder(adjacency_list, children[0], visited, inorder_order)
        inorder_order.append(node)
        if not visited[children[1]]:
            inorder(adjacency_list, children[1], visited, inorder_order)
    else:
        inorder_order.append(node)

def main(args):
    data_size = args.data_size
    nodes = args.nodes
    file_dir = "./data/inorder/"
    
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    file_name = os.path.join(file_dir, f"dfs_inorder_data_{nodes}.csv")
    
    df = None
    for _ in range(data_size):
        n = nodes
        edges = generate_tree(n)
        
        adjacency_list = {i: [] for i in range(n)}
        for parent, child in edges:
            adjacency_list[parent].append(child)
            adjacency_list[child].append(parent)
        
        visited = [False] * n
        inorder_order = []
        inorder(adjacency_list, 0, visited, inorder_order)
        
        instance = {
            "nodes": n,
            "edges": " ".join([f"{parent}-{child}" for parent, child in edges]),
            "inorder_order": " ".join(map(str, inorder_order))
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
    parser.add_argument("--nodes", type=int, default=20)
    args = parser.parse_args()
    
    main(args)
