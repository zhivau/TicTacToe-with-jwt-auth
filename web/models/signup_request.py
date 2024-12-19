from pydantic import BaseModel, Field


class SignUpRequest(BaseModel):
    login: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1)
