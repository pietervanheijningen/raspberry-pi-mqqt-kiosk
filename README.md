# Raspberry pi based kiosk controllable by home assistant/mqqt

Mostly my own project, expect some tinkering to get it working

### Features:
- Display any webpage with chromium
- Change the current page to display with MQQT
- Remembers what the last page was set to on reboot

### Installation (from what i can remember, might not be complete)
- ``sudo raspi-config`` -> system options -> boot -> dekstop autologin
- ``sudo apt install xdotool unclutter sed``
- ``pip install paho-mqtt --break-system-packages``
- setup .env file for MQQT config
- ``./install.sh``

homeassistant configuration.yaml:
```yaml
input_text:
  browser_url:
    name: Browser URL
    initial: ""
    max: 255
automation:
- alias: Send URL to Raspberry Pi
  trigger:
    platform: state
    entity_id: input_text.browser_url
  action:
    - service: mqtt.publish
      data:
        topic: "browser/command"
        payload: "url:{{ states('input_text.browser_url') }}"
```
