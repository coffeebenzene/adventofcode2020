import collections
import time

class PasswordEntry:
    def __init__(self, line):
        spec, password = line.split(":")
        spec_vals, spec_letter = spec.split(" ")
        spec_first, spec_second = (int(x) for x in spec_vals.split("-"))
        password = password.strip()
        self.spec_letter = spec_letter
        self.spec_first = spec_first
        self.spec_second = spec_second
        self.password = password
    
    def validate1(self):
        return self.spec_first <= self.password.count(self.spec_letter) <= self.spec_second
    
    def validate2(self):
        index1 = self.spec_first-1
        index2 = self.spec_second-1
        
        count = ((self.password[index1] == self.spec_letter) + 
                 (self.password[index2] == self.spec_letter)
                )
        return count == 1

if __name__ == "__main__":
    start = time.time()
    
    with open("input.txt") as f:
        password_list = [PasswordEntry(line) for line in f.readlines()]
    
    end = time.time()
    print(f"Took {end - start}s")
    
    total_correct = sum(password.validate1() for password in password_list)
    print(f"part1: {total_correct}")
    
    total_correct = sum(password.validate2() for password in password_list)
    print(f"part2: {total_correct}")
    
    end = time.time()
    print(f"Took {end - start}s")
