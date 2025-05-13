from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_required_env(key: str) -> str:
    """Get a required environment variable or raise an error if not found."""
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Required environment variable {key} is not set. Please check your .env file.")
    return value

# MQTT Configuration
MQTT_BROKER = get_required_env("MQTT_BROKER")
MQTT_PORT = int(get_required_env("MQTT_PORT"))
MQTT_TOPIC = get_required_env("MQTT_TOPIC")

# API Configuration
API_HOST = get_required_env("API_HOST")
API_PORT = int(get_required_env("API_PORT"))

# OpenAI Configuration
OPENAI_API_KEY = get_required_env("OPENAI_API_KEY") 