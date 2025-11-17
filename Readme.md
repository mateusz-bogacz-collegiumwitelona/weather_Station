# Weather Station – Projekt zaliczeniowy z TMISW

**Wykonał:** Mateusz Bogacz-Drewniak

---

## Wymagania

### Sprzętowe

- Raspberry Pi z systemem **Raspberry Pi OS**
- Czujnik **BME280**
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
| 6 (GND)           | GND       |
| 3 (SDA)           | SDA (SDI) |
| 5 (SCL)           | SCL (SDK) |

### Schemat połączeń

![Schemat połączenia BME280](/images/schemat.png)

---

## Konfiguracja Raspberry Pi

1. Połącz się z Raspberry Pi przez **SSH**.
2. Włącz komunikację I2C:
   ```bash
   sudo raspi-config
   ```
   **Interface Options → I2C → Enable**
3. Sprawdź adres czujnika:
   ```bash
   sudo i2cdetect -y 1
   ```

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

![Raspberry Pi z BME280 - zdjęcie 1](/images/real_1.jpg)
![Raspberry Pi z BME280 - zdjęcie 2](/images/real_2.jpg)

---

## Dostęp do aplikacji

Po uruchomieniu frontendu strona jest dostępna pod adresem:  
[http://localhost:4173/](http://localhost:4173/)
