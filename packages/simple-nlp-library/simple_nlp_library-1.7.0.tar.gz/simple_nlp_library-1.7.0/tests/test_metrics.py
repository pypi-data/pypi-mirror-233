import unittest

from src.simple_nlp_library.metrics import (
    dot_product,
    frobenius_norm,
    cosine_similarity,
    inserting_distance,
    inserting_similarity,
    jaccard_similarity,
)


class TestMetrics(unittest.TestCase):
    def test_dot_product(self) -> None:
        self.assertEqual(dot_product([1.0, 2.0, 3.0], [4.0, 5.0, 6.0]), 32)

    def test_frobenius_norm(self) -> None:
        self.assertEqual(frobenius_norm([1.0, 1.0, 1.0, 2.0, 3.0]), 4.0)

    def test_cosine_similarity(self) -> None:
        self.assertAlmostEqual(cosine_similarity([1.0, 1.0, 1.0], [4.0, 4.0, 4.0]), 1.0, 1)

    def test_inserting_distance(self) -> None:
        self.assertEqual(inserting_distance("simple", "simple"), 0)
        self.assertEqual(inserting_distance("simple", "simpler"), 1)
        self.assertEqual(inserting_distance("easy", "hard"), 4)

    def test_inserting_distance_backward(self) -> None:
        self.assertEqual(inserting_distance("simple", "simple", True), 0)
        self.assertEqual(inserting_distance("best", "the best", True), 4)
        self.assertEqual(inserting_distance("easy", "hard", True), 4)

    def test_inserting_similarity(self) -> None:
        self.assertEqual(inserting_similarity("simple", "simple"), 1.0)
        self.assertEqual(inserting_similarity("simple", "simpler"), 1.0 - 1 / 7)
        self.assertEqual(inserting_similarity("easy", "hard"), 0.0)

    def test_inserting_similarity_backward(self) -> None:
        self.assertEqual(inserting_similarity("simple", "simple", True), 1.0)
        self.assertEqual(inserting_similarity("best", "the best", True), 0.5)
        self.assertEqual(inserting_similarity("easy", "hard", True), 0.0)

    def test_jaccard_similarity(self) -> None:
        self.assertEqual(jaccard_similarity([1, 2, 3], [1, 2, 3]), 1.0)
        self.assertEqual(jaccard_similarity([1, 2], [1, 2, 3]), 2 / 3)
        self.assertEqual(jaccard_similarity([1, 2, 4], [1, 2, 3]), 0.5)
        self.assertEqual(jaccard_similarity([1, 2, 3], [1, 2, 3, 4]), 0.75)
