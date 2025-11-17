import time
import board
import digitalio
from adafruit_rgb_display import st7735
from PIL import Image, ImageDraw, ImageFont

print("ST7735 Display Test")

try:
    cs_pin = digitalio.DigitalInOut(board.CE0)
    dc_pin = digitalio.DigitalInOut(board.D25)
    reset_pin = digitalio.DigitalInOut(board.D24)
    
    spi = board.SPI()
    display = st7735.ST7735R(
        spi,
        cs=cs_pin,
        dc=dc_pin,
        rst=reset_pin,
        width=128,
        height=160,
        rotation=90,
        baudrate=24000000
    )

    print("Display initialized successfully.")
    print(f"Display native dimensions: {display.width}x{display.height}")
    print(f"Display rotation: {display.rotation}")
    

    if display.rotation in (90, 270):
        WIDTH = display.height 
        HEIGHT = display.width   
    else:
        WIDTH = display.width
        HEIGHT = display.height
    
    print(f"Actual image dimensions needed: {WIDTH}x{HEIGHT}")
    
    print("Test 1: black screen 2s")
    image = Image.new("RGB", (WIDTH, HEIGHT), "#000000")
    display.image(image)
    time.sleep(2)
    
    print("Test 2: red screen 2s")
    image = Image.new("RGB", (WIDTH, HEIGHT), "#FF0000")
    display.image(image)
    time.sleep(2)
    
    print("Test 3: green screen 2s")
    image = Image.new("RGB", (WIDTH, HEIGHT), "#00FF00")
    display.image(image)
    time.sleep(2)
    
    print("Test 4: blue screen 2s")
    image = Image.new("RGB", (WIDTH, HEIGHT), "#0000FF")
    display.image(image)
    time.sleep(2)
    
    print("Test 5: white screen 2s")
    image = Image.new("RGB", (WIDTH, HEIGHT), "#FFFFFF")
    display.image(image)
    time.sleep(2)
    
    print("Test 6: displaying text 5s")
    font = ImageFont.load_default()
    image = Image.new("RGB", (WIDTH, HEIGHT), "#000000")
    draw = ImageDraw.Draw(image)
    
    draw.text((10, 10), "ST7735 TEST", font=font, fill="#FFFFFF")
    draw.text((10, 30), "Works!", font=font, fill="#00FF00")
    draw.text((10, 50), "Temperature: 23.5C", font=font, fill="#FF6B6B")
    draw.text((10, 70), "Humidity: 45%", font=font, fill="#4ECDC4")
    draw.text((10, 90), "Pressure: 1013hPa", font=font, fill="#95E1D3")
    
    display.image(image)
    print("Text displayed. Test complete.")
    time.sleep(5)
    
    print("Test 7: Animations 10s")
    for i in range(0, WIDTH + 1, 10):
        image = Image.new("RGB", (WIDTH, HEIGHT), "#000000")
        draw = ImageDraw.Draw(image)

        bar_width = WIDTH - 20
        draw.rectangle([(10, 50), (WIDTH - 10, 70)], outline="#FFFFFF")
        bar_progress = int(10 + (i / WIDTH) * bar_width)
        draw.rectangle([(10, 50), (bar_progress, 70)], fill="#00FF00")

        percent = int((i / WIDTH) * 100)
        text_x = WIDTH // 2 - 15
        draw.text((text_x, 80), f"{percent}%", font=font, fill="#FFFFFF")
        
        display.image(image)
        time.sleep(0.1)
    
    print("Animation end")
    time.sleep(2)
    
    print("Test ended successfully.")
    image = Image.new("RGB", (WIDTH, HEIGHT), "#004400")
    draw = ImageDraw.Draw(image)
    draw.text((30, 50), "TEST OK!", font=font, fill="#00FF00")
    draw.text((20, 70), "Everything works!", font=font, fill="#FFFFFF")
    display.image(image)
    
    print("\nDisplay works good!")
    print("Screen will be cleared in 5 seconds...")
    time.sleep(5)
    
    image = Image.new("RGB", (WIDTH, HEIGHT), "#000000")
    display.image(image)
    
    
except ImportError as e:
    print(f"\nERROR: Required libraries missing!")
    print(f"Details: {e}")
    print("\nInstall the libraries:")
    print("pip install adafruit-circuitpython-rgb-display Pillow")
    
except ValueError as e:
    print(f"\nERROR: SPI configuration problem!")
    print(f"Details: {e}")
    print("\nCheck if SPI is enabled:")
    print("sudo raspi-config -> Interface Options -> SPI -> Enable")
    
except Exception as e:
    print(f"\\Error: {e}")
    print("\nCheck the connections:")
    print("VCC    -> Pin 1  (3.3V)")
    print("GND    -> Pin 6  (GND)")
    print("CS     -> Pin 24 (GPIO 8)")
    print("RESET  -> Pin 18 (GPIO 24)")
    print("A0/DC  -> Pin 22 (GPIO 25)")
    print("SDA    -> Pin 19 (GPIO 10)")
    print("SCK    -> Pin 23 (GPIO 11)")
    print("LED    -> Pin 17 (3.3V)")

print("\nTest finished.")