import spacy
import joblib
import logging
import numpy as np
import os 
from app.AIModel.typings.aimodel_class_output import AiModelClassOutput
from app.AIModel.typings.aimodel_level_output import AiModelLevelOutput

dir_path = os.path.dirname(os.path.realpath(__file__))

class_model=os.getenv('CLASS_MODEL')
class_vector=os.getenv('CLASS_VECTOR')
level_model=os.getenv('LEVEL_MODEL')
level_vector=os.getenv('LEVEL_VECTOR')

class AIModel:
    def __init__(self) -> None:
        self.nlp = spacy.load("en_core_web_lg")
        self.class_model = joblib.load(f"{dir_path}/domain/{class_model}")
        self.class_vectorizer = joblib.load(f"{dir_path}/domain/{class_vector}")
        self.level_model = joblib.load(f"{dir_path}/domain/{level_model}")
        self.level_vectorizer = joblib.load(f"{dir_path}/domain/{level_vector}")
        self.logger = logging.getLogger(__name__)

    def parseCvvClass(self, text: str) -> AiModelClassOutput:
        self.logger.info('Parsing CVV...')
        processed_text= self._remove_stopwords_and_lemmatize(text)
        self.logger.info('Processed content')
        predicted_class= self._classify_class(processed_text)
        self.logger.info('Classified successfully')
        return predicted_class
    
    def parseCvvLevel(self, text:str) -> AiModelLevelOutput:
        self.logger.info('Parsing CVV...')
        processed_text= self._remove_stopwords_and_lemmatize(text)
        self.logger.info('Processed content')
        predicted_class= self._classify_level(processed_text)
        self.logger.info('Classified successfully')
        return predicted_class
        
    def _remove_stopwords_and_lemmatize(self, text: str) -> str:
        cleaned_text = ' '.join(text.strip().split())
        doc = self.nlp(cleaned_text.lower())
        tokens_lemmatized = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
        return ' '.join(tokens_lemmatized)

    
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


aiModel= AIModel()