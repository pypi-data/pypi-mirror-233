import unittest

from src.simple_nlp_library.preprocessing import (
    semantic_tokens,
)


class TestPreprocessing(unittest.TestCase):
    def test_no_hyphens_and_underscores(self) -> None:
        self.assertEqual(semantic_tokens("state-of-the-art uncased_model"), ["state", "art", "uncased", "model"])

    def test_lower_letters(self) -> None:
        self.assertEqual(
            semantic_tokens("Quick brown fox jUMPs"),
            ["quick", "brown", "fox", "jumps"],
        )

    def test_single_spaces(self) -> None:
        self.assertEqual(
            semantic_tokens("quick \t brown \n fox jumps"),
            ["quick", "brown", "fox", "jumps"],
        )

    def test_non_stopword_tokens(self) -> None:
        self.assertEqual(
            semantic_tokens("The quick brown fox jumps over"),
            ["quick", "brown", "fox", "jumps"],
        )

    def test_non_social(self) -> None:
        self.assertEqual(
            semantic_tokens("quick brown fox jumps over @user https://domain.com"),
            ["quick", "brown", "fox", "jumps"],
        )

    def test_semantic_tokens(self) -> None:
        self.assertEqual(
            semantic_tokens("The 2 quick \t brown foxes jumps, over the lazy dog! @user"),
            ["2", "quick", "brown", "foxes", "jumps", "lazy", "dog"],
        )

    def test_semantic_text(self) -> None:
        self.assertEqual(
            " ".join(
                semantic_tokens(
                    """
                    <br> <a href="https://google.com">Google It</a> to find an answer, 
                    this is state-of-the-art uncased_model,
                    email me quick_fox@gmail.com or visit my website http://quick-fox.com https://quick-fox.com
                    Value of PI: 3.14 it is less than 4,
                    line<br>break
                    """
                )
            ),
            "google find answer state art uncased model email visit website value pi 314 less 4 line break",
        )
