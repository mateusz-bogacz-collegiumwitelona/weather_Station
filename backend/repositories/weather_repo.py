import bme280
import smbus2
from time import sleep
from datetime import datetime
from dto.weather_dto import WeatherDTO
from database import WeatherData

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
            temperature=round(ambient_temperature, 2),
            humidity=round(humidity, 2),
            pressure=round(pressure, 2),
            timestamp=datetime.now()
        ) 
    
    def save_weather_data(self, weather_data: WeatherDTO) -> bool:
        try:
            weather_record = WeatherData(
                temperature=weather_data.temperature,
                humidity=weather_data.humidity,
                pressure=weather_data.pressure,
                timestamp=weather_data.timestamp
            )
            
            self.db_session.add(weather_record)
            self.db_session.commit()
            
            return True
        
        except Exception as error:
            self.db_session.rollback()
            print(f"Error saving weather data: {error}")
            return False
        
    def get_weather_history(self) -> list[WeatherDTO]:
        records = self.db_session.query(WeatherData) \
                    .order_by(WeatherData.timestamp.desc()).all()
        
        weather_history = [
            WeatherDTO(
                temperature=record.temperature,
                humidity=record.humidity,
                pressure=record.pressure,
                timestamp=record.timestamp
            ) for record in records
        ]    
        
        return weather_history