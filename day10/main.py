import collections
import time

def get_difference_product(adapters):
    usage_order = sorted(adapters)
    usage_order.append(usage_order[-1]+3)
    
    count = collections.Counter()
    prev = 0
    for x in usage_order:
        diff = x - prev
        count[diff] += 1
        prev = x
    
    return count[1] * count[3]

def get_possibilities(adapters):
    usage_order = sorted(adapters+[0])
    
    possible_paths = [0 for _ in usage_order]
    possible_paths[0] = 1
    for i, possibilities in enumerate(possible_paths):
        for j in range(i+1, i+4):
            if j >= len(usage_order):
                break
            if usage_order[j] > (usage_order[i] + 3):
                break
            possible_paths[j] += possibilities
    
    return possible_paths[-1]

if __name__ == "__main__":
    start = time.time()
    
    with open("input.txt") as f:
        adapters = [int(x.strip()) for x in f.readlines()]
    
    diff_prod = get_difference_product(adapters)
    print(f"part1: 1-diff * 3-diff = {diff_prod}")
    
    num_possibilities = get_possibilities(adapters)
    print(f"part2: total possibilities = {num_possibilities}")
    
    end = time.time()
    print(f"Took {end - start}s")
