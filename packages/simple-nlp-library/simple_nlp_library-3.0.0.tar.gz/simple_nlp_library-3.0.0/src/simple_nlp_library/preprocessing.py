import os
import re
from typing import List


def stop_words() -> List[str]:
    with open(os.path.join(os.path.dirname(__file__), "data/scikitlearn.txt"), "r", encoding="utf8") as file:
        return [line.rstrip() for line in file]


def semantic_tokens(stop_words: List[str], text: str) -> List[str]:
    text = text.lower()
    text = re.sub(r"<[^<]+?>", " ", text)
    text = re.sub(r"\S*@\S*", "", text)
    text = re.sub(r"\S*https?\S*", "", text)
    text = re.sub(r"[\-/]+", " ", text)
    text = re.sub(r"[^a-z0-9 ]+", "", text)
    return [word for word in text.split() if word not in dict.fromkeys(stop_words)]
