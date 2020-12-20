import time

class Field():
    def __init__(self, name, ranges):
        self.name = name
        self.ranges = list(ranges)
    
    def valid(self, val):
        return any(val in r for r in self.ranges)
    
    def __eq__(self, other):
        return self.name == other.name
    
    def __hash__(self):
        return hash(self.name)
    
    def __repr__(self):
        return f'Field("{self.name}", {self.ranges})'

def process_data(data):
    data_generator = iter(data)
    fields = []
    for line in data_generator:
        if not line or line.isspace():
            break
        name, ranges = line.strip().split(": ")
        ranges = ranges.split(" or ")
        ranges = (r.split("-") for r in ranges)
        field = Field(name, [range(int(r[0]), int(r[1])+1) for r in ranges])
        fields.append(field)
    
    next(data_generator) # Consume "your ticket:"
    myticket = [int(x) for x in next(data_generator).strip().split(",")]
    
    next(data_generator) # Consume "<newline>"
    next(data_generator) # Consume "nearby tickets:"
    nearby_tickets = []
    for line in data_generator:
        if not line or line.isspace():
            break
        ticket = [int(x) for x in line.strip().split(",")]
        nearby_tickets.append(ticket)
    
    return fields, myticket, nearby_tickets

def scanning_error_rate_1ticket(fields, ticket):
    error_rate = 0
    for val in ticket:
        if not any(f.valid(val) for f in fields):
            error_rate += val
    return error_rate

def scanning_error_rate(fields, tickets):
    return sum(scanning_error_rate_1ticket(fields, t) for t in tickets)

def possibly_valid_ticket(fields, ticket):
    for val in ticket:
        if not any(f.valid(val) for f in fields):
            return False
    return True

def identify_field_positions(fields, myticket, tickets):
    tickets = [t for t in tickets if possibly_valid_ticket(fields, t)]
    tickets.append(myticket)
    
    possibilities = [set(fields) for i in myticket]
    for t in tickets:
        for idx, val in enumerate(t):
            possibilities[idx].intersection_update(f for f in possibilities[idx] if f.valid(val))
    
    known_fields = [None for _ in possibilities]
    have_change = True
    while have_change:
        have_change = False
        for i, p in enumerate(possibilities):
            if len(p) == 1:
                known_field = p.pop()
                for p2 in possibilities:
                    p2.discard(known_field)
                known_fields[i] = known_field
                have_change = True
    
    return known_fields

def get_departure_product(known_fields, myticket):
    prod = 1
    for field, val in zip(known_fields, myticket):
        if field.name.startswith("departure"):
            prod *= val
    return prod

if __name__ == "__main__":
    start = time.time()
    
    with open("input.txt") as f:
        data = f.readlines()
    
    fields, myticket, nearby_tickets = process_data(data)
    error_rate = scanning_error_rate(fields, nearby_tickets)
    print(f"Part 1: scanning error rate: {error_rate}")
    
    known_fields = identify_field_positions(fields, myticket, nearby_tickets)
    departure_product = get_departure_product(known_fields, myticket)
    print(f"Part 2: departure product: {departure_product}")
    
    end = time.time()
    print(f"Took {end - start}s")
