import collections
import time

def get_2020_pair(nums):
    nums = collections.Counter(nums)
    for x in nums:
        other_required = 2020 - x
        if other_required in nums:
            if x == other_required and nums[x] < 2:
                continue
            return (x, other_required)

def get_2020_triplet(nums):
    nums = collections.Counter(nums)
    for x1 in nums:
        for x2 in nums:
            other_required = 2020 - x1 - x2
            if other_required not in nums:
                continue
            triplet = (x1, x2, other_required)
            triplet_multiset = collections.Counter(triplet)
            if (triplet_multiset & nums) != triplet_multiset:
                continue
            return (x1, x2, other_required)

if __name__ == "__main__":
    start = time.time()
    
    with open("input.txt") as f:
        expense = [int(line.strip()) for line in f.readlines()]
    x,y = get_2020_pair(expense)
    print(f"part1: {x} * {y} = {x*y}")
    x,y,z = get_2020_triplet(expense)
    print(f"part2: {x} * {y} * {z} = {x*y*z}")
    
    end = time.time()
    print(f"Took {end - start}s")
