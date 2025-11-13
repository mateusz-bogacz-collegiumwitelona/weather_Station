import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import threading
from contextlib import asynccontextmanager
from services.weather_service import WeatherService
from dto.weather_dto import WeatherDTO
from repositories.weather_repo import WeatherRepository

background_thread = None
stop_event = threading.Event()

def bme280_background_task():
    try:
        import bme280_read
        print ("bme280_read module imported successfully.")
        
        bme280_read.main(stop_event)
    except Exception as error:
        print(f"Error in bme280_background_task: {error}")
        import traceback
        traceback.print_exc()

@asynccontextmanager
async def lifespan(app: FastAPI):
    global background_thread
    
    print("Starting background task...")
    stop_event.clear()
    background_thread = threading.Thread(target=bme280_background_task, daemon=True)
    background_thread.start()
    print(f"\nBackground task started: {background_thread.is_alive()}")
    
    yield
    
    print("\nStopping background task...")
    stop_event.set()
    if background_thread:
        background_thread.join(timeout=5)
        print("Background task stopped.")
    
app = FastAPI(
    title="Weather Station API", 
    version="v1",
    lifespan=lifespan
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

weather_repo = WeatherRepository(db_session=None)
weather_service = WeatherService(weather_repo=weather_repo)

@app.get("/")
def root():
    return {
        "message": "hello word"
    }
    
@app.get("/weather", response_model=WeatherDTO)
async def get_weather_data():
    response = weather_service.get_data_from_bme280()
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)