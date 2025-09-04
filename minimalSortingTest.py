import time
from typing import Callable, Iterable, Sequence
import random
from statistics import median
import csv
from itertools import pairwise, repeat

#All sorting functions return a sorted array, and avoid side effects
def selection_sort(arr: Sequence[int]) -> Sequence[int]:
    """
    Sort using selection sort
    """
    def find_min(arr: Sequence[int]) -> tuple[int, int]:
        """
        finds minimum in array
        returns index, item
        """
        minItem: int = arr[0]
        minIndex = 0
        for i, item in enumerate(arr):
            if item < minItem:
                minItem = item
                minIndex = i
        return minIndex, minItem
                
    out = list(arr)
    for i in range(len(out)):
        minIndex, minItem = find_min(out[i:])
        out[i+minIndex] = out[i]
        out[i] = minItem
    return out
            
def fun_merge_sort(arr: Sequence[int]) -> Sequence[int]:
    """
    Sort using merge sort
    Uses iters and branchless techniques
    """
    def merge(left: Sequence[int], right: Sequence[int]) -> Sequence[int]:
        """
        Merge 2 sequences
        """
        iters = (iter(left), iter(right))
        heads = [next(iters[0]), next(iters[1])]
        out = []
        while True:
            smallerIndex = heads[1] < heads[0] #bool is the index of which value is smaller
            out.append(heads[smallerIndex])
            try:
                heads[smallerIndex] = next(iters[smallerIndex])
            except StopIteration:
                out.append(heads[not smallerIndex])
                out.extend(iters[not smallerIndex])
                return out
    if len(arr) == 1:
        return arr
    
    mid = len(arr)//2
    left, right = arr[:mid], arr[mid:]
    return merge(fun_merge_sort(left), fun_merge_sort(right))

def basic_merge_sort(arr: Sequence[int]) -> Sequence[int]:
    """
    Sort using merge sort
    """
    def merge(left: Sequence[int], right: Sequence[int]) -> Sequence[int]:
        """
        Merge 2 sequences
        """
        L = R = 0
        out = []

        while L < len(left) and R < len(right):
            if left[L] < right[R]:
                out.append(left[L])
                L += 1
            else:
                out.append(right[R])
                R += 1

        out.extend(left[L:])
        out.extend(right[R:])
        
        return out
    
    if len(arr) == 1:
        return arr
    
    mid = len(arr)//2
    left, right = arr[:mid], arr[mid:]
    return merge(basic_merge_sort(left), basic_merge_sort(right))

def bubble_sort(arr: Sequence[int]) -> Sequence[int]:
    """
    Sort using bubble sort
    """
    out = list(arr)
    did_swap = True
    while did_swap:
        did_swap = False
        for (i1, item1), (i2, item2) in pairwise(enumerate(out)):
            if item2 < item1:
                out[i1], out[i2] = out[i2], out[i1]
                did_swap = True
    return out

def time_algorithm(
        algo: Callable[[Sequence[int]], Sequence[int]], 
        arr: Sequence[int]) -> float:
    """
    Time a sorting algorithm with a given input array.
    """
    start = time.perf_counter()
    algo(arr)
    return time.perf_counter() - start

def gen_starting_arr(len: int, seed = None) -> Sequence[int]:
    """
    Generate a randomly shuffled list.
    """
    out = list(range(len))
    random.seed(seed)
    random.shuffle(out)
    return out

def gen_starting_arrs(len: int, seed = None) -> Iterable[Sequence[int]]:
    """
    Returns an iterator that generates infinite randomly shuffled lists.
    """
    random.seed(seed)
    out = list(range(len))
    while True:
        random.shuffle(out)
        yield out

def algorithm_trials(
        algo: Callable[[Sequence[int]], Sequence[int]], 
        arrs: Iterable[Sequence[int]], 
        trials: int) -> Sequence[float]:
    """
    Runs multiple time_algorithm trials
    """
    time_algorithm(algo, next(iter(arrs))) #warm up the function for consistency
    results = []
    for _, arr in zip(range(trials), arrs):
        results.append(time_algorithm(algo, arr))
    return results

def main():
    #{name: alg} change these to test different sorting functions
    tested_algs: dict[str, Callable[[Sequence[int]], Sequence[int]]] = {
        "built-int": sorted, 
        "merge": fun_merge_sort, 
        "selection": selection_sort, 
        "bubble": bubble_sort}
    sizes = 100, 500, 1_000, 5_000, 10_000, 20_000 #array sizes to test
    trials = 5 #number of trials to perform
    seed = 42 #starting seed

    results = {}
    for name, alg in tested_algs.items():
        #un-comment exactly one of these to test different array input generation methods
        results[name] = list(map(lambda a: median(algorithm_trials(alg, gen_starting_arrs(a, seed), trials)), sizes)) #random input
        #results[name] = list(map(lambda a: median(algorithm_trials(alg, repeat(list(range(a))), trials)), sizes)) #pre-sorted input
        #results[name] = list(map(lambda a: median(algorithm_trials(alg, repeat(list(range(a-1, -1, -1))), trials)), sizes)) #anti-sorted input

    #write the results to a csv file
    with open('SortComparisonResults.csv', 'w', newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["algorithm_name"] + list(sizes))
        for name, result in results.items():
            writer.writerow([name] + list(result))

if __name__ == '__main__':
    main()