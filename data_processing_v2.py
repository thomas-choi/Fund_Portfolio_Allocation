import pandas as pd
import multiprocessing as mp
import math

dbug_flag = True

def set_debug(flag):
    dbug_flag = flag
    print(f"MP> set new dbug flag: {dbug_flag}")

def worker(task_queue, result_queue, process_data):
    cnt = 0
    created = mp.Process()
    current = mp.current_process()
    if dbug_flag:
        print(f'MP> running: {current.name}, {current._identity}\n created: {created.name}, {created._identity}\n')

    while True:
        data_pack = task_queue.get()
        cnt = data_pack["cnt"]
        data_chunk = data_pack["data"]
        if data_chunk is None:  # Sentinel to signal the end of tasks
            if dbug_flag:
                print(f'MP> worker: {current.name} existed. {cnt} data processed\n')
            break
        result = process_data(cnt, data_chunk)
        result_queue.put({"cnt": cnt, "result": result})
        if dbug_flag:
            print(f'MP> worker: {current.name} processed {cnt} data\n')

def split_dataframe(data, num_chunks):
    chunk_size = math.ceil(len(data) / num_chunks)
    if dbug_flag:
        print(f'MP> split_data: chunk_size:{chunk_size} from data.length={len(data)}')
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    # return [df.iloc[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

def run_pool_v2(data, process_data, num_cpus=None):
    if num_cpus is None:
        num_cpus = mp.cpu_count() - 1  # Use all CPUs except one to avoid overloading
    else:
        num_cpus = min(num_cpus, mp.cpu_count() - 1)  # Ensure we don't exceed available CPUs
    if dbug_flag:
        print(f'MP> num_cpus is {num_cpus}')
    
    data_chunks = split_dataframe(data, len(data))  # Split data into individual tasks
    task_queue = mp.Queue()
    result_queue = mp.Queue()

    # Start worker processes
    processes = []
    for _ in range(num_cpus):
        p = mp.Process(target=worker, args=(task_queue, result_queue, process_data))
        p.start()
        processes.append(p)

    # Distribute tasks
    dsent=0
    for chunk in data_chunks:
        dsent +=1
        task_queue.put({"cnt": dsent, "data": chunk})
    if dbug_flag:
        print(f"MP> {dsent} data sent")

    # Add a sentinel (None) to signal the end of tasks
    for _ in range(num_cpus):
        task_queue.put({"cnt": dsent, "data": None})

    # Collect results
    results = []
    for _ in data_chunks:
        res_package = result_queue.get()
        drecv = res_package["cnt"]
        if dbug_flag:
            print(f"MP> received data {drecv}")
        results.append(res_package["result"])      
    if dbug_flag:
        print(f"MP> total {len(results)} results received")

    # Ensure all worker processes have finished
    for p in processes:
        p.join()

    return results

