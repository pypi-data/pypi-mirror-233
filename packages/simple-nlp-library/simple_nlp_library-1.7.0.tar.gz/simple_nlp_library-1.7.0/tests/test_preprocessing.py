import unittest

from src.simple_nlp_library.preprocessing import (
    single_spaces,
    lower_letters,
    non_stopword_tokens,
    semantic_tokens,
    non_social,
)


class TestPreprocessing(unittest.TestCase):
    def test_single_spaces(self) -> None:
        self.assertEqual(
            single_spaces("The  quick \t brown \n fox jumps"),
            "The quick brown fox jumps",
        )

    def test_lower_letters(self) -> None:
        self.assertEqual(
            lower_letters("The quick brown fox jumps-over!"),
            "the quick brown fox jumps over",
        )

    def test_non_stopword_tokens(self) -> None:
        self.assertEqual(
            non_stopword_tokens(["the", "quick", "brown", "fox", "jumps"]),
            ["quick", "brown", "fox", "jumps"],
        )

    def test_non_social(self) -> None:
        self.assertEqual(
            non_social(["quick", "brown", "fox", "jumps", "@user", "https://domain.com"]),
            ["quick", "brown", "fox", "jumps"],
        )

    def test_semantic_tokens(self) -> None:
        self.assertEqual(
            semantic_tokens("The 2 quick \t brown foxes jumps, over the lazy dog! @user"),
            ["2", "quick", "brown", "foxes", "jumps", "lazy", "dog"],
        )
