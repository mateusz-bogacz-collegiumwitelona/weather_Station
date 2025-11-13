import bme280
import smbus2
from time import sleep
from datetime import datetime
from database import SessionLocal, WeatherData 

# bme280 setup
port = 1
address = 0x76 
bus = smbus2.SMBus(port)
bme280.load_calibration_params(bus,address)

def save_data_to_db(temp, hum, press):
    db = SessionLocal()
    
    try:
        reading = WeatherData(
            temperature=round(temp, 2),
            humidity=round(hum, 2),
            pressure=round(press, 2),
        )
        
        db.add(reading)
        db.commit()
        print(f"Save to DB: {reading.timestamp}")   
    except Exception as error:
        print(f"Error saving to DB: {error}")
    finally:
        db.close()    

def main(stop_event=None):
    print("Station started...\n")
    print("Readings every 60 seconds...\n")
    
    while True:
        if stop_event and stop_event.is_set():
            print("\nStopping background task...")
            break
        
        try:
            bmp280_data = bme280.sample(bus,address)
            humidity  = bmp280_data.humidity
            pressure  = bmp280_data.pressure
            ambient_temperature = bmp280_data.temperature
                
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            f"Temp: {ambient_temperature:.2f}°C | "
            f"Hum: {humidity:.2f}% | "
            f"Press: {pressure:.2f} hPa")
            
            save_data_to_db(ambient_temperature, humidity, pressure)
        
            sleep(60)
        except KeyboardInterrupt:
            print("\nStation stopped by user.")
            break
        except Exception as error:
            print(f"Error during reading or saving data: {error}")
            sleep(60)

if __name__ == "__main__":
    main()
        