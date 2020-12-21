import time

translation = str.maketrans({"F":"0", "B":"1", "L":"0", "R":"1"})

def seat_id(line):
    binary_line = line.translate(translation)
    return int(binary_line,2)

if __name__ == "__main__":
    start = time.time()
    
    with open("input.txt") as f:
        seats = f.readlines()
    
    all_seats = {seat_id(s) for s in seats}
    
    max_seat = max(all_seats)
    print(f"part1: max_seat: {max_seat}")
    
    min_seat = min(all_seats)
    for seat_id in range(min_seat, max_seat+1):
        if seat_id not in all_seats:
            print(f"part2: missing seat: {seat_id}")
    
    end = time.time()
    print(f"Took {end - start}s")
