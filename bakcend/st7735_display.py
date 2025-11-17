import time
import board
import digitalio
from adafruit_rgb_display import st7735
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from database import SessionLocal, WeatherData

class ST7735Display:
    def __init__(self):
        try:
            cs_pin = digitalio.DigitalInOut(board.CE0)
            dc_pin = digitalio.DigitalInOut(board.D25)
            reset_pin = digitalio.DigitalInOut(board.D24)

            spi = board.SPI()
            self.display = st7735.ST7735R(
                spi,
                cs=cs_pin,
                dc=dc_pin,
                rst=reset_pin,
                width=128,
                height=160,
                rotation=90,
                baudrate=24000000
            )
            
            if self.display.rotation in (90, 270):
                self.width = self.display.height   # 160
                self.height = self.display.width   # 128
            else:
                self.width = self.display.width
                self.height = self.display.height

            self.font = ImageFont.load_default()
            
            print(f"Display initialized: {self.width}x{self.height}")

            self._show_welcome_screen()
            
        except Exception as e:
            print(f"Error initializing display: {e}")
            raise
    
    def _show_welcome_screen(self):
        image = Image.new("RGB", (self.width, self.height), "#001a33")
        draw = ImageDraw.Draw(image)
        
        draw.text((40, 40), "Weather Station", font=self.font, fill="#FFFFFF")
        draw.text((45, 60), "Starting...", font=self.font, fill="#00FF00")
        
        self.display.image(image)
        time.sleep(2)
    
    def get_latest_weather_data(self):
        db = SessionLocal()
        try:
            latest_record = db.query(WeatherData)\
                .order_by(WeatherData.timestamp.desc())\
                .first()
            
            if latest_record:
                return {
                    'temperature': latest_record.temperature,
                    'humidity': latest_record.humidity,
                    'pressure': latest_record.pressure,
                    'timestamp': latest_record.timestamp
                }
            return None
            
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
        finally:
            db.close()
    
    def display_weather_data(self, data):
        if data is None:
            self._show_no_data_screen()
            return

        image = Image.new("RGB", (self.width, self.height), "#000000")
        draw = ImageDraw.Draw(image)

        for y in range(self.height):
            color_value = int(30 + (y / self.height) * 20)
            draw.rectangle([(0, y), (self.width, y+1)], fill=(0, color_value, color_value * 2))

        timestamp_str = data['timestamp'].strftime('%H:%M:%S')
        draw.text((5, 5), f"Updated: {timestamp_str}", font=self.font, fill="#FFFFFF")

        draw.line([(5, 20), (self.width - 5, 20)], fill="#FFFFFF", width=1)

        temp_color = self._get_temperature_color(data['temperature'])
        draw.text((10, 30), "Temperature:", font=self.font, fill="#FFFFFF")
        draw.text((10, 45), f"{data['temperature']:.1f} C", font=self.font, fill=temp_color)

        hum_color = self._get_humidity_color(data['humidity'])
        draw.text((10, 65), "Humidity:", font=self.font, fill="#FFFFFF")
        draw.text((10, 80), f"{data['humidity']:.1f} %", font=self.font, fill=hum_color)

        draw.text((10, 100), "Pressure:", font=self.font, fill="#FFFFFF")
        draw.text((10, 115), f"{data['pressure']:.1f} hPa", font=self.font, fill="#95E1D3")
        
        self.display.image(image)
    
    def _show_no_data_screen(self):
        image = Image.new("RGB", (self.width, self.height), "#330000")
        draw = ImageDraw.Draw(image)
        
        draw.text((40, 50), "No data", font=self.font, fill="#FF0000")
        draw.text((25, 70), "Waiting for sensor...", font=self.font, fill="#FFFFFF")
        
        self.display.image(image)
    
    def _get_temperature_color(self, temp):
        """Kolor na podstawie temperatury"""
        if temp < 0:
            return "#00BFFF"  # Niebieski (zimno)
        elif temp < 15:
            return "#4ECDC4"  # Cyjan (chłodno)
        elif temp < 25:
            return "#00FF00"  # Zielony (przyjemnie)
        elif temp < 30:
            return "#FFA500"  # Pomarańczowy (ciepło)
        else:
            return "#FF0000"  # Czerwony (gorąco)
    
    def _get_humidity_color(self, humidity):
        """Kolor na podstawie wilgotności"""
        if humidity < 30:
            return "#FFD700"  # Złoty (sucho)
        elif humidity < 60:
            return "#00FF00"  # Zielony (dobrze)
        else:
            return "#1E90FF"  # Niebieski (wilgotno)
    
    def clear_display(self):
        image = Image.new("RGB", (self.width, self.height), "#000000")
        self.display.image(image)


def main(stop_event=None):
    print("Display service started...")
    
    try:
        display_service = ST7735Display()
        
        while True:
            if stop_event and stop_event.is_set():
                print("Stopping display service...")
                display_service.clear_display()
                break

            data = display_service.get_latest_weather_data()
            display_service.display_weather_data(data)

            time.sleep(60)
            
    except KeyboardInterrupt:
        print("\nDisplay service stopped by user.")
        display_service.clear_display()
    except Exception as e:
        print(f"Error in display service: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()