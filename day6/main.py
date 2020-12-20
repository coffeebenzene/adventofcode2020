import time

def extract_groups(rawfile):
    data = rawfile.split("\n\n")
    groups = []
    for group in data:
        group = group.split("\n")
        groups.append(group)
    return groups

def group_count_any(group):
    answers = set(group[0])
    for person in group:
        answers.update(person)
    return len(answers)

def group_count_all(group):
    answers = set(group[0])
    for person in group:
        answers.intersection_update(person)
    return len(answers)

if __name__ == "__main__":
    start = time.time()
    
    with open("input.txt") as f:
        rawfile = f.read().strip()
    
    groups = extract_groups(rawfile)
    
    group_count = sum(group_count_any(g) for g in groups)
    print(f"part1: group_count: {group_count}")
    
    group_count = sum(group_count_all(g) for g in groups)
    print(f"part2: group_count: {group_count}")
    
    end = time.time()
    print(f"Took {end - start}s")
