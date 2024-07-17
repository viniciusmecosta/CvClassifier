from pydantic import BaseModel

class AiModelClassOutput(BaseModel):
    cv_class: int
    cv_prob: str