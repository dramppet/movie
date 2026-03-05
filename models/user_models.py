from pydantic import BaseModel, Field

class UserBase(BaseModel):
    username: str = Field(..., min_length=3)


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    role_id: int