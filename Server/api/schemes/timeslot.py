from pydantic import BaseModel, Field
from datetime import time


class TimeslotIn(BaseModel):
    start: time
    end: time

    class Config:
        schema_extra = {
            'example': {
                'start': '09:00',
                'end': '10:30'
            }
        }


class TimeslotOut(TimeslotIn):
    id: int

    class Config:
        schema_extra = {
            'example': {
                'start': '12:00',
                'end': '13:00',
                'id': 8
            }
        }