import bme280
import smbus2
from time import sleep
from datetime import datetime
from dto.weather_dto import WeatherDTO

# bme280 setup
port = 1
address = 0x76 
bus = smbus2.SMBus(port)
bme280.load_calibration_params(bus,address)

class WeatherRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_data_from_bme280(self) -> WeatherDTO:
        bme280_data = bme280.sample(bus,address)
        humidity  = bme280_data.humidity
        pressure  = bme280_data.pressure
        ambient_temperature = bme280_data.temperature
        
        return WeatherDTO(
            temperature=ambient_temperature,
            humidity=humidity,
            pressure=pressure,
            timestamp=datetime.utcnow()
        ) 