from pydantic import BaseModel

class Play(BaseModel):
    play_id: str
    name: str
    type: str