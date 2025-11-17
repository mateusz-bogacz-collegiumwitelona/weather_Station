import bme280
import smbus2
from time import sleep

port = 1
address = 0x76 
bus = smbus2.SMBus(port)

bme280.load_calibration_params(bus,address)

while True:
    bme280_data = bme280.sample(bus,address)
    humidity  = bme280_data.humidity
    pressure  = bme280_data.pressure
    ambient_temperature = bme280_data.temperature
    print(f"Temp: {ambient_temperature:.2f}°C | Hum: {humidity:.2f}% | Press: {pressure:.2f} hPa")
    sleep(1)