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

    def test_consecutive_characters_are_following_the_pattern(self):
        self.assertFalse(tokenisator.consecutive_characters_are_following_the_pattern("A", "B", r'\d'))
        self.assertFalse(tokenisator.consecutive_characters_are_following_the_pattern("A", "77", r'\d'))
        self.assertTrue(tokenisator.consecutive_characters_are_following_the_pattern("7.5", "5", r'\d'))
        self.assertTrue(tokenisator.consecutive_characters_are_following_the_pattern("75", "5", r'\d'))

    def test_hypnen_needs_spaces_around(self):
        self.assertFalse(tokenisator.hypnen_needs_spaces_around("up-to", 2))
        self.assertTrue(tokenisator.hypnen_needs_spaces_around("up- to", 2))

    def test_insert_identifier_at_index(self):
        self.assertEqual(tokenisator.insert_identifier_at_index("3", 0, "string", False), "3tring")
        self.assertEqual(tokenisator.insert_identifier_at_index("3", 0, "string", True), "3 tring")

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
        self.assertEqual(tokenisator.tokenise("I.O.U."), "I.O.U.".split())
        self.assertEqual(tokenisator.tokenise("5.55"), '5.55'.split())
        self.assertEqual(tokenisator.tokenise("142.32.48.231"), "142.32.48.231".split())
        self.assertEqual(tokenisator.tokenise("Hewlett-Packard"), "Hewlett-Packard".split())
