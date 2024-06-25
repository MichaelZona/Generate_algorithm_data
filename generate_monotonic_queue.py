import numpy as np
import pandas as pd
import os
import argparse
from collections import deque

def sliding_window_maximum(nums, k):
    deq = deque()
    result = []
    for i in range(len(nums)):
        if deq and deq[0] == i - k:
            deq.popleft()
        while deq and nums[deq[-1]] < nums[i]:
            deq.pop()
        deq.append(i)
        if i >= k - 1:
            result.append(nums[deq[0]])
    return result

def generate_array_and_windows(array_size, window_size, num_operations):
    arrays = []
    windows = []
    for _ in range(num_operations):
        array = np.random.randint(1, 101, size=array_size)
        arrays.append(array)
        windows.append(window_size)
    return arrays, windows

def main(args):
    data_size = args.data_size
    array_size = args.array_size
    window_size = args.window_size
    file_dir = "./data/monotonic_queue/"
    
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    file_name = os.path.join(file_dir, f"monotonic_queue_data_{array_size}_{window_size}.csv")
    print(file_name)
    df = None
    for _ in range(data_size):
        arrays, windows = generate_array_and_windows(array_size, window_size, 1)
        array = arrays[0]
        window = windows[0]
        
        max_values = sliding_window_maximum(array, window)
        
        instance = {
            "array": " ".join(map(str, array)),
            "window_size": window,
            "max_values": " ".join(map(str, max_values))
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
    parser.add_argument("--window_size", type=int, default=3)
    args = parser.parse_args()
    
    main(args)
