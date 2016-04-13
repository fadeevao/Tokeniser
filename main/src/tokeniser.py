# -*- coding: utf-8 -*-
import re
import unittest

'''
Tokenisation rules are following:
- all punctuation marks are separated as tokens apart from the cases when they are parts of symbols (eg: up-to-date, $55, 5.44 and so on)
- for all possessive nouns/pronouns (that we identify with 's or s' we add (p) and remove the 's' as we don't want it to be a separate token as it doesn't carry much meaning
    examples of this would be: Jones\' -> Jones(p), Ivan's -> Ivan(p)
- We deal with negations (such as 'doesn't') by separating them into 2 tokens such as: does, not  (special case for can't as it needs to turn into cannot)
'''


class TokenisationController() :

    def __init__(self):
        ()

    def bothItemsAreNotDigits(self, prev, current):
        digitRegex = '\d'
        if not re.match(digitRegex, current) and not re.match(digitRegex, prev):
            return True
        return False

    def isHyphenInNeedOfSpaceAroundIt(self, line, index) :
        alphanumericalCharacters = r'[a-zA-Z0-9]'
        return (not re.search(alphanumericalCharacters, line[index - 1]) and not re.search(alphanumericalCharacters,line[index + 1])) \
               or (not re.search(alphanumericalCharacters, line[index-1]) and re.search(alphanumericalCharacters,line[index + 1])) \
                or ( re.search(alphanumericalCharacters, line[index-1]) and not re.search(alphanumericalCharacters,line[index + 1]))

    def insertIdentifierAtIndex(self, identifer, index, line, spaceAfterIdentifier) :
        if spaceAfterIdentifier :
            return line[:index] + identifer + " " + line[index+len(identifer):]
        return line[:index] + identifer + line[index + len(identifer):]


    def insertSpaceIntoStringAfterItemAtSomeIndex(self, line, index) :
        return line[:index+1] + " " + line[index+1:]

    def insertSpaceIntoStringBeforeItemAtSomeIndex(self, line, index) :
        return line [:index]+ " " + line[index:]

    def isItemApostropheAndIsFollowedByLowerCaseLetters(self, item, line, currentItemsIndex):
        lowerCaseLetters = r'[a-z]'
        apostrophe = r'[\']'
        return (re.search(apostrophe, item)) and re.search(lowerCaseLetters, line[currentItemsIndex - 1])

    def isItemSurroundedByCertainLetters(self, letterOne, letterTwo, line, currentItemIndex) :
        return re.search(letterOne, line[currentItemIndex - 1]) and re.search(letterTwo, line[currentItemIndex + 1])

    def dealWithPossessiveNouns(self, item, line, index, modificationsMade, lineCopy) :
        # dealing with possessive nouns in plural
        if re.search('\'', item) and re.search('s', line[index - 1]):
            lineCopy = self.insertIdentifierAtIndex('(p)', index + modificationsMade, lineCopy, True)
            modificationsMade = modificationsMade + 1

        # dealing with possessive nouns in singular
        if self.isItemApostropheAndIsFollowedByLowerCaseLetters(item, line, index):
            if (index + 1 <= len(line) - 1):
                if re.search(' ', line[index + 1]) or re.search('s', line[index + 1]):
                    lineCopy = self.insertIdentifierAtIndex( '(p)', index + modificationsMade, lineCopy, True)
                    modificationsMade = modificationsMade + 1
        return lineCopy

    def dealWithApostrophesInLastNames(self, index, modificationsMade, lineCopy) :
        lineCopy = self.insertSpaceIntoStringAfterItemAtSomeIndex(lineCopy, index + modificationsMade)
        lineCopy = self.insertSpaceIntoStringAfterItemAtSomeIndex(lineCopy, index - 1 + modificationsMade)
        return lineCopy


    def dealWithNegations(self, item, line, index, modificationsMade, lineCopy) :
        lineCopy = self.insertSpaceIntoStringAfterItemAtSomeIndex(lineCopy, index - 2 + modificationsMade)
        modificationsMade = modificationsMade + 1
        lineCopy = self.insertIdentifierAtIndex('o', index + modificationsMade, lineCopy, False)
        return lineCopy

    def tokenise(self, line) :
        #regular expressions
        specialSymbols = r'[.?,!():;$£%^&*¬+]'
        alphanumericalCharacters= r'[a-zA-Z0-9]'
        capitalLetters = r'[A-Z]'
        hyphen = r'[-]'

        modificationsMade = 0 #for indexing reasons
        lineCopy = line #copy of the original piece of text, needed for indexing reasons
        for index,item in enumerate(line):
            prev = line[index - 1]
            if index != 0: #cases where need to check the previous symbol before the actual item we're looking at

                lineCopy = self.dealWithPossessiveNouns(item, line, index, modificationsMade, lineCopy)

                #dealing with negations like "don't", "doesn't"
                if self.isItemApostropheAndIsFollowedByLowerCaseLetters(item, line, index) and self.isItemSurroundedByCertainLetters('n', 't', line, index):
                    print (line[index-3:index])
                    if line[index-3:index] == 'can' : #deal with can't -> cannot
                        lineCopy = lineCopy[:index] + 'not' + lineCopy[index+2:]
                    else:
                         lineCopy = self.dealWithNegations(item, line, index, modificationsMade, lineCopy)

                # deal with last names and other cases where pattern is like [A-Z'A-Z]
                if re.search('\'', item) and index != len(line) -1 :
                    if re.search(capitalLetters, prev) and re.search(capitalLetters, line[index+1]) :
                        lineCopy = self.dealWithApostrophesInLastNames(index, modificationsMade, lineCopy)

                # dealing with hyphens (e.g. up-to-date - in this case there should be no changes)
                if (re.search(hyphen, item)):
                    if index + 1 < len(line) and self.isHyphenInNeedOfSpaceAroundIt(line, index):
                        lineCopy = self.insertSpaceIntoStringAfterItemAtSomeIndex(lineCopy, index + modificationsMade)
                        lineCopy = self.insertSpaceIntoStringBeforeItemAtSomeIndex(lineCopy, index + modificationsMade)


            #separate punctuation but doesn't separate digits if there's punctuation between them
            if re.search(specialSymbols,item) and re.search(specialSymbols,item) and self.bothItemsAreNotDigits(prev, item) :
                lineCopy = self.insertSpaceIntoStringAfterItemAtSomeIndex(lineCopy, index+modificationsMade)

            if re.search(alphanumericalCharacters, item) and index != len(line) - 1:
                if re.search(specialSymbols, line[index+1]) : #if the next symbol after the capital letter is a special symbol
                    lineCopy = self.insertSpaceIntoStringAfterItemAtSomeIndex(lineCopy, index + modificationsMade)

            modificationsMade = len(lineCopy) - len(line)


        print(lineCopy)
        return lineCopy.split()

controller = TokenisationController()
controller.tokenise('he')

class TestTokeniser(unittest.TestCase):

    global tokenisator
    tokenisator = TokenisationController()

    def testCheckItemsAreNotDigits(self):
        self.assertTrue(tokenisator.bothItemsAreNotDigits('a', 'b'))
        self.assertFalse(tokenisator.bothItemsAreNotDigits('a', '1'))
        self.assertFalse(tokenisator.bothItemsAreNotDigits('2', '1'))

    def testInsertSpaceIntoStringAfterSomeIndex(self):
        self.assertEqual(tokenisator.insertSpaceIntoStringAfterItemAtSomeIndex("hello", 0), "h ello")
        self.assertEqual(tokenisator.insertSpaceIntoStringAfterItemAtSomeIndex("hello", 1), "he llo")
        self.assertEqual(tokenisator.insertSpaceIntoStringAfterItemAtSomeIndex("hello", 2), "hel lo")
        self.assertEqual(tokenisator.insertSpaceIntoStringAfterItemAtSomeIndex("hello", 10), "hello ")

    def testTokenisation(self):
        self.assertEqual(tokenisator.tokenise("..."), '. . . '.split())
        self.assertEqual(tokenisator.tokenise("Hello world."), 'Hello world .'.split())
        self.assertEqual(tokenisator.tokenise("J. Smith said that..."), 'J . Smith said that . . . '.split())
        self.assertEqual(tokenisator.tokenise("O'Neill"), 'O \' Neill'.split())
        self.assertEqual(tokenisator.tokenise("Ivan's"), 'Ivan(p)'.split())
        self.assertEqual(tokenisator.tokenise("Jones\'"), 'Jones(p)'.split())
        self.assertEqual(tokenisator.tokenise("symbols (characters or word or phrases)."), 'symbols ( characters or word or phrases ) .'.split())
        self.assertEqual(tokenisator.tokenise("up-to-date"), 'up-to-date'.split())
        self.assertEqual(tokenisator.tokenise("New-York based"), 'New-York based'.split())
        self.assertEqual(tokenisator.tokenise("doesn't"), 'does not'.split())
        self.assertEqual(tokenisator.tokenise("don't"), 'do not'.split())
        self.assertEqual(tokenisator.tokenise("Vanya's doesn't"), 'Vanya(p) does not'.split())
        self.assertEqual(tokenisator.tokenise("Hey- you"), 'Hey - you'.split())
        self.assertEqual(tokenisator.tokenise("can't"), 'cannot'.split())


suite = unittest.TestLoader().loadTestsFromTestCase(TestTokeniser)
unittest.TextTestRunner().run(suite)
