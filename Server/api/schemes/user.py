from pydantic import BaseModel, Field

from ..db.models import USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH

PASSWORD_MIN_LENGTH = 5
PASSWORD_MAX_LENGTH = 16


class _UserBase(BaseModel):
    username: str = Field(min_length=USERNAME_MIN_LENGTH, max_length=USERNAME_MAX_LENGTH)


class UserIn(_UserBase):
    password: str = Field(min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_LENGTH)

    class Config:
        schema_extra = {
            'example': {
                'username': 'bjarne_s',
                'password': 'ilovepython91'
            }
        }


class UserOut(_UserBase):
    id: int

    class Config:
        schema_extra = {
            'example': {
                'username': 'AndersH.',
                'id': 42
            }
        }

        orm_mode = True


class UserFromToken(UserOut):
    role: str


class UserInternal(UserFromToken):
    pw_hash: str
