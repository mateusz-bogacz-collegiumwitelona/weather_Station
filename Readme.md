# Weather Station – Projekt zaliczeniowy z TMISW

**Wykonał:** Mateusz Bogacz-Drewniak

---

## Wymagania

### Sprzętowe

- Raspberry Pi z systemem **Raspberry Pi OS**
- Czujnik **BME280**
- Wyświetlacz **ST7735** (128x160, SPI)
- Kable połączeniowe
- Płytka prototypowa

### Programowe

- **Python**
- **Node.js** z **npm**

---

## Podłączenie BME280 do Raspberry Pi

| Raspberry Pi GPIO | BME280    |
| ----------------- | --------- |
| 17 (3.3V)         | Vin       |
| Ground            | GND       |
| 2 (SDA)           | SDA (SDI) |
| 3 (SCL)           | SCL (SDK) |

---

## Podłączenie ST7735 do Raspberry Pi

| Raspberry Pi GPIO | ST7735 Pin |
| ----------------- | ---------- |
| Pin 1 (3.3V)      | VCC        |
| Pin 6 (GND)       | GND        |
| Pin 24 (GPIO 8)   | CS         |
| Pin 18 (GPIO 24)  | RESET      |
| Pin 22 (GPIO 25)  | A0/DC      |
| Pin 19 (GPIO 10)  | SDA        |
| Pin 23 (GPIO 11)  | SCK        |
| Pin 17 (3.3V)     | LED        |

---

## Schemat połączeń

![Schemat połączeń](./images/weather_station_bb.png)

---

## Konfiguracja Raspberry Pi

1. Połącz się z Raspberry Pi przez **SSH**.

2. Włącz komunikację **I2C** (dla BME280):

   ```bash
   sudo raspi-config
   ```

   **Interface Options → I2C → Enable**

3. Włącz komunikację **SPI** (dla ST7735):

   ```bash
   sudo raspi-config
   ```

   **Interface Options → SPI → Enable**

4. Sprawdź adres czujnika BME280:
   ```bash
   sudo i2cdetect -y 1
   ```

---

## Instalacja bibliotek dla wyświetlacza

Zainstaluj wymagane biblioteki Python dla ST7735:

```bash
pip install adafruit-circuitpython-rgb-display Pillow
```

### Test wyświetlacza ST7735

Uruchom test wyświetlacza:

```bash
python display_test.py
```

Test wykonuje następujące sekwencje:

- Wyświetlenie kolorów: czarny, czerwony, zielony, niebieski, biały
- Wyświetlenie tekstu z danymi pogodowymi
- Animację paska postępu
- Potwierdzenie poprawnego działania

---

## Uruchomienie backendu

1. Pobierz projekt:  
   [Weather Station](https://github.com/mateusz-bogacz-collegiumwitelona/weather_Station)
2. Przejdź do katalogu `backend`.
3. Utwórz środowisko wirtualne:
   ```bash
   python -m venv .venv
   ```
4. Aktywuj środowisko:
   ```bash
   source .venv/bin/activate
   ```
5. Zainstaluj zależności:
   ```bash
   pip install -r requirements.txt
   ```
6. Uruchom backend:
   ```bash
   python main.py
   ```

---

## Uruchomienie frontendu

1. Przejdź do katalogu `frontend`.
2. Zainstaluj zależności:
   ```bash
   npm install
   ```
3. Zbuduj projekt:
   ```bash
   npm run build
   ```
4. Uruchom podgląd:
   ```bash
   npm run preview
   ```

---

## Zdjęcia rzeczywiste

![Zdjęcie 1](./images/bNYBmX3j.jpg)
![Zdjęcie 2](./images/I830sLuW.jpg)

---

## Dostęp do aplikacji

Po uruchomieniu frontendu strona jest dostępna pod adresem:  
[http://localhost:4173/](http://localhost:4173/)

---

## Rozwiązywanie problemów

### Problem z wyświetlaczem ST7735

Jeśli wyświetlacz nie działa:

1. Sprawdź, czy SPI jest włączone:

   ```bash
   sudo raspi-config
   ```

2. Zweryfikuj poprawność połączeń zgodnie z tabelą podłączeń

3. Sprawdź, czy biblioteki są zainstalowane:
   ```bash
   pip list | grep adafruit
   ```

### Problem z czujnikiem BME280

Jeśli czujnik nie jest wykrywany:

1. Sprawdź połączenia I2C
2. Upewnij się, że I2C jest włączone w `raspi-config`
3. Użyj `i2cdetect -y 1` aby zweryfikować adres czujnika
