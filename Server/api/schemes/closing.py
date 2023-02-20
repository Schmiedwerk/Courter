from pydantic import BaseModel
import datetime

_TODAY = datetime.datetime.now().date()


class ClosingIn(BaseModel):
    date: datetime.date
    start_timeslot_id: int
    end_timeslot_id: int
    court_id: int

    class Config:
        schema_extra = {
            'example': {
                'date': _TODAY + datetime.timedelta(days=10),
                'start_timeslot_id': 2,
                'end_timeslot_id': 5,
                'court_id': 1
            }
        }


class ClosingOut(ClosingIn):
    id: int

    class Config:
        schema_extra = {
            'example': {
                'date': _TODAY + datetime.timedelta(days=21),
                'start_timeslot_id': 1,
                'end_timeslot_id': 6,
                'court_id': 4,
                'id': 23
            }
        }

        orm_mode = True
