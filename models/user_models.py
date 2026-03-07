from pydantic import BaseModel, Field

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class LoginRequest(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    username: str
    role_id: int
    
    @classmethod
    def from_query_result(cls, id, username, role_id):
        return cls(
            id = id,
            username = username,
            role_id = role_id 
        )