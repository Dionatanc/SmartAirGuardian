# iot_simulator/mqtt_publisher.py

import json
import time
import random
import paho.mqtt.client as mqtt

BROKER_HOST = "test.mosquitto.org"
BROKER_PORT = 1883
TOPIC = "smartair/guardian/data"
SENSOR_ID = "virtual_mqtt_001"


def generate_reading():
    return {
        "sensor_id": SENSOR_ID,
        "co2": random.uniform(350, 900),
        "pm25": random.uniform(5, 90),
        "temp": random.uniform(18, 32),
        "humidity": random.uniform(30, 80),
    }


def main():
    client = mqtt.Client()
    client.connect(BROKER_HOST, BROKER_PORT, 60)
    client.loop_start()
    print(f"Publicando dados MQTT em {BROKER_HOST}:{BROKER_PORT}, tópico '{TOPIC}'")

    try:
        while True:
            reading = generate_reading()
            payload = json.dumps(reading)
            client.publish(TOPIC, payload)
            print(f"Publicado MQTT: {payload}")
            time.sleep(5)
    except KeyboardInterrupt:
        print("Encerrando simulador MQTT.")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
