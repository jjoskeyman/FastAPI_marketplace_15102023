from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str
    first_name: str
    email: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserCreate):
    pass


class UserUpdatePartial(UserCreate):
    username: str | None = None
    first_name: str | None = None
    email: str | None = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
