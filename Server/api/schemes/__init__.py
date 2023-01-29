from pydantic import BaseModel

from .user import UserIn, UserOut, UserFromToken, UserInternal


class AccessToken(BaseModel):
    access_token: str
    token_type: str