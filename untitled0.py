import concurrent.futures as cf
from time import time
from traceback import print_exc
from itertools import chain

def _findmatch(nmin, nmax, number):
    '''Function to find the occurrence of number in range nmin to nmax and return
       the found occurrences in a list.'''
    print('\n def _findmatch', nmin, nmax, number)
    start = time()
    match=[]
    for n in range(nmin, nmax):
        if number in str(n):
            match.append(n)
    end = time() - start
    print("found {0} in {1:.4f}sec".format(len(match),end))
    return match

def _concurrent_map(nmax, number, workers):
    '''Function that utilises concurrent.futures.ProcessPoolExecutor.map to
       find the occurrences of a given number in a number range in a parallelised
       manner.'''
    # 1. Local variables
    chunk = nmax // workers
    futures = []
    found =[]
    #2. Parallelization
    with cf.ThreadPoolExecutor(max_workers=workers) as executor:
        # 2.1. Discretise workload and submit to worker pool
        for i in range(workers):
            cstart = chunk * i
            cstop = chunk * (i + 1) if i != workers - 1 else nmax
            futures.append(executor.submit(_findmatch, cstart, cstop, number))

    return chain.from_iterable(f.result() for f in cf.as_completed(futures))

if __name__ == '__main__':
    nmax = int(1E8) # Number range maximum.
    number = str(5) # Number to be found in number range.
    workers = 25     # Pool of workers

    start = time()
    a = _concurrent_map(nmax, number, workers)
    end = time() - start
    print('\n main')
    print('workers = ', workers)
    print("found {0} in {1:.4f}sec".format(sum(1 for x in a),end))