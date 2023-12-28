import re
data = open("./Day2/day2.txt").read()  # read the file
games = data.split("\n")  # split the file into a list of words


gamesParsed = []
validGames = []
for game in games:
    
    game = re.sub(r"Game [0-9]: ", "", game)
    drawingList = game.split(";")
    drawingListParsed = [re.findall(r"([0-9]+) (red|blue|green)", drawing) for drawing in drawingList]
    rgbDrawingList = []
    for drawing in drawingListParsed:
        rgb = [0,0,0]
        for pull in drawing:
            if pull[1] == "red":
                rgb[0] = int(pull[0])
            elif pull[1] == "green":
                rgb[1] = int(pull[0])
            elif pull[1] == "blue":
                rgb[2] = int(pull[0])
        rgbDrawingList.append(rgb)
    gamesParsed.append(rgbDrawingList)

gamesPower = []
rgbMaxList = []
for (i, game) in enumerate(gamesParsed, start=1):
    rgbMax = [0,0,0]
    for drawing in game:
        if drawing[0] > rgbMax[0]:
            rgbMax[0] = drawing[0]
        if drawing[1] > rgbMax[1]:
            rgbMax[1] = drawing[1]
        if drawing[2] > rgbMax[2]:
            rgbMax[2] = drawing[2]
    rgbMaxList.append(rgbMax)
    gamesPower.append(rgbMax[0] * rgbMax[1] * rgbMax[2])
print(rgbMaxList)
print(sum(gamesPower))





# print(matches[0].group(0))
# print(matches)