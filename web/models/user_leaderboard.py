from pydantic import BaseModel

class UserLeaderboard(BaseModel):
    uuid: str
    win: int
    lose_draw: int
