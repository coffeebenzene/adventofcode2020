import collections
import time

Estimate = collections.namedtuple("Estimate", ["start","end","sum"])

def val_vaild_given_preamble(val, preamble):
    for possible_part in preamble:
        if val - possible_part in preamble:
            return True
    return False

def find_invalid(data):
    PREAMBLE_SIZE = 25
    preamble = set(data[0:PREAMBLE_SIZE])
    current_index = PREAMBLE_SIZE
    
    for i, val in enumerate(data[PREAMBLE_SIZE:], PREAMBLE_SIZE):
        if not val_vaild_given_preamble(val, preamble):
            return i, val
        preamble.remove(data[i-PREAMBLE_SIZE])
        preamble.add(val)
    return None, None

def advance_start(data, estimate):
    new_sum = estimate.sum - data[estimate.start]
    return Estimate(estimate.start+1, estimate.end, new_sum)

def advance_end(data, estimate):
    new_sum = estimate.sum + data[estimate.end]
    return Estimate(estimate.start, estimate.end+1, new_sum)

def decrement_end(data, estimate):
    new_sum = estimate.sum - data[estimate.end-1]
    return Estimate(estimate.start, estimate.end-1, new_sum)

def find_closest_sum_with_start(data, sum_to_find, estimate):
    if estimate.sum > sum_to_find:
        while estimate.sum > sum_to_find:
            estimate = decrement_end(data, estimate)
            break
    else:
        while estimate.sum < sum_to_find:
            estimate = advance_end(data, estimate)
    return estimate

def find_contiguous_sum(data, sum_to_find):
    estimate = Estimate(0, 2, sum(data[0:2]))
    for i in range(len(data)):
        estimate = find_closest_sum_with_start(data, sum_to_find, estimate)
        if estimate.sum == sum_to_find:
            break
        estimate = advance_start(data, estimate)
    return estimate

def add_smallest_and_largest(data, estimate):
    region = data[estimate.start: estimate.end]
    return min(region) + max(region)

if __name__ == "__main__":
    start = time.time()
    
    with open("input.txt") as f:
        data = [int(x) for x in f.readlines()]
    
    index, invalid_num = find_invalid(data)
    print(f"part1: invalid_num = {invalid_num} (at {index})")
    
    estimate = find_contiguous_sum(data, invalid_num)
    weakness = add_smallest_and_largest(data, estimate)
    print(f"part2: weakness = {weakness} (estimate = {estimate})")
    
    end = time.time()
    print(f"Took {end - start}s")
