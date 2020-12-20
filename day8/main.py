import time

def preprocess_assembly(assembly):
    instructions = []
    for line in assembly:
        opcode, offset = line.strip().split()
        offset = int(offset)
        instructions.append((opcode, offset))
    return instructions

def check_termination(assembly):
    instruction_pointer = 0
    accumulator = 0
    seen_instructions = set()
    
    while True:
        if instruction_pointer == len(assembly):
            return instruction_pointer, accumulator, "Normal"
        elif instruction_pointer < 0 or len(assembly) < instruction_pointer:
            return instruction_pointer, accumulator, "OutOfBounds"
        elif instruction_pointer in seen_instructions:
            return instruction_pointer, accumulator, "InfiniteLoop"
        else:
            seen_instructions.add(instruction_pointer)
        
        opcode, offset = assembly[instruction_pointer]
        if opcode == "acc":
            accumulator += offset
        elif opcode == "jmp":
            instruction_pointer += offset-1
        
        instruction_pointer += 1
    
    return instruction_pointer, accumulator, "Error"

def find_corrupt_instruction(assembly):
    switch_opcode = {"nop":"jmp", "jmp":"nop"}
    
    for index, instruction in enumerate(assembly):
        if instruction[0] == "acc":
            continue
        
        trial_assembly = assembly.copy()
        new_opcode = switch_opcode[instruction[0]]
        trial_assembly[index] = (new_opcode, instruction[1])
        
        instruction_pointer, accumulator, termination_type = check_termination(trial_assembly)
        if termination_type == "Normal":
            return instruction_pointer, accumulator, index
    
    return 0, 0, -1

if __name__ == "__main__":
    start = time.time()
    
    with open("input.txt") as f:
        assembly = f.readlines()
    
    assembly = preprocess_assembly(assembly)
    
    instruction_pointer, accumulator, termination_type = check_termination(assembly)
    print(f"part1: accumulator at loop: {accumulator} ({termination_type} at {instruction_pointer})")
    
    instruction_pointer, accumulator, corrupt_index = find_corrupt_instruction(assembly)
    print(f"part2: accumulator at fixed: {accumulator} (Fixed {corrupt_index}. Terminated at {instruction_pointer})")
    
    end = time.time()
    print(f"Took {end - start}s")
