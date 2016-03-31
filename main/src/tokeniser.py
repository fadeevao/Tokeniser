import re
import unittest

def splitBySpaceAndPunctuation(line) :
    punctuationMarks = r'[.?\-",!():;]'
    specialSymbols = r'[$£%^&*¬+]'
    for index,item in enumerate(line):
        if re.search(specialSymbols, item):
            line = insertSpaceIntoStringAfterItemAtSomeIndex(line, index)

        if re.search(punctuationMarks,item) :
            if bothItemsAreNotDigits(line[index-1], item) :
                line = insertSpaceIntoStringAfterItemAtSomeIndex(line, index)
    print(line)
    return line.split()

def bothItemsAreNotDigits(prev, current) :
    digitRegex = '\d'
    if prev != " ":
        if not re.match(digitRegex, current) and not re.match(digitRegex, prev):
            return True
    return False

def insertSpaceIntoStringAfterItemAtSomeIndex(line, index) :
    return line[:index+1] + " " + line[index+1:]

splitBySpaceAndPunctuation("nh %5.55 dollars!")

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


suite = unittest.TestLoader().loadTestsFromTestCase(TestTokeniser)
unittest.TextTestRunner().run(suite)