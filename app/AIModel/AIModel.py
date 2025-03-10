import joblib
import logging
import numpy as np
import os
from dotenv import load_dotenv
from textblob import TextBlob
from app.AIModel.typings.aimodel_class_output import AiModelClassOutput
from app.AIModel.typings.aimodel_level_output import AiModelLevelOutput

load_dotenv()

dir_path = os.path.dirname(os.path.realpath(__file__))

class_model = os.getenv('CLASS_MODEL')
class_vector = os.getenv('CLASS_VECTOR')
level_model = os.getenv('LEVEL_MODEL')
level_vector = os.getenv('LEVEL_VECTOR')
if None in [class_model, class_vector, level_model, level_vector]:
    raise ValueError("Error: invalid .env")

class AIModel:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.class_model = self._load_model(f"{dir_path}/domain/{class_model}")
        self.class_vectorizer = self._load_model(f"{dir_path}/domain/{class_vector}")
        self.level_model = self._load_model(f"{dir_path}/domain/{level_model}")
        self.level_vectorizer = self._load_model(f"{dir_path}/domain/{level_vector}")

    def _load_model(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Error: Models not found -> {path}")
        return joblib.load(path)

    def parseCvvClass(self, text: str) -> AiModelClassOutput:
        self.logger.info('Parsing CVV...')
        processed_text = self._remove_stopwords_and_lemmatize(text)
        self.logger.info('Processed content')
        predicted_class = self._classify_class(processed_text)
        self.logger.info('Classified successfully')
        return predicted_class
    
    def parseCvvLevel(self, text: str) -> AiModelLevelOutput:
        self.logger.info('Parsing CVV...')
        processed_text = self._remove_stopwords_and_lemmatize(text)
        self.logger.info('Processed content')
        predicted_class = self._classify_level(processed_text)
        self.logger.info('Classified successfully')
        return predicted_class

    def _remove_stopwords_and_lemmatize(self, text: str) -> str:
        blob = TextBlob(text.lower())
        lemmatized_words = [word.lemmatize() for word in blob.words if word.isalnum()]
        return ' '.join(lemmatized_words)
    
    def _classify_class(self, text) -> AiModelClassOutput:
        X = np.array([text])
        X_vec = self.class_vectorizer.transform(X)
        predicted_class = self.class_model.predict_proba(X_vec)
        top_class = np.argsort(predicted_class[0])[::-1][0]
        probability = predicted_class[0][top_class] * 100        
        result = AiModelClassOutput(**{
            "cv_class": top_class,
            "cv_prob": str(probability)
        })
        return result
    
    def _classify_level(self, text) -> AiModelLevelOutput:
        X = np.array([text])
        X_vec = self.level_vectorizer.transform(X)
        predicted_class = self.level_model.predict_proba(X_vec)
        top_class = np.argsort(predicted_class[0])[::-1][0]
        probability = predicted_class[0][top_class] * 100        
        result = AiModelLevelOutput(**{
            "cvv_level": top_class,
            "cvv_level_prob": str(probability)
        })
        return result

aiModel = AIModel()