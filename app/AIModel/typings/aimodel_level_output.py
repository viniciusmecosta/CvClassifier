from pydantic import BaseModel

class AiModelLevelOutput(BaseModel):
    cvv_level: int
    cvv_level_prob: str