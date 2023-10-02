import itertools
import re


class Normalizer:
    def __init__(
        self,
        stopwords_file=None,
        lowercase=True,
        remove_punctuation=True,
        remove_digits=True,
        normalize_tajik=True,
        remove_stopwords=True,
        remove_extra_spaces=True,
    ):
        self.stopwords = (
            set(open(stopwords_file).read().split("\n")) if stopwords_file else None
        )
        self.lowercase = lowercase
        self.remove_punctuation_flag = remove_punctuation
        self.remove_digits_flag = remove_digits
        self.normalize_tajik_flag = normalize_tajik
        self.remove_stopwords_flag = remove_stopwords
        self.remove_extra_spaces_flag = remove_extra_spaces

    @staticmethod
    def remove_digits(string: str):
        return re.sub(r"\d", " ", string)

    @staticmethod
    def remove_extra_spaces(text: str):
        return " ".join(text.split())

    @staticmethod
    def normalize_tajik(text: str):
        return text.translate(str.maketrans("ҷқӯғҳӣъщыэ", "чкугхиьшие"))

    @staticmethod
    def remove_consecutive_duplicates(s: str):
        return "".join(key for key, group in itertools.groupby(s))

    @staticmethod
    def remove_punctuation(s: str):
        return re.sub(r"[^\w\s]", " ", s)

    def remove_stopwords(self, s: str):
        return " ".join((w for w in s.split() if w not in self.stopwords))

    def normalize_text(self, text: str):
        if self.lowercase:
            text = text.lower()
        if self.remove_punctuation_flag:
            text = self.remove_punctuation(text)
        if self.remove_digits_flag:
            text = self.remove_digits(text)
        if self.normalize_tajik_flag:
            text = self.normalize_tajik(text)
        if self.remove_stopwords_flag:
            text = self.remove_stopwords(text)
        if self.remove_extra_spaces_flag:
            text = self.remove_extra_spaces(text)
        return text

    __call__ = normalize_text


if __name__ == "__main__":
    normalizer = Normalizer(
        lowercase=True,
        remove_punctuation=True,
        remove_digits=True,
        normalize_tajik=True,
        remove_stopwords=True,
        remove_extra_spaces=True,
    )
    text = "Навиштаи шумо инҷо бошад!"
    normalized_text = normalizer.normalize_text(text)

    print(normalized_text)
