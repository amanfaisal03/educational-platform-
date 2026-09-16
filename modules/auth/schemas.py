from pydantic import BaseModel, ConfigDict


class StudentRegistrationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    role: str


class TokenData(BaseModel):
    user_id: int





