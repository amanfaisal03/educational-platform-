from pydantic import BaseModel, ConfigDict


class StudentRegistrationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    email : str
    password : str

class LoginRequest(BaseModel):
     email: str
     password: str
