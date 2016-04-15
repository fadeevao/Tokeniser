import unittest
from main.src.tokeniser import TokenisationController

class TestTokeniser(unittest.TestCase):

    global tokenisator
    tokenisator = TokenisationController()

    def test_check_items_are_not_digits(self):
        digits = r'\d'
        self.assertFalse(tokenisator.consecutive_characters_are_following_the_pattern('a', 'b', digits))
        self.assertFalse(tokenisator.consecutive_characters_are_following_the_pattern('a', '1', digits))
        self.assertTrue(tokenisator.consecutive_characters_are_following_the_pattern('2', '1', digits))

    def test_insert_space_into_string_after_some_index(self):
        self.assertEqual(tokenisator.insert_space_after_item_at_some_index("hello", 0), "h ello")
        self.assertEqual(tokenisator.insert_space_after_item_at_some_index("hello", 1), "he llo")
        self.assertEqual(tokenisator.insert_space_after_item_at_some_index("hello", 2), "hel lo")
        self.assertEqual(tokenisator.insert_space_after_item_at_some_index("hello", 10), "hello ")

    def test_tokenisation(self):
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
        self.assertEqual(tokenisator.tokenise("U.K."), 'U.K.'.split())
        self.assertEqual(tokenisator.tokenise("U.S.A."), 'U.S.A.'.split())

# suite = unittest.TestLoader().loadTestsFromTestCase(TestTokeniser)
# unittest.TextTestRunner().run(suite)
