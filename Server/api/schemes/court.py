from pydantic import BaseModel, Field
from typing import Optional


NAME_MIN_LENGTH = 2
NAME_MAX_LENGTH = 32
SURFACE_MIN_LENGTH = 1
SURFACE_MAX_LENGTH = 16


class CourtIn(BaseModel):
    name: str = Field(min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH)
    surface: Optional[str] = Field(min_length=SURFACE_MIN_LENGTH, max_length=SURFACE_MAX_LENGTH)

    class Config:
        schema_extra = {
            'example': {
                'name': 'Wimbledon Centre Court',
                'surface': 'grass'
            }
        }


class CourtOut(CourtIn):
    id: int

    class Config:
        schema_extra = {
            'example': {
                'name': 'Arthur Ashe Stadium',
                'surface': 'hard',
                'id': 5
            }
        }

        orm_mode = True
