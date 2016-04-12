import re
import unittest

def splitBySpaceAndPunctuation(line) :
    #regular expressions
    specialSymbols = r'[.?\",!():;$£%^&*¬+]'
    alphanumericalCharacters= r'[a-zA-Z0-9]'
    capitalLetters = r'[A-Z]'
    hyphen = r'[-]'

    modificationsMade = 0 #for indexing reasons
    lineCopy = line #copy of the original piece of text, needed for indexing reasons
    for index,item in enumerate(line):
        if index != 0: #cases where need to check the previous symbol before the actual item we're looking at
            # dealing with possessive nouns in plural
            if re.search('\'', item) and re.search('s', line[index - 1]):
                lineCopy = insertIdentifierAtIndex('(p)', index + modificationsMade, lineCopy)
                modificationsMade = modificationsMade + 1

            #dealing with possessive nouns in singular
            if isItemApostropheAndIsFollowedByLowerCaseLetters(item, line, index):
                if (index + 1 <= len(line) - 1):
                    if re.search(' ', line[index + 1]) or re.search('s', line[index + 1]):
                        lineCopy = insertIdentifierAtIndex('(p)', index + modificationsMade, lineCopy)
                        modificationsMade = modificationsMade + 1

            #dealing with cases like "don't", "doesn't"
            if isItemApostropheAndIsFollowedByLowerCaseLetters(item, line, index) and isItemSurroundedByCertainLetters('n', 't', line, index):
                lineCopy = insertSpaceIntoStringAfterItemAtSomeIndex(lineCopy, index - 2 + modificationsMade)
                lineCopy = insertIdentifierAtIndex('o', index + 1 + modificationsMade, lineCopy)
                modificationsMade = modificationsMade + 2


            # deal with last names and other cases where pattern is like [A-Z'A-Z]
            if re.search('\'', item) and index != len(line) -1 :
                if re.search(capitalLetters, line[index-1]) and re.search(capitalLetters, line[index+1]) :
                    lineCopy = insertSpaceIntoStringAfterItemAtSomeIndex(lineCopy,index+modificationsMade)
                    lineCopy = insertSpaceIntoStringAfterItemAtSomeIndex(lineCopy, index-1 + modificationsMade)
                    modificationsMade = modificationsMade +2

            # dealing with hyphens (e.g. up-to-date)
            if (re.search(hyphen, item)):
                if index + 1 < len(line) and not re.search(alphanumericalCharacters, line[index - 1]) and not re.search(alphanumericalCharacters, line[index + 1]):
                    lineCopy = insertSpaceIntoStringAfterItemAtSomeIndex(lineCopy, index + modificationsMade)
                    modificationsMade = modificationsMade + 1



        #separate punctuation but doesn't separate digits if there's punctuation between them
        if re.search(specialSymbols,item) and re.search(specialSymbols,item) and bothItemsAreNotDigits(line[index-1], item) :
            lineCopy = insertSpaceIntoStringAfterItemAtSomeIndex(lineCopy, index+modificationsMade)
            modificationsMade = modificationsMade + 1

        if re.search(alphanumericalCharacters, item) and index != len(line) - 1:
            if re.search(specialSymbols, line[index+1]) : #if the next symbol after the capital letter is a special symbol
                lineCopy = insertSpaceIntoStringAfterItemAtSomeIndex(lineCopy, index + modificationsMade)
                modificationsMade = modificationsMade + 1


    print(lineCopy)
    return lineCopy.split()

def bothItemsAreNotDigits(prev, current) :
    digitRegex = '\d'
    if not re.match(digitRegex, current) and not re.match(digitRegex, prev):
        return True
    return False
def insertIdentifierAtIndex(identifer, index, line) :
    return line[:index] + identifer + line[index+len(identifer):]


def insertSpaceIntoStringAfterItemAtSomeIndex(line, index) :
    return line[:index+1] + " " + line[index+1:]

def isItemApostropheAndIsFollowedByLowerCaseLetters(item, line, currentItemsIndex):
    lowerCaseLetters = r'[a-z]'
    apostrophe = r'[\']'
    return (re.search(apostrophe, item)) and re.search(lowerCaseLetters, line[currentItemsIndex - 1])

def isItemSurroundedByCertainLetters(letterOne, letterTwo, line, currentItemIndex) :
    return re.search(letterOne, line[currentItemIndex - 1]) and re.search(letterTwo, line[currentItemIndex + 1])

splitBySpaceAndPunctuation("doesn't")

class TestTokeniser(unittest.TestCase):

    def testCheckItemsAreNotDigits(self):
        self.assertTrue(bothItemsAreNotDigits('a', 'b'))
        self.assertFalse(bothItemsAreNotDigits('a', '1'))
        self.assertFalse(bothItemsAreNotDigits('2', '1'))

    def testInsertSpaceIntoStringAfterSomeIndex(self):
        self.assertEqual(insertSpaceIntoStringAfterItemAtSomeIndex("hello", 0), "h ello")
        self.assertEqual(insertSpaceIntoStringAfterItemAtSomeIndex("hello", 1), "he llo")
        self.assertEqual(insertSpaceIntoStringAfterItemAtSomeIndex("hello", 2), "hel lo")
        self.assertEqual(insertSpaceIntoStringAfterItemAtSomeIndex("hello", 10), "hello ")

    def testSplipBySpaceAndPunctuation(self):
        self.assertEqual(splitBySpaceAndPunctuation("..."), '. . . '.split())
        self.assertEqual(splitBySpaceAndPunctuation("Hello world."), 'Hello world .'.split())
        self.assertEqual(splitBySpaceAndPunctuation("J. Smith said that..."), 'J . Smith said that . . . '.split())
        self.assertEqual(splitBySpaceAndPunctuation("O'Neill"), 'O \' Neill'.split())
        self.assertEqual(splitBySpaceAndPunctuation("Ivan's"), 'Ivan(p)'.split())
        self.assertEqual(splitBySpaceAndPunctuation("Jones\'"), 'Jones(p)'.split())
        self.assertEqual(splitBySpaceAndPunctuation("symbols (characters or word or phrases)."), 'symbols ( characters or word or phrases ) .'.split())
        self.assertEqual(splitBySpaceAndPunctuation("up-to-date"), 'up-to-date'.split())
        self.assertEqual(splitBySpaceAndPunctuation("New-York based"), 'New-York based'.split())
        self.assertEqual(splitBySpaceAndPunctuation("doesn't"), 'does not'.split())
        self.assertEqual(splitBySpaceAndPunctuation("don't"), 'do not'.split())


suite = unittest.TestLoader().loadTestsFromTestCase(TestTokeniser)
unittest.TextTestRunner().run(suite)