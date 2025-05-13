from paho.mqtt import client as mqtt_client
import json
from typing import Optional, Callable
from config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC

class AmbientMQTTClient:
    def __init__(self):
        self.latest_ambient_data: Optional[dict] = None
        self.client = self._create_client()
        self._connect()

    def _create_client(self) -> mqtt_client.Client:
        client = mqtt_client.Client()
        client.on_connect = self._on_connect
        client.on_message = self._on_message
        return client

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.subscribe(MQTT_TOPIC)
        else:
            print(f"Failed to connect, return code {rc}")

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            self.latest_ambient_data = payload
        except json.JSONDecodeError:
            self.latest_ambient_data = {"value": msg.payload.decode()}

    def _connect(self):
        try:
            self.client.connect(MQTT_BROKER, MQTT_PORT)
            self.client.loop_start()
        except Exception as e:
            print(f"Error connecting to MQTT broker: {e}")
            raise

    def get_latest_data(self) -> Optional[dict]:
        """Returns the latest ambient data received from MQTT"""
        return self.latest_ambient_data

# Create a singleton instance
mqtt_client_instance = AmbientMQTTClient() 