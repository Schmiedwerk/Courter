from pydantic import BaseModel, Field
from typing import Optional
from ..db.models import Court


class CourtIn(BaseModel):
    name: str = Field(min_length=Court.NAME_MIN_LENGTH, max_length=Court.NAME_MAX_LENGTH)
    surface: Optional[str] = Field(min_length=Court.SURFACE_MIN_LENGTH, max_length=Court.SURFACE_MAX_LENGTH)

    class Config:
        schema_extra = {
            'example': {
                'name': 'Wimbledon Centre',
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
