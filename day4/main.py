import re
import time

def extract_passports(rawfile):
    data = rawfile.split("\n\n")
    passports = []
    for block in data:
        fields = (field.split(":") for field in block.split())
        passport = {field[0]:field[1] for field in fields}
        passports.append(passport)
    return passports

def is_all_fields_present(passport):
    required_fields = {"byr","iyr","eyr","hgt","hcl","ecl","pid"}
    return required_fields <= passport.keys()

def is_valid_fields(passport):
    try:
        byr = int(passport["byr"])
        if not (1920 <= byr <= 2002):
            return False
        
        iyr = int(passport["iyr"])
        if not (2010 <= iyr <= 2020):
            return False
        
        eyr = int(passport["eyr"])
        if not (2020 <= eyr <= 2030):
            return False
        
        hgt = int(passport["hgt"][:-2])
        if (not (passport["hgt"].endswith("cm") and (150 <= hgt <= 193))
            and not (passport["hgt"].endswith("in") and (59 <= hgt <= 76))):
            return False
    except ValueError:
        return False
    
    if not re.fullmatch("#[0-9a-f]{6}", passport["hcl"]):
        return False
    
    if passport["ecl"] not in ("amb","blu","brn","gry","grn","hzl","oth"):
        return False
    
    if not (passport["pid"].isdigit() and len(passport["pid"]) == 9):
        return False
    
    return True

if __name__ == "__main__":
    start = time.time()
    
    with open("input.txt") as f:
        rawfile = f.read().strip()
    
    passports = extract_passports(rawfile)
    
    valid_passports = [p for p in passports if is_all_fields_present(p)]
    print(f"part1: valid_passports: {len(valid_passports)}")
    
    valid_passports = [p for p in valid_passports if is_valid_fields(p)]
    print(f"part2: valid_passports: {len(valid_passports)}")
    
    end = time.time()
    print(f"Took {end - start}s")
