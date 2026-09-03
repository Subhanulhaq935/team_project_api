from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


# Schema for updating profile (role, is_active, created_at excluded hain taake normal user inko change na kar sake)
class UserUpdate(BaseModel):
    firstname: str | None = None
    lastname: str | None = None


# Schema for returning user profile (Safe response)
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    firstname: str
    lastname: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime
