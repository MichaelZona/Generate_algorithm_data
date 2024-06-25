import numpy as np
import pandas as pd
import os
import argparse

class FenwickTree:
    def __init__(self, size):
        self.size = size
        self.tree = [0] * (size + 1)

    def update(self, index, delta):
        while index <= self.size:
            self.tree[index] += delta
            index += index & -index

    def query(self, index):
        sum = 0
        while index > 0:
            sum += self.tree[index]
            index -= index & -index
        return sum

    def range_query(self, left, right):
        return self.query(right) - self.query(left - 1)

def generate_operations(n, num_operations):
    operations = []
    for _ in range(num_operations):
        op_type = np.random.choice(["update", "query"])
        if op_type == "update":
            index = np.random.randint(1, n + 1)
            delta = np.random.randint(1, 101)
            operations.append((op_type, index, delta))
        else:
            left = np.random.randint(1, n + 1)
            right = np.random.randint(left, n + 1)
            operations.append((op_type, left, right))
    return operations

def main(args):
    data_size = args.data_size
    array_size = args.array_size
    num_operations = args.num_operations
    file_dir = "./data/tree_numpy/"
    
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    file_name = os.path.join(file_dir, f"tree_numpy_data_{array_size}_{num_operations}.csv")
    print(file_name)
    df = None
    for _ in range(data_size):
        n = array_size
        initial_array = np.random.randint(1, 101, size=n)
        fenwick_tree = FenwickTree(n)
        
        for i in range(n):
            fenwick_tree.update(i + 1, initial_array[i])
        
        operations = generate_operations(n, num_operations)
        results = []
        for op in operations:
            if op[0] == "update":
                _, index, delta = op
                fenwick_tree.update(index, delta)
                results.append(None)
            else:
                _, left, right = op
                result = fenwick_tree.range_query(left, right)
                results.append(result)
        
        instance = {
            "initial_array": " ".join(map(str, initial_array)),
            "operations": " | ".join([f"{op[0]}-{op[1]}-{op[2]}" if op[0] == "update" else f"{op[0]}-{op[1]}-{op[2]}" for op in operations]),
            "results": " ".join([str(res) if res is not None else "None" for res in results])
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
    parser.add_argument("--array_size", type=int, default=10)
    parser.add_argument("--num_operations", type=int, default=15)
    args = parser.parse_args()
    
    main(args)
