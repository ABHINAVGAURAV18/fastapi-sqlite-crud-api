from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(..., description="The name of the user")
    age: int = Field(..., gt=0, lt=150, description="The age of the user")


class UserResponse(BaseModel):
    user_id: int
    name: str
    age: int
