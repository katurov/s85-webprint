# S85 Web Print Service

## Project Description
This project was created purely for entertainment purposes to control an S85 Bluetooth thermal printer. It provides a simple web interface (API) that allows printing text, QR codes, and barcodes. The service is designed for easy consumption by both humans and AI agents.

## Hardware & Software
- **Hardware:** Raspberry Pi Zero 2 W
- **OS:** Debian 13 (Trixie)
- **Language:** Python 3 (Flask)
- **Connectivity:** Bluetooth RFCOMM (via native Python sockets)

## Port
The service runs on **port 80**.

---

## Instructions for Agents (and Humans)

### 1. Check Status
It is recommended to check the printer status before sending a print job.
- **URL:** GET /status
- **Success (200 OK):** `{"status": "ready", "message": "Ready"}`
- **Error (503 Service Unavailable):** Returned if the printer is off, out of paper, or the cover is open.

### 2. Printing
- **URL:** POST /print
- **Header:** Content-Type: application/json
- **Body:** A list of command objects.

#### Data Format:
```json
[
  {
    "type": "text",
    "content": "Hello! This is text.\n"
  },
  {
    "type": "qr",
    "content": "https://github.com/katurov/s85-webprint",
    "size": 6
  },
  {
    "type": "barcode",
    "content": "123456789012"
  }
]
```

#### Commands & Options:
- **text**: Prints plain text.
    - **Note on Characters**: ASCII and **Pseudo-graphics (box drawing)** are supported. 
    - **Cyrillic is NOT supported** (it will be replaced by diacritics/symbols).
- **qr**: Generates a QR code.
    - `content`: Any valid string or URL.
    - `size` (optional): Module size from 1 to 16. **Recommended: 6** for URLs.
- **barcode**:
    - Automatic detection: If content consists of 12-13 digits, it prints an **EAN13** barcode.
    - Fallback: Otherwise, it prints a **CODE128** barcode.

#### Constraints:
- **Length:** The total length of all content in a single request must not exceed 512 characters.

### 3. Documentation
The Markdown documentation is always available at GET /.

### 4. Example usage (curl)
```bash
curl -X POST -H "Content-Type: application/json" -d '[
    {"type": "text", "content": "Test print\n"},
    {"type": "qr", "content": "https://github.com/katurov/s85-webprint", "size": 6}
]' http://192.168.42.53/print
```
