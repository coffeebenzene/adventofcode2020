import time

class Rule:
    def __init__(self, line):
        ident, grammar = line.split(":", 1)
        self.id = int(ident)
        self.cases = []
        cases = grammar.split("|")
        for case in cases:
            parsed_case = []
            for elem in case.strip().split():
                if elem.startswith('"') and elem.endswith('"'):
                    elem = elem[1:-1]
                else:
                    elem = int(elem)
                parsed_case.append(elem)
            self.cases.append(tuple(parsed_case))
        self.fully_known = False
        self.check_known()
    
    def check_known(self):
        if self.fully_known:
            return
        if not all(all(isinstance(e, str) for e in case) for case in self.cases):
            return
        self.cases = ["".join(case) for case in self.cases]
        self.fully_known = True
    
    def substitute(self, other_rule):
        if self.fully_known:
            return
        
        all_subbed_cases = []
        for case in self.cases:
            subbed_cases = [[]]
            for elem in case:
                if elem == other_rule.id:
                    case_product = []
                    for c in subbed_cases:
                        for other_c in other_rule.cases:
                            if isinstance(other_c, str):
                                case_product.append(c + [other_c])
                            else:
                                case_product.append(c + list(other_c))
                    subbed_cases = case_product
                else:
                    for c in subbed_cases:
                        c.append(elem)
            all_subbed_cases.extend(subbed_cases)
        
        self.cases = [tuple(c) for c in all_subbed_cases]
        self.check_known()
    
    def __repr__(self):
        return f"Rule({self.id},{self.cases})"

def match_part_generator(self, message, allrules, start):
    for case in self.cases:
        remaining = message
        for elem in case:
            if isinstance(elem, str):
                remaining = matchstart_str(message, elem)
            elif isinstance(elem, int):
                remaining = allrules[elem].matchstart(message, allrules)
            else:
                raise Exception(f"{self}: Unknown element {elem} in {case}")
            if remaining is None:
                break

def process_data(data):
    rules = {}
    for i,line in enumerate(data):
        if line == "":
            break
        rule = Rule(line)
        rules[rule.id] = rule
    return rules, data[i+1:]

def matchrule(message, start_index, ruleid, allrules):
    rule = allrules[ruleid]
    if rule.fully_known:
        for case in rule.cases:
            end_index = start_index + len(case)
            if message[start_index:end_index] == case:
                yield end_index
        return
    
    for case in rule.cases:
        indexes  = [start_index]
        for elem in case:
            next_indexes = []
            if isinstance(elem, str):
                for idx in indexes:
                    end_index = idx + len(elem)
                    if message[idx:end_index] == elem:
                        next_indexes.append(end_index)
            elif isinstance(elem, int):
                for idx in indexes:
                    next_indexes_part = matchrule(message, idx, elem, allrules)
                    next_indexes.extend(next_indexes_part)
            else:
                raise Exception(f"{ruleid}:  Unknown element {elem} in {case}")
            indexes = next_indexes
        for i in indexes:
            yield i

def match_exact(message, ruleid, allrules):
    return len(message) in matchrule(message, 0, ruleid, rules)

def is_optimization_candidate(rule):
    return rule.fully_known and len(rule.cases) <= 4

def optimize_rules(rules):
    optimization_candidates = {r.id for r in rules.values() if is_optimization_candidate(r)}
    
    processed = set()
    while optimization_candidates:
        to_sub = optimization_candidates.pop()
        to_sub = rules[to_sub]
        processed.add(to_sub.id)
        for r in rules.values():
            r.substitute(to_sub)
            if is_optimization_candidate(r) and r.id not in processed:
                optimization_candidates.add(r.id)

if __name__ == "__main__":
    start = time.time()
    
    with open("input.txt") as f:
        data = [line.strip() for line in f.readlines()]
    rules, messages = process_data(data)
    optimize_rules(rules)
    
    count_valid = sum(match_exact(m, 0, rules) for m in messages)
    print(f"Part 1: valid messages: {count_valid}")
    
    with open("input.txt") as f:
        data = [line.strip() for line in f.readlines()]
    rules, messages = process_data(data)
    rules[8] = Rule("8: 42 | 42 8")
    rules[11] = Rule("11: 42 31 | 42 11 31")
    optimize_rules(rules)
    
    count_valid = sum(match_exact(m, 0, rules) for m in messages)
    print(f"Part 2: valid messages: {count_valid}")
    
    end = time.time()
    print(f"Took {end - start}s")
