import nltk
import pymorphy2
import string
from nltk.tokenize import WordPunctTokenizer

nltk.download('stopwords')
from nltk.corpus import stopwords


class RawTextHandler:
    spec_chars = string.punctuation + '\n\xa0«»\t—…'

    @staticmethod
    def remove_chars_from_text(text, is_forbidden):
        return "".join([char for char in text if not is_forbidden(char)])

    def prepare_raw_text(self, text):
        clean_text = self.remove_chars_from_text(text, lambda x: x in self.spec_chars)
        clean_text = self.remove_chars_from_text(clean_text, lambda x: x.isnumeric())
        return clean_text.lower()


class TextHandler:
    russian_stopwords = stopwords.words("russian")

    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()
        self.tokenizer = WordPunctTokenizer()
        self.raw_text_handler = RawTextHandler()

    def tokenize_text(self, text):
        return self.tokenizer.tokenize(text)

    @staticmethod
    def remove_forbidden_tokens(tokens, forbidden_tokens):
        return [token for token in tokens if token not in forbidden_tokens and len(token) > 2]

    def lemmatize_text(self, tokens):
        return [self.morph.parse(word)[0].normal_form for word in tokens]

    def process_text(self, text):
        prepared_text = self.raw_text_handler.prepare_raw_text(text)
        tokenized_text = self.tokenize_text(prepared_text)
        text_with_required_tokens = self.remove_forbidden_tokens(tokenized_text, self.russian_stopwords)
        lemmatized_text = self.lemmatize_text(text_with_required_tokens)
        return lemmatized_text
