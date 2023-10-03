import unittest
from typing import Dict, List

from src.simple_nlp_library.embeddings import model, vectors_average, tokens_vector
from src.simple_nlp_library.metrics import cosine_similarity
from src.simple_nlp_library.preprocessing import semantic_tokens


class TestEmbeddings(unittest.TestCase):
    vectors: Dict[str, List[float]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.vectors = model()

    def test_vectors(self) -> None:
        self.assertEqual(
            self.vectors.get("facebook"),
            [
                0.50248,
                0.10375,
                1.6825,
                0.60564,
                0.080408,
                -0.096378,
                -1.3325,
                -1.0853,
                0.27789,
                0.61109,
                -0.23044,
                -0.25419,
                -0.41496,
                -0.66857,
                0.90437,
                0.070662,
                -0.99646,
                -0.23861,
                1.076,
                0.019238,
                0.54294,
                0.11509,
                -0.044859,
                1.0704,
                0.6394,
                -0.25886,
                0.30337,
                -0.67565,
                -0.53396,
                -0.59785,
                1.6814,
                -0.00598,
                -0.12614,
                -0.82862,
                -1.2254,
                -0.13355,
                -0.074345,
                -0.67755,
                -0.89556,
                -0.8341,
                1.0422,
                -0.70266,
                -1.4604,
                0.76414,
                0.52434,
                -0.87978,
                0.12579,
                -0.1819,
                0.1785,
                -0.10107,
            ],
        )

    def test_similarity(self) -> None:
        self.assertAlmostEqual(cosine_similarity(self.vectors["facebook"], self.vectors["twitter"]), 0.93, 2)

    def test_vectors_average(self) -> None:
        self.assertEqual(vectors_average([[1.0] * 50, [2.0] * 50, [3.0] * 50]), [2.0] * 50)

    def test_tokens_vector(self) -> None:
        self.assertEqual(
            cosine_similarity(
                tokens_vector(self.vectors, semantic_tokens("Facebook is a")),
                self.vectors["facebook"],
            ),
            1.0,
        )

    def test_tokens_similarity(self) -> None:
        self.assertAlmostEqual(
            cosine_similarity(
                tokens_vector(self.vectors, semantic_tokens("the slow brown bear jumped over the lazy dog")),
                tokens_vector(self.vectors, semantic_tokens("the quick red fox jumped over the lazy cat")),
            ),
            0.95,
            2,
        )
