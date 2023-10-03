from typing import List, Any


def dot_product(a: List[float], b: List[float]) -> float:
    return sum([x1 * x2 for x1, x2 in zip(a, b)])


def frobenius_norm(a: List[float]) -> float:
    return sum([x * x for x in a]) ** 0.5


def cosine_similarity(a: List[float], b: List[float]) -> float:
    return dot_product(a, b) / (frobenius_norm(a) * frobenius_norm(b))


def inserting_distance(word1: str, word2: str, backward: bool = False) -> int:
    common_start = 0
    for i in range(min(len(word1), len(word2))):
        if (not backward and word1[i] == word2[i]) or (backward and word1[-i - 1] == word2[-i - 1]):
            common_start += 1
        else:
            break
    return max(len(word1), len(word2)) - common_start


def inserting_similarity(word1: str, word2: str, backward: bool = False) -> float:
    return 1.0 - (inserting_distance(word1, word2, backward) / max(len(word1), len(word2)))


def jaccard_similarity(a: List[Any], b: List[Any]) -> float:
    a_and_b = len(set(a).intersection(set(b)))
    return a_and_b / (len(a) + len(b) - a_and_b)
