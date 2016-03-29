import re

def splitBySpaceAndPunctuation(line) :
    punctuationMarks = r'[.?\-",!():;]'
    foundPunctuation = set(re.findall(punctuationMarks, line))
    print(foundPunctuation)
    for index,item in enumerate(line):
        for punctuation in foundPunctuation :
            if item == punctuation and line[index-1] != " " :
                if not re.match('\d', item) and not re.match('\d',  line[index-1]) :
                    line = line[:index] + " " + line[index:]

    print(line)
    return line.split()


splitBySpaceAndPunctuation("This costs 5.55 dollars!")