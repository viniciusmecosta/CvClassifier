from pydantic import BaseModel

class ClassifyCvOutput(BaseModel):
    cv_class: str
    cv_prob: str