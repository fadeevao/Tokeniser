import re
import unittest

def splitBySpaceAndPunctuation(line) :
    #regular expressions
    specialSymbols = r'[.?\-",!():;$£%^&*¬+]'
    alphanumericalCharacters= r'[a-zA-Z0-9]'
    apostrophe = r'[\']'
    capitalLetters = r'[A-Z]'

    spacesInserted = 0 #for indexing reasons
    lineCopy = line #copy of the original piece of text, needed for indexing reasons
    for index,item in enumerate(line):

        #separate punctuation but doesn't separate digits if there's punctuation between them
        if re.search(specialSymbols,item) :
            if bothItemsAreNotDigits(line[index-1], item) :
                lineCopy = insertSpaceIntoStringAfterItemAtSomeIndex(lineCopy, index+spacesInserted)
                spacesInserted = spacesInserted + 1

        if re.search(alphanumericalCharacters, item) and index != len(line) - 1:
            if re.search(specialSymbols, line[index+1]) : #if the next symbol after the capital letter is a special symbol
                lineCopy = insertSpaceIntoStringAfterItemAtSomeIndex(lineCopy, index + spacesInserted)
                spacesInserted = spacesInserted + 1

        #deal with last names and other cases where pattern is like [A-Z'A-Z]
        if re.search(apostrophe, item) :
            if index != 0 and index != len(line) -1 :
                if re.search(capitalLetters, line[index-1]) and re.search(capitalLetters, line[index+1]) :
                    lineCopy = insertSpaceIntoStringAfterItemAtSomeIndex(lineCopy,index+spacesInserted)
                    lineCopy = insertSpaceIntoStringAfterItemAtSomeIndex(lineCopy, index-1 + spacesInserted)
                    spacesInserted = spacesInserted +2


    print(lineCopy)
    return lineCopy.split()

def bothItemsAreNotDigits(prev, current) :
    digitRegex = '\d'
    if not re.match(digitRegex, current) and not re.match(digitRegex, prev):
        return True
    return False


def insertSpaceIntoStringAfterItemAtSomeIndex(line, index) :
    return line[:index+1] + " " + line[index+1:]

splitBySpaceAndPunctuation("O'Neill")

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

suite = unittest.TestLoader().loadTestsFromTestCase(TestTokeniser)
unittest.TextTestRunner().run(suite)