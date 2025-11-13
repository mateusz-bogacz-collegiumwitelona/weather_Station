from dto.weather_dto import WeatherDTO
 
class WeatherService:
    def __init__(self, weather_repo):
        self.weather_repo = weather_repo

    def get_data_from_bme280(self) -> WeatherDTO:
        try:
            response = self.weather_repo.get_data_from_bme280()

            if response is None:
                raise Exception("No data received from BME280 sensor")
            
            return response
        
        except Exception as error:
            raise Exception(f"Error getting data from BME280 sensor: {error}")
        