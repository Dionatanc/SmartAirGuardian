# iot_simulator/http_publisher.py

import time
import random
import requests

API_URL = "http://127.0.0.1:8000/ingest"
SENSOR_ID = "virtual_esp32_001"


def generate_reading():
    return {
        "sensor_id": SENSOR_ID,
        "co2": random.uniform(350, 900),
        "pm25": random.uniform(5, 90),
        "temp": random.uniform(18, 32),
        "humidity": random.uniform(30, 80),
    }


def main():
    print("Iniciando simulador HTTP do SmartAir Guardian...")
    while True:
        reading = generate_reading()
        try:
            resp = requests.post(API_URL, json=reading, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                print(
                    f"[OK] Enviado: CO2={data['co2']:.1f}, PM2.5={data['pm25']:.1f}, "
                    f"risk={data['risk_level']}, anomaly={data['is_anomaly']}"
                )
            else:
                print(f"[ERRO] Status HTTP {resp.status_code}: {resp.text}")
        except Exception as e:
            print(f"[EXCEÇÃO] {e}")
        time.sleep(5)


if __name__ == "__main__":
    main()
