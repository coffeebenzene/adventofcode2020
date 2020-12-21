import inspect
import time

def parse_line(line):
    tokens = []
    number_part = []
    for c in line:
        if c.isspace():
            continue
        
        if c.isdigit():
            number_part.append(c)
        elif number_part:
            tokens.append(int("".join(number_part)))
            number_part = []
        
        if not c.isdigit():
            tokens.append(c)
    
    if number_part:
        tokens.append(int("".join(number_part)))
    
    return tokens

class Frame:
    operator_map = {
        "+" : lambda x,y : x+y,
        "*" : lambda x,y : x*y,
    }
    
    def __init__(self):
        self.val = 0
        self.last_operator = "+"
    
    def set_last_operator(self, operator_token):
        self.last_operator = operator_token
    
    def apply_last_operator(self, other_val):
        self.val = self.operator_map[self.last_operator](self.val, other_val)
        self.last_operator = None
    
    def __repr__(self):
        return f"Frame({self.val}, {self.last_operator})"

def evaluate_expression(expression):
    stack = [Frame()]
    for t in expression:
        if isinstance(t, int):
            stack[-1].apply_last_operator(t)
        elif t in Frame.operator_map:
            stack[-1].set_last_operator(t)
        elif t == "(":
            stack.append(Frame())
        elif t == ")":
            completed_frame = stack.pop()
            stack[-1].apply_last_operator(completed_frame.val)
    return stack.pop().val

def shunting_yard_convert(expression, precedence):
    operator_stack = []
    output_queue = []
    for t in expression:
        if isinstance(t, int):
            output_queue.append(t)
        elif t in precedence:
            while (operator_stack
                   and operator_stack[-1] != "(" 
                   and precedence[operator_stack[-1]] >= precedence[t]):
                output_queue.append(operator_stack.pop())
            operator_stack.append(t)
        elif t == "(":
            operator_stack.append(t)
        elif t == ")":
            while operator_stack[-1] != "(":
                output_queue.append(operator_stack.pop())
            operator_stack.pop()
    
    while operator_stack:
        output_queue.append(operator_stack.pop())
    
    return output_queue

def shunting_yard_evaluate(expression, precedence):
    operator_map = {
        "+" : lambda x,y : x+y,
        "*" : lambda x,y : x*y,
    }
    operator_map = {
        k : (v, len(inspect.signature(v).parameters))
        for k,v in operator_map.items()
    }
    
    output_queue = shunting_yard_convert(expression, precedence)
    
    evaluation_stack = []
    for t in output_queue:
        if isinstance(t, int):
            evaluation_stack.append(t)
        if t in operator_map:
            opfunc, param_count = operator_map[t]
            args = reversed([evaluation_stack.pop() for i in range(param_count)])
            result = opfunc(*args)
            evaluation_stack.append(result)
    
    return evaluation_stack.pop()

if __name__ == "__main__":
    start = time.time()
    
    with open("input.txt") as f:
        lines = f.readlines()
    
    expressions = [parse_line(line) for line in lines]
    #total_sum = sum(evaluate_expression(e) for e in expressions)
    total_sum = sum(shunting_yard_evaluate(e, {"+":0,"*":0}) for e in expressions)
    print(f"part1: total sum = {total_sum}")
    
    total_sum = sum(shunting_yard_evaluate(e, {"+":1,"*":0}) for e in expressions)
    print(f"part2: total sum = {total_sum}")
    
    end = time.time()
    print(f"Took {end - start}s")
