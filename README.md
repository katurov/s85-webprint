# S85 Web Print Service

A Flask-based web service for printing to the S85 Bluetooth thermal printer.

## Installation
The service is designed to run on a Raspberry Pi Zero 2 W.
It uses a systemd service for auto-start.

## Files
- `app.py`: Flask API
- `printer_logic.py`: Bluetooth and ESC/POS logic
- `s85-webprint.service`: Systemd service file
