import re
data = open("./Day1/day1.txt").read()  # read the file
words = data.split("\n")  # split the file into a list of words
words = words[:1]
accum = 0
digits = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
for j in range(len(words)):
    word = words[j]
    findlist = []
    for i in range(9):
        xs = re.finditer(digits[i], word)
        findlist.append([xs,i+1])
        xs = re.finditer(str(i+1), word)
        findlist.append([xs,i+1])
    print(findlist)
    word2 = []
    # for (x,i) in findlist:
    #     if x != -1:
    #         word2.append(str(i))
    #         break
    # word2.append(findlist[-1][1] )
    # print(word2)

    # for char in word:
    #     if char.isalpha():
    #         word = word.replace(char, "")
    # words[j] = word

    # accum += int(word2[0])*10 + int(word2[-1])

# print(accum)
print(words)
print(accum)