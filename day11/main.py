import collections
import functools
import time

Coord = collections.namedtuple("Coord", ["row","col"])

def preprocess_seats(data):
    seats = []
    for line in data:
        line = line.strip()
        row = [True if c=="L" else None for c in line]
        seats.append(row)
    return seats

@functools.lru_cache(maxsize=None)
def get_neighbours(row, col, row_len, col_len):
    row_range = [row-1, row+2]
    col_range = [col-1, col+2]
    row_range = [min(max(x, 0), row_len) for x in row_range]
    col_range = [min(max(x, 0), col_len) for x in col_range]
    
    neighbours = []
    for i in range(*row_range):
        for j in range(*col_range):
            if (i,j) == (row,col):
                continue
            neighbours.append((i,j))
    
    return neighbours

def next_step(seats):
    row_len = len(seats)
    col_len = len(seats[0])
    
    new_seats = []
    
    for i, row in enumerate(seats):
        new_row = []
        for j, seat in enumerate(row):
            if seat is None:
                new_row.append(None)
                continue
            
            neighbours = get_neighbours(i, j, row_len, col_len)
            if seat:
                occupied = sum(seats[n[0]][n[1]] for n in neighbours
                               if seats[n[0]][n[1]] is not None)
                new_row.append(occupied < 4)
            else:
                can_seat = not any(seats[n[0]][n[1]] for n in neighbours)
                new_row.append(can_seat)
        new_seats.append(new_row)
    
    return new_seats

def find_stable(seats):
    while True:
        new_seats = next_step(seats)
        if new_seats == seats:
            return seats
        seats = new_seats

def count_occupied(seats):
    total = 0
    for row in seats:
        total += sum(x for x in row if x is not None)
    return total

def str_seats(seats):
    char_map = {
        True:"#",
        False:"L",
        None:"."
    }
    
    seats = "\n".join("".join(char_map[s] for s in row) for row in seats)
    
    return seats

def add_coord(coord1, coord2):
    return Coord(coord1.row+coord2.row, coord1.col+coord2.col)

class SeatSimulation:
    def __init__(self, seats, max_range=1, leave_threshold=4):
        self.seats = seats
        self.sights = self.compute_all_sights(max_range)
        self.leave_threshold = leave_threshold
    
    def in_boundary(self, coord):
        return (0 <= coord.row < len(self.seats)
                and 0 <= coord.col < len(self.seats[0]))
    
    def get_seat(self, coord):
        return self.seats[coord.row][coord.col]
    
    def compute_sight(self, coord, max_range=1):
        directions = [Coord(i,j) for i in range(-1,2) for j in range(-1,2)]
        directions.remove(Coord(0,0))
        sight = []
        for d in directions:
            current = coord
            for i in range(max_range):
                current = add_coord(current, d)
                if not self.in_boundary(current):
                    break
                seat_val = self.get_seat(current)
                if seat_val is not None:
                    sight.append(current)
                    break
        return sight
    
    def compute_all_sights(self, max_range=1):
        sights = {}
        for i, row in enumerate(self.seats):
            for j, seat in enumerate(row):
                if seat is None:
                    continue
                seat_coord = Coord(i,j)
                sights[seat_coord] = self.compute_sight(seat_coord, max_range)
        return sights
    
    def next_iter(self):
        new_seats = []
        for i, row in enumerate(self.seats):
            new_row = []
            for j, seat in enumerate(row):
                if seat is None:
                    new_row.append(None)
                    continue
                seat_coord = Coord(i,j)
                sighted_seats = self.sights[seat_coord]
                if seat:
                    occupied = sum(self.get_seat(s) for s in sighted_seats
                                   if self.get_seat(s) is not None)
                    new_row.append(occupied < self.leave_threshold)
                else:
                    can_seat = not any(self.get_seat(s) for s in sighted_seats)
                    new_row.append(can_seat)
            new_seats.append(new_row)
        self.seats = new_seats
    
    def iterate_till_stable(self):
        while True:
            previous_seats = self.seats
            self.next_iter()
            if previous_seats == self.seats:
                break
    
    def print_seats(self):
        print(str_seats(self.seats))
        print()
    
    def get_num_occupied(self):
        return count_occupied(self.seats)

if __name__ == "__main__":
    start = time.time()
    
    with open("input.txt") as f:
        data = f.readlines()
    seats = preprocess_seats(data)
    
    #stable_seats = find_stable(seats)
    #num_occupied = count_occupied(stable_seats)
    seat_sim = SeatSimulation(seats)
    seat_sim.iterate_till_stable()
    num_occupied = seat_sim.get_num_occupied()
    print(f"part1: num occupied = {num_occupied}")
    
    seat_sim = SeatSimulation(seats, max_range=max(len(seats), len(seats[0])), leave_threshold=5)
    seat_sim.iterate_till_stable()
    num_occupied = seat_sim.get_num_occupied()
    print(f"part2: num occupied = {num_occupied}")
    
    end = time.time()
    print(f"Took {end - start}s")
