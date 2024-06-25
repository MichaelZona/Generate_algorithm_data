import numpy as np
import pandas as pd
import os
import argparse

class SparseTable:
    def __init__(self, array):
        self.n = len(array)
        self.log = [0] * (self.n + 1)
        self.build_log()
        self.st = self.build_sparse_table(array)

    def build_log(self):
        for i in range(2, self.n + 1):
            self.log[i] = self.log[i // 2] + 1

    def build_sparse_table(self, array):
        K = self.log[self.n] + 1
        st = [[0] * K for _ in range(self.n)]
        for i in range(self.n):
            st[i][0] = array[i]
        j = 1
        while (1 << j) <= self.n:
            i = 0
            while (i + (1 << j) - 1) < self.n:
                st[i][j] = min(st[i][j - 1], st[i + (1 << (j - 1))][j - 1])
                i += 1
            j += 1
        return st

    def query(self, L, R):
        j = self.log[R - L + 1]
        return min(self.st[L][j], self.st[R - (1 << j) + 1][j])

def generate_queries(n, num_queries):
    queries = []
    for _ in range(num_queries):
        L = np.random.randint(0, n)
        R = np.random.randint(L, n)
        queries.append((L, R))
    return queries

def main(args):
    data_size = args.data_size
    array_size = args.array_size
    num_queries = args.num_queries
    file_dir = "./data/sparse_table/"
    
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    file_name = os.path.join(file_dir, f"sparse_table_data_{array_size}_{num_queries}.csv")
    print(file_name)
    df = None
    for _ in range(data_size):
        n = array_size
        array = np.random.randint(1, 101, size=n)
        st = SparseTable(array)
        
        queries = generate_queries(n, num_queries)
        results = []
        for L, R in queries:
            result = st.query(L, R)
            results.append(result)
        
        instance = {
            "array": " ".join(map(str, array)),
            "queries": " | ".join([f"{L}-{R}" for L, R in queries]),
            "results": " ".join(map(str, results))
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
    parser.add_argument("--num_queries", type=int, default=15)
    args = parser.parse_args()
    
    main(args)
