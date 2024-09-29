import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# MQTT broker details
MQTT_BROKER = os.getenv("MQTT_BROKER_IP")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

# Path to the file storing the last URL
URL_FILE = "/home/pi/raspberry-pi-mqqt-kiosk/url.txt"

def set_url(url):
    """Launch the Chromium browser in kiosk mode with the given URL and store the URL in a file."""
    os.system(f"2>/dev/null 1>&2 /usr/bin/chromium-browser --noerrdialogs --disable-infobars --kiosk {url} /dev/null &")

    # Write the URL to url.txt
    with open(URL_FILE, "w") as file:
        file.write(url)


def read_url():
    """Read the URL from url.txt, if it exists."""
    if os.path.exists(URL_FILE):
        with open(URL_FILE, "r") as file:
            return file.read().strip()
    return None


def on_connect(client, userdata, flags, rc):
    """Handle MQTT connection and subscribe to the topic."""
    print(f"Connected with result code {rc}")
    client.subscribe("browser/command")


def on_message(client, userdata, msg):
    """Handle messages received via MQTT and take appropriate actions."""
    command = msg.payload.decode()
    if command.startswith("url:"):
        url = command[4:]
        set_url(url)
    elif command == "screen_off":
        os.system("vcgencmd display_power 0")
    elif command == "screen_on":
        os.system("vcgencmd display_power 1")


# Read the last URL from the file on startup and launch the browser with it
last_url = read_url()
if last_url:
    print(f"Launching with last URL: {last_url}")
    set_url(last_url)

# Create MQTT client and set up callbacks
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Set MQTT username and password if provided
if MQTT_USERNAME and MQTT_PASSWORD:
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

# Connect to the MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Loop forever and handle incoming MQTT messages
client.loop_forever()
