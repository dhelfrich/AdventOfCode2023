import re
from collections import deque

def hash(string):
    result = 0
    for char in string:
        result += ord(char)
        result = result * 17 % 256
    return result

def partOneAnswer(strings):
    output = 0
    for s in strings:
        output += hash(s)
    return output

def partTwoAnswer(strings):
    boxList = [{} for i in range(256)]
    for s in strings:
        m = re.fullmatch(r'([a-z]+)([-=])([1-9]?)', s)
        label = m.group(1)
        box = hash(label)
        op = m.group(2)
        focal = m.group(3)
        if op == '-':
            if boxList[box].get(label):
                del boxList[box][label]
        if op == '=':
            boxList[box][label] = int(focal)
    power = 0
    for i, box in enumerate(boxList):
        for j, label in enumerate(box.keys()):
            power += (i + 1) * (j + 1) * box[label]
    print(power)


def main():
    data = open("./Day15/day15.txt").read()  # read the file
    # data = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
    strings = data.split(",")  # split the file into a list of words
    print(partOneAnswer(strings))
    partTwoAnswer(strings)


main()