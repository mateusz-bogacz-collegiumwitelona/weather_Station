from pydantic import BaseModel
from datetime import datetime

class WeatherDTO(BaseModel):
    temperature: float
    humidity: float
    pressure: float
    timestamp: datetime