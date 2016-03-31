import re

def splitBySpaceAndPunctuation(line) :
    punctuationMarks = r'[.?\-",!():;]'
    foundPunctuation = set(re.findall(punctuationMarks, line))
    for index,item in enumerate(line):
        if re.search(punctuationMarks,item) :
            if checkItemsAreNotDigits(line[index-1], item) :
                    line = line[:index] + " " + line[index:]

    print(line)
    return line.split()

def checkItemsAreNotDigits(prev, current) :
    digitRegex = '\d'
    if prev != " ":
        if not re.match(digitRegex, current) and not re.match(digitRegex, prev):
            return True
    return False


splitBySpaceAndPunctuation("This costs 5.55 dollars!")