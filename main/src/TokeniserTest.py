import unittest
from main.src import tokeniser

class TestTokeniser(unittest.TestCase):

    global tokenisator
    tokenisator = tokenisator.TokenisationController()

    def testCheckItemsAreNotDigits(self):
        self.assertTrue(tokenisator.consecutive_characters_are_not_digits('a', 'b'))
        self.assertFalse(tokenisator.consecutive_characters_are_not_digits('a', '1'))
        self.assertFalse(tokenisator.consecutive_characters_are_not_digits('2', '1'))

    def testInsertSpaceIntoStringAfterSomeIndex(self):
        self.assertEqual(tokenisator.insert_space_after_item_at_some_index("hello", 0), "h ello")
        self.assertEqual(tokenisator.insert_space_after_item_at_some_index("hello", 1), "he llo")
        self.assertEqual(tokenisator.insert_space_after_item_at_some_index("hello", 2), "hel lo")
        self.assertEqual(tokenisator.insert_space_after_item_at_some_index("hello", 10), "hello ")

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