import re
import unittest



def tokenise(line) :
    #regular expressions
    specialSymbols = r'[.?\",!():;$£%^&*¬+]'
    alphanumericalCharacters= r'[a-zA-Z0-9]'
    capitalLetters = r'[A-Z]'
    hyphen = r'[-]'

    modificationsMade = 0 #for indexing reasons
    lineCopy = line #copy of the original piece of text, needed for indexing reasons
    for index,item in enumerate(line):
        if index != 0: #cases where need to check the previous symbol before the actual item we're looking at
            lineCopy = dealWithPossessiveNouns(item, line, index, modificationsMade, lineCopy)
            modificationsMade  = len(lineCopy) - len(line)

            #dealing with negations like "don't", "doesn't"
            if isItemApostropheAndIsFollowedByLowerCaseLetters(item, line, index) and isItemSurroundedByCertainLetters('n', 't', line, index):
                lineCopy = insertSpaceIntoStringAfterItemAtSomeIndex(lineCopy, index - 2 + modificationsMade)
                lineCopy = insertIdentifierAtIndex('o', index + 1 + modificationsMade, lineCopy, False)
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

def insertIdentifierAtIndex(identifer, index, line, spaceAfterIdentifier) :
    if spaceAfterIdentifier :
        return line[:index] + identifer + " " + line[index+len(identifer):]
    return line[:index] + identifer + line[index + len(identifer):]


def insertSpaceIntoStringAfterItemAtSomeIndex(line, index) :
    return line[:index+1] + " " + line[index+1:]

def isItemApostropheAndIsFollowedByLowerCaseLetters(item, line, currentItemsIndex):
    lowerCaseLetters = r'[a-z]'
    apostrophe = r'[\']'
    return (re.search(apostrophe, item)) and re.search(lowerCaseLetters, line[currentItemsIndex - 1])

def isItemSurroundedByCertainLetters(letterOne, letterTwo, line, currentItemIndex) :
    return re.search(letterOne, line[currentItemIndex - 1]) and re.search(letterTwo, line[currentItemIndex + 1])

def dealWithPossessiveNouns(item, line, index, modificationsMade, lineCopy) :
    # dealing with possessive nouns in plural
    if re.search('\'', item) and re.search('s', line[index - 1]):
        lineCopy = insertIdentifierAtIndex('(p)', index + modificationsMade, lineCopy, True)
        modificationsMade = modificationsMade + 1

    # dealing with possessive nouns in singular
    if isItemApostropheAndIsFollowedByLowerCaseLetters(item, line, index):
        if (index + 1 <= len(line) - 1):
            if re.search(' ', line[index + 1]) or re.search('s', line[index + 1]):
                lineCopy = insertIdentifierAtIndex('(p)', index + modificationsMade, lineCopy, True)
                modificationsMade = modificationsMade + 1
    return lineCopy

tokenise(" Vanya's doesn't")

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
        self.assertEqual(tokenise("..."), '. . . '.split())
        self.assertEqual(tokenise("Hello world."), 'Hello world .'.split())
        self.assertEqual(tokenise("J. Smith said that..."), 'J . Smith said that . . . '.split())
        self.assertEqual(tokenise("O'Neill"), 'O \' Neill'.split())
        self.assertEqual(tokenise("Ivan's"), 'Ivan(p)'.split())
        self.assertEqual(tokenise("Jones\'"), 'Jones(p)'.split())
        self.assertEqual(tokenise("symbols (characters or word or phrases)."), 'symbols ( characters or word or phrases ) .'.split())
        self.assertEqual(tokenise("up-to-date"), 'up-to-date'.split())
        self.assertEqual(tokenise("New-York based"), 'New-York based'.split())
        self.assertEqual(tokenise("doesn't"), 'does not'.split())
        self.assertEqual(tokenise("don't"), 'do not'.split())
        self.assertEqual(tokenise("Vanya's doesn't"), 'Vanya(p) does not'.split())


suite = unittest.TestLoader().loadTestsFromTestCase(TestTokeniser)
unittest.TextTestRunner().run(suite)