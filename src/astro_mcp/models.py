from pydantic import BaseModel


class BirthData(BaseModel):
    year: int
    month: int
    day: int

    hour: int
    minute: int

    latitude: float
    longitude: float

    timezone: str = "UTC"
