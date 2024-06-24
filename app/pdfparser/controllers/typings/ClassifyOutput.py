from pydantic import BaseModel

class ClassifyOutput(BaseModel):
    cv_class: str
    cv_class_prob: str
    cv_level: str
    cv_level_prob: str