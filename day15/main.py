import time

def generate_numbers(initial):
    for x in initial:
        yield x
    
    last_positions = {}
    for prev_i,x in enumerate(initial[:-1]):
        last_positions[x] = prev_i
    
    prev_num = initial[-1]
    while True:
        prev_i += 1
        if prev_num in last_positions:
            this_num = prev_i - last_positions[prev_num]
        else:
            this_num = 0
        
        yield this_num
        last_positions[prev_num] = prev_i
        prev_num = this_num

def get_num(initial, position):
    game = generate_numbers(initial)
    for i in range(position):
        num = next(game)
    return num

if __name__ == "__main__":
    start = time.time()
    
    data = [7,12,1,0,16,2]
    
    num = get_num(data, 2020)
    print(f"part1: 2020th number = {num}")
    
    num = get_num(data, 30000000)
    print(f"part1: 30000000th number = {num}")
    
    end = time.time()
    print(f"Took {end - start}s")
