import spacy
import joblib
import logging
import numpy as np
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

class AIModel:
    def __init__(self) -> None:
        self.nlp = spacy.load("en_core_web_lg")
        self.vectorizer = joblib.load(f"{dir_path}/domain/vector.pkl")
        self.model = joblib.load(f"{dir_path}/domain/model.pkl")
        self.logger = logging.getLogger(__name__)

    def parseCvv(self, text: str) -> int:
        self.logger.info('Parsing CVV...')
        processed_text= self._remove_stopwords_and_lemmatize(text)
        self.logger.info('Processed content')
        predicted_class= self._classify(processed_text)
        self.logger.info('Classified successfully')
        return predicted_class
        
    def _remove_stopwords_and_lemmatize(self, text: str) -> str:
        cleaned_text = ' '.join(text.strip().split())
        doc = self.nlp(cleaned_text.lower())
        tokens_lemmatized = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
        return ' '.join(tokens_lemmatized)

    
    def _classify(self, text) -> int:
        preprocessed_text = self._remove_stopwords_and_lemmatize(text)
        X = np.array([preprocessed_text])
        X_vec = self.vectorizer.transform(X)
        predicted_class = self.model.predict(X_vec)[0]
        return predicted_class.item()


aiModel= AIModel()