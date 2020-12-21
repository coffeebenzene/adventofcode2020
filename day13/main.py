import time

def part1(data):
    time_available = int(data[0])
    buses = [int(b) for b in data[1].split(",") if b!="x"]
    bus_available_after = {}
    for b in buses:
        bus_left_time_ago = time_available % b
        next_bus_time = b - bus_left_time_ago
        bus_available_after[b] = next_bus_time
    
    min_bus, wait_time = min(bus_available_after.items(), key=lambda bt:bt[1])
    return min_bus * wait_time

class LoopedCheckpoints:
    def __init__(self, loop_size, checkpoints):
        self.loop_size = loop_size
        self.checkpoints = sorted(checkpoints)
        self.checkpoints_set = set(checkpoints)
    
    def order_by_loop_size(self, other_loop):
        if self.loop_size <= other_loop.loop_size:
            return self, other_loop
        else:
            return other_loop, self
    
    def generate_checkpoints(self, times):
        for i in range(times):
            loop_start = i*self.loop_size
            for c in self.checkpoints:
                yield loop_start + c
    
    def is_a_checkpoint(self, value):
        loop_offset = value % self.loop_size
        return loop_offset in self.checkpoints_set
    
    def intersect_loop(self, other_loop):
        new_loop_size = self.loop_size * other_loop.loop_size
        smaller_loop, larger_loop = self.order_by_loop_size(other_loop)
        
        new_loop_checkpoints = []
        trial_checkpoints = larger_loop.generate_checkpoints(smaller_loop.loop_size)
        for c in trial_checkpoints:
            if smaller_loop.is_a_checkpoint(c):
                new_loop_checkpoints.append(c)
        
        return LoopedCheckpoints(new_loop_size, new_loop_checkpoints)
    
    def __repr__(self):
        return f"LoopedCheckpoints({self.loop_size}, {self.checkpoints})"

def preprocess_part2(data):
    bus_offsets = [(int(b),i) for i,b in enumerate(data[1].split(",")) if (b != "x")]
    bus_checkpoints = []
    for b, offset in bus_offsets:
        offset = offset % b
        checkpoint = (b - offset) % b
        bus_checkpoints.append(LoopedCheckpoints(b, [checkpoint]))
    return bus_checkpoints

def earliest_sequence_departure_time(bus_checkpoints):
    checkpoint = bus_checkpoints.pop()
    for next_checkpoint in bus_checkpoints:
        checkpoint = checkpoint.intersect_loop(next_checkpoint)
    return checkpoint.checkpoints[0]

if __name__ == "__main__":
    start = time.time()
    
    with open("input.txt") as f:
        data = [x.strip() for x in f.readlines()]
    
    part1_value = part1(data)
    print(f"part1: {part1_value}")
    
    bus_checkpoints = preprocess_part2(data)
    departure_time = earliest_sequence_departure_time(bus_checkpoints)
    print(f"departure time: {departure_time}")
    
    end = time.time()
    print(f"Took {end - start}s")
