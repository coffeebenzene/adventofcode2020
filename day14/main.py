import time
import collections

class MaskInst:
    def __init__(self, mask):
        self.mask = mask
        ones = []
        zeros = []
        xs = []
        for i, m in enumerate(mask):
            if m=="1":
                ones.append(i)
            elif m=="0":
                zeros.append(i)
            elif m=="X":
                xs.append(i)
        self.ones = ones
        self.zeros = zeros
        self.xs = xs
    
    def apply(self, val):
        binary_val = list(format(val,"036b"))
        for idx in self.ones:
            binary_val[idx] = "1"
        for idx in self.zeros:
            binary_val[idx] = "0"
        return int("".join(binary_val), 2)
    
    def apply_float(self, val):
        binary_val = list(format(val,"036b"))
        for idx in self.ones:
            binary_val[idx] = "1"
        
        for idx in self.xs:
            binary_val[idx] = "0"
        for i in range(2**len(self.xs)):
            yield int("".join(binary_val), 2)
            
            carry = 1
            for x_idx in self.xs:
                if not carry:
                    break
                x_val = int(binary_val[x_idx])
                x_val += carry
                carry, x_val = divmod(x_val, 2)
                binary_val[x_idx] = str(x_val)

class MemoryInst:
    def __init__(self, addr, val):
        self.addr = addr
        self.val = val

def process_data(data):
    instructions = []
    for line in data:
        if line.startswith("mask"):
            inst = MaskInst(line[7:])
        elif line.startswith("mem"):
            addr, val = line[4:].split("] = ")
            addr = int(addr)
            val = int(val)
            inst = MemoryInst(addr, val)
        instructions.append(inst)
    return instructions

def compute_memory_sum_part1(instructions):
    memory = {}
    mask = None
    
    for inst in instructions:
        if isinstance(inst, MaskInst):
            mask = inst
        elif isinstance(inst, MemoryInst):
            memory[inst.addr] = mask.apply(inst.val)
    
    return sum(memory.values())

def compute_memory_sum_part2(instructions):
    memory = {}
    mask = None
    
    for inst in instructions:
        if isinstance(inst, MaskInst):
            mask = inst
        elif isinstance(inst, MemoryInst):
            for addr in mask.apply_float(inst.addr):
                memory[addr] = inst.val
    
    return sum(memory.values())


if __name__ == "__main__":
    start = time.time()
    
    with open("input.txt") as f:
        data = [line.strip() for line in f.readlines()]
    instructions = process_data(data)
    
    memory_sum = compute_memory_sum_part1(instructions)
    print(f"Part 1: valid messages: {memory_sum}")
    
    memory_sum = compute_memory_sum_part2(instructions)
    print(f"Part 1: valid messages: {memory_sum}")
    
    end = time.time()
    print(f"Took {end - start}s")
