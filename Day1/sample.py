import sys

zero = ord('0')
nine = ord('9')

# lines = [l for l in sys.stdin.readlines()]


data = open("day1.txt").read()  # read the file
lines = data.split("\n")  # split the file into a list of words

sum1 = 0
for line in lines:
    for c in map(ord, line):
        if zero <= c <= nine:
            digit_one = chr(c)
            break
    for c in map(ord, reversed(line)):
        if zero <= c <= nine:
            digit_two = chr(c)
            break
    sum1 += int(digit_one + digit_two)

print(sum1)

import re

nums = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
r_nums = [''.join(reversed(n)) for n in nums]

def parens(x):
    return f"({x})"
FWD_RE = '|'.join(map(parens, nums))
REV_RE = '|'.join(map(parens, r_nums))



sum2 = 0
for line in lines:
    m = re.search(FWD_RE, line)
    for i, c in enumerate(map(ord, line)):
        if zero <= c <= nine:
            index = i
            digit_one = chr(c)
            break
    if m is not None:
        regex_i = m.start(0)
        if regex_i < index:
            digit_one = nums.index(m[0]) + 1


    line = ''.join(reversed(line))
    m = re.search(REV_RE, line)
    for i, c in enumerate(map(ord, line)):
        if zero <= c <= nine:
            index = i
            digit_two = chr(c)
            break
    if m is not None:
        regex_i = m.start(0)
        if regex_i < index:
            digit_two = r_nums.index(m[0]) + 1

    my_str = f"{digit_one}{digit_two}"
    sum2 += int(my_str)
print(sum2)