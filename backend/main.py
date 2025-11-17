import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import threading
from contextlib import asynccontextmanager
from services.weather_service import WeatherService
from dto.weather_dto import WeatherDTO
from repositories.weather_repo import WeatherRepository
from database import SessionLocal

bme280_thread = None
st7735_thread = None
stop_event = threading.Event()

def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()

def bme280_background_task():
    try:
        import bme280_read
        print ("bme280_read module imported successfully.")
        
        bme280_read.main(stop_event)
    except Exception as error:
        print(f"Error in bme280_background_task: {error}")
        import traceback
        traceback.print_exc()

def st7735_background_task():
    try:
        import st7735_display
        print ("st7735_display module imported successfully.")
        
        st7735_display.main(stop_event)
    except Exception as error:
        print(f"Error in st7735_background_task: {error}")
        import traceback
        traceback.print_exc()

@asynccontextmanager
async def lifespan(app: FastAPI):
    global bme280_thread, st7735_thread
    
    print("\nStarting Weather Station")
    stop_event.clear()
    
    print("Starting BME280 sensor thread...")
    bme280_thread = threading.Thread(target=bme280_background_task, daemon=True)
    bme280_thread.start()
    print(f"BME280 thread started: {bme280_thread.is_alive()}")
    
    print("Starting display thread...")
    st7735_thread = threading.Thread(target=st7735_background_task, daemon=True)
    st7735_thread.start()
    print(f"Display thread started: {st7735_thread.is_alive()}")
    
    print("Weather Station Ready\n")
    
    yield
    
    print("\nStopping Weather Station")
    stop_event.set()
    
    if bme280_thread:
        bme280_thread.join(timeout=5)
        print("BME280 thread stopped.")
    
    if st7735_thread:
        st7735_thread.join(timeout=5)
        print("Display thread stopped.")
    
    print("Weather Station Stopped\n")

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
    
@app.get("/", response_model=WeatherDTO)
async def get_weather_data(db=Depends(get_db)):
    weather_repo = WeatherRepository(db_session=db)
    weather_service = WeatherService(weather_repo=weather_repo)
    response = weather_service.get_data_from_bme280()
    return response

@app.get("/history", response_model=list[WeatherDTO])
async def get_weather_history(db=Depends(get_db)):
    weather_repo = WeatherRepository(db_session=db)
    weather_service = WeatherService(weather_repo=weather_repo)
    response = weather_service.get_weather_history()
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)