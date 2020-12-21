import collections
import time

Instruction = collections.namedtuple("Instruction", ["action", "val"])
Position = collections.namedtuple("Position", ["north", "east", "facing"])

def preprocess_instructions(data):
    instructions = []
    for line in data:
        line = line.strip()
        inst = Instruction(line[0], int(line[1:]))
        instructions.append(inst)
    return instructions

def next_position_part1(pos, inst):
    if inst.action == "F":
        inst = Instruction(pos.facing, inst.val)
    
    if inst.action == "N":
        return Position(pos.north+inst.val, pos.east, pos.facing)
    elif inst.action == "S":
        return Position(pos.north-inst.val, pos.east, pos.facing)
    elif inst.action == "E":
        return Position(pos.north, pos.east+inst.val, pos.facing)
    elif inst.action == "W":
        return Position(pos.north, pos.east-inst.val, pos.facing)
    
    if inst.action == "L":
        rotations = "NWSE"*2
    elif inst.action == "R":
        rotations = "NESW"*2
    turns = (inst.val//90) % 4
    rot_index = rotations.index(pos.facing)
    new_facing = rotations[rot_index+turns]
    return Position(pos.north, pos.east, new_facing)

def next_position_part2(pos, inst):
    # facing is the waypoint
    if inst.action == "F":
        new_north = pos.north + pos.facing.north * inst.val
        new_east = pos.east + pos.facing.east * inst.val
        return Position(new_north, new_east, pos.facing)
    
    if inst.action in "NSEW":
        if inst.action == "N":
            new_waypoint = Position(pos.facing.north+inst.val, pos.facing.east, None)
        elif inst.action == "S":
            new_waypoint = Position(pos.facing.north-inst.val, pos.facing.east, None)
        elif inst.action == "E":
            new_waypoint = Position(pos.facing.north, pos.facing.east+inst.val, None)
        elif inst.action == "W":
            new_waypoint = Position(pos.facing.north, pos.facing.east-inst.val, None)
        return Position(pos.north, pos.east, new_waypoint)
    
    turns = (inst.val//90) % 4
    if inst.action == "L":
        turns = (4 - turns) % 4
    elif inst.action == "R":
        pass
    
    rotated_facing = pos.facing
    for i in range(turns):
        new_east = rotated_facing.north
        new_north = -rotated_facing.east
        rotated_facing = Position(new_north, new_east, None)
    
    return Position(pos.north, pos.east, rotated_facing)

def execute_instructions(pos, instructions, next_position_func):
    for inst in instructions:
        pos = next_position_func(pos, inst)
        #print(f"{inst} => {pos}")
    return pos

if __name__ == "__main__":
    start = time.time()
    
    with open("input.txt") as f:
        data = f.readlines()
    instructions = preprocess_instructions(data)
    
    final_pos = execute_instructions(Position(0,0,"E"), 
                                     instructions,
                                     next_position_part1)
    manhattan_dist = abs(final_pos[0])+abs(final_pos[1])
    print(f"part1: manhattan dist = {manhattan_dist}")
    
    final_pos = execute_instructions(Position(0,0,Position(1,10,None)),
                                     instructions,
                                     next_position_part2)
    manhattan_dist = abs(final_pos[0])+abs(final_pos[1])
    print(f"part2: manhattan dist = {manhattan_dist}")
    
    end = time.time()
    print(f"Took {end - start}s")
