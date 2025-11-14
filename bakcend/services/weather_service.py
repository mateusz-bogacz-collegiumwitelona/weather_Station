from dto.weather_dto import WeatherDTO
 
class WeatherService:
    def __init__(self, weather_repo):
        self.weather_repo = weather_repo

    def get_data_from_bme280(self) -> WeatherDTO:
        try:
            response = self.weather_repo.get_data_from_bme280()

            if response is None:
                raise Exception("No data received from BME280 sensor")
            
            isSaved = self.weather_repo.save_weather_data(response)
            
            if not isSaved:
                raise Exception("Failed to save weather data to the database")
            
            return response
        
        except Exception as error:
            raise Exception(f"Error getting data from BME280 sensor: {error}")
        
    def get_weather_history(self) -> list[WeatherDTO]:
        try: 
            response = self.weather_repo.get_weather_history()
            
            if response is None:
                raise Exception("No weather history data found")
            
            return response
        
        except Exception as error:
            raise Exception(f"Error retrieving weather history: {error}")