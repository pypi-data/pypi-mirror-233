import os

import joblib

from tjru_language_classifier.normalizer import Normalizer
from tjru_language_classifier.transliteration import transliterate


class LanguageClassifier:
    """Tajiki/Russian Language Classifier"""

    MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

    _data_dtype = {"text": str, "lang": str, "test": bool}

    _COLUMN_TEXT = "text"
    _COLUMN_TEST = "test"
    _COLUMN_LANG = "lang"

    def __init__(self):
        if os.path.exists(self.MODEL_PATH):
            self.model = joblib.load(self.MODEL_PATH)
        else:

            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.naive_bayes import MultinomialNB
            from sklearn.pipeline import make_pipeline

            self.model = make_pipeline(
                TfidfVectorizer(analyzer="char", ngram_range=(1, 5), min_df=5),
                MultinomialNB(fit_prior=False),
            )

        self.normalizer = Normalizer(
            lowercase=True,
            remove_digits=True,
            remove_punctuation=True,
            normalize_tajik=False,
            remove_extra_spaces=True,
            remove_stopwords=False,
        )

    def _load_data(self, data_path: str, test=False):
        import pandas as pd

        data = pd.read_csv(data_path, dtype=self._data_dtype)
        data = data.dropna()
        test = data[self._COLUMN_TEST] if test else ~data[self._COLUMN_TEST]
        data = data[test]
        return data
    
    def preprocess_texts(self, texts: "list[str]"):
        texts = [self.normalizer(t) for t in texts]
        texts = [transliterate(t) for t in texts]
        return texts

    def train(self, data_path: str):
        import pandas as pd

        data = self._load_data(data_path, test=False)
        texts = data[self._COLUMN_TEXT]
        # preprocess texts
        texts = self.preprocess_texts(texts)
        labels = data[self._COLUMN_LANG]
        self.model.fit(texts, labels)
        joblib.dump(self.model, self.MODEL_PATH)

    def test(self, data_path: str):
        from sklearn.metrics import accuracy_score
        data = self._load_data(data_path, test=True)
        texts = data[self._COLUMN_TEXT]
        # preprocess texts
        texts = self.preprocess_texts(texts)
        labels = data[self._COLUMN_LANG]
        predictions = self.model.predict(texts)
        accuracy = accuracy_score(labels, predictions)
        return accuracy

    def predict(self, input: "str|list[str]", return_probabilities: bool = False):
        """
        Predict the class labels or probabilities for the given input.

        Parameters:
        - input (str|list[str]): The input data for prediction. Can be a single string or a list of strings.
        - return_probabilities (bool, optional): If set to True, the function will return the probabilities
        of the classes instead of the class labels. Default is False.

        Returns:
        - If return_probabilities is False: Returns the predicted class label for a single string input, or
        a list of predicted class labels for a list input.
        - If return_probabilities is True: Returns the predicted class probabilities for a single string input,
        or a list of predicted class probabilities for a list input.
        """

        # Check if the input is a single string
        is_str = isinstance(input, str)
        if is_str:
            input = [input]

        # Normalize the input
        input = self.preprocess_texts(input)

        # Predict using the model
        if return_probabilities:
            prediction = self.model.predict_proba(input)
        else:
            prediction = self.model.predict(input)

        # Return the prediction
        return prediction[0] if is_str else prediction
