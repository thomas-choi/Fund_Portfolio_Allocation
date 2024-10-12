import pandas as pd
import multiprocessing as mp
import math

def worker(args):
    print(f'work: ==>{args}<==\n')
    data_chunk, process_data = args
    # print('worker:', data_chunk, ' , ', process_data)
    return process_data(data_chunk)

def split_dataframe(data, num_chunks):
    chunk_size = math.ceil(len(data) / num_chunks)
    print(f'split_data: chunk_size:{chunk_size}')
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

def run_pool(data, process_data, num_cpus=None):
    if num_cpus is None:
        num_cpus = mp.cpu_count() - 2  # Use all CPUs except one to avoid overloading
    else:
        num_cpus = min(num_cpus, mp.cpu_count() - 2)  # Ensure we don't exceed available CPUs
    print(f'num_cpus is {num_cpus}')

    data_chunks = split_dataframe(data, num_cpus)
    print('data_chunks:\n', data_chunks)
    # print([(chunk, process_data) for chunk in data_chunks])
    
    with mp.Pool(processes=num_cpus) as pool:
        results = pool.map(worker, [(chunk, process_data) for chunk in data_chunks])
    return results

if __name__ == "__main__":

    import pandas as pd

    def custom_process_data(data):
        # Example processing function
        df = pd.DataFrame(data)
        result = df.describe().to_dict()
        return result

    from data_processing import run_pool
    import pandas as pd
    
    data = [
            {'A': 1, 'B': 4}, {'A': 2, 'B': 5}, {'A': 3, 'B': 6},
            {'A': 7, 'B': 10}, {'A': 8, 'B': 11}, {'A': 9, 'B': 12},
            {'A': 13, 'B': 16}, {'A': 14, 'B': 17}, {'A': 15, 'B': 18},
            {'A': 12, 'B': 4}, {'A': 22, 'B': 5}, {'A': 23, 'B': 6},
            {'A': 27, 'B': 10}, {'A': 28, 'B': 11}, {'A': 29, 'B': 12},
            {'A': 213, 'B': 16}, {'A': 214, 'B': 17}, {'A': 215, 'B': 18},
            {'A': 31, 'B': 4}, {'A': 32, 'B': 5}, {'A': 33, 'B': 6},
            {'A': 37, 'B': 10}, {'A': 38, 'B': 11}, {'A':39, 'B': 12},
            {'A': 313, 'B': 16}, {'A': 314, 'B': 17}, {'A': 315, 'B': 18},
            {'A': 41, 'B': 4}, {'A': 42, 'B': 5}, {'A': 43, 'B': 6},
            {'A': 47, 'B': 10}, {'A': 48, 'B': 11}, {'A': 49, 'B': 12},
            {'A': 413, 'B': 16}, {'A': 414, 'B': 17}, {'A': 415, 'B': 18},
            {'A': 51, 'B': 4}, {'A': 52, 'B': 5}, {'A': 53, 'B': 6},
            {'A': 57, 'B': 10}, {'A': 58, 'B': 11}, {'A': 59, 'B': 12},
            {'A': 513, 'B': 16}, {'A': 514, 'B': 17}, {'A': 515, 'B': 18},
            {'A': 61, 'B': 4}, {'A': 62, 'B': 5}, {'A': 63, 'B': 6},
            {'A': 67, 'B': 10}, {'A': 68, 'B': 11}, {'A': 69, 'B': 12},
            {'A': 713, 'B': 16}, {'A': 714, 'B': 17}, {'A':715, 'B': 18},
        ]
        
    # Run with a specified number of CPUs
    results = run_pool(data, custom_process_data)
    for result in results:
        print(result)
