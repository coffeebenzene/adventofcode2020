import collections
import time

def remove_bag(color_bag):
    color_bag = color_bag.strip()
    if color_bag.endswith(" bags"):
        color_bag = color_bag[:-5]
    elif color_bag.endswith(" bag"):
        color_bag = color_bag[:-4]
    return color_bag

def get_num_color(num_color_bag):
    num_color = remove_bag(num_color_bag)
    num, color = num_color.split(" ", 1)
    num = int(num)
    return (num, color)

# rule_graph = {color: [(num, color), ...], ...}
def construct_graph(rules):
    rule_graph = {}
    for line in rules:
        line = line.strip().strip(".")
        container, contents = line.split(" contain ")
        container = remove_bag(container)
        if contents == "no other bags":
            contents = []
        else:
            contents = [get_num_color(c) for c in contents.split(",")]
        rule_graph[container] = contents
    return rule_graph

def reverse_graph(rule_graph):
    reverse_rule_graph = collections.defaultdict(list)
    for color, content in rule_graph.items():
        for num, content_color in content:
            reverse_rule_graph[content_color].append(color)
    return reverse_rule_graph

def find_possible_origins(rule_graph, wanted_color):
    reverse_rule_graph = reverse_graph(rule_graph)
    queue = collections.deque([wanted_color])
    possible_origins = set()
    
    while queue:
        current_color = queue.popleft()
        if current_color not in reverse_rule_graph:
            continue
        containers = reverse_rule_graph.pop(current_color)
        queue.extend(containers)
        possible_origins.update(containers)
    
    return possible_origins

def find_num_contained(rule_graph, wanted_color, memo=None):
    if memo is None:
        memo = {}
    
    if wanted_color in memo:
        return memo[wanted_color]
    
    contents = rule_graph[wanted_color]
    count = 0
    for num, color in contents:
        count += num * (1 + find_num_contained(rule_graph, color, memo)) 
    
    memo[wanted_color] = count
    
    return count

if __name__ == "__main__":
    start = time.time()
    
    with open("input.txt") as f:
        rules = f.readlines()
    
    rule_graph = construct_graph(rules)
    
    origins = find_possible_origins(rule_graph, "shiny gold")
    print(f"part1: possible containers: {len(origins)}")
    
    num_contained = find_num_contained(rule_graph, "shiny gold")
    print(f"part2: Number of bags contained: {num_contained}")
    
    end = time.time()
    print(f"Took {end - start}s")
