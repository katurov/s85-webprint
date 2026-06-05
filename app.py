from flask import Flask, request, jsonify
from printer_logic import S85Printer
import string

app = Flask(__name__)
printer = S85Printer()

DOCS = """
# S85 Printer API Documentation

This service provides an interface for the S85 Bluetooth thermal printer.

## Endpoints

### GET /
Returns this documentation.

### GET /status
Returns the current status of the printer.
- 200 OK: Printer is ready.
- 503 Service Unavailable: Printer is offline, out of paper, or unreachable.

### POST /print
Prints a job. The body should be a JSON list of commands.
- Max total content length: 512 characters.
- Types: text, qr, barcode.

Example Payload:
[
    {"type": "text", "content": "Hello!\n"},
    {"type": "qr", "content": "https://github.com/katurov/s85-webprint"},
    {"type": "barcode", "content": "12345678"}
]

## Validation Rules
- text: Only printable characters and newlines allowed.
- qr: Any valid UTF-8 string.
- barcode: Alphanumeric characters (CODE128).
"""

def is_printable(s):
    printable = set(string.printable)
    return all(c in printable for c in s)

@app.route('/')
def index():
    return DOCS, 200, {'Content-Type': 'text/markdown; charset=utf-8'}

@app.route('/status')
def status():
    success, message = printer.get_status()
    if success:
        return jsonify({"status": "ready", "message": message}), 200
    else:
        return jsonify({"status": "error", "message": message}), 503

@app.route('/print', methods=['POST'])
def print_job():
    data = request.json
    if not isinstance(data, list):
        return jsonify({"status": "error", "message": "Payload must be a list of commands"}), 400
    
    total_len = 0
    jobs = []
    
    for item in data:
        cmd_type = item.get('type')
        content = item.get('content', '')
        if not cmd_type or not content: continue
            
        total_len += len(content)
        if total_len > 512:
            return jsonify({"status": "error", "message": "Total content length exceeds 512 characters"}), 400
            
        if cmd_type == 'text':
            if not is_printable(content):
                return jsonify({"status": "error", "message": f"Invalid characters in text: {content}"}), 400
        elif cmd_type == 'barcode':
            if not content.isalnum():
                return jsonify({"status": "error", "message": f"Invalid characters in barcode: {content}"}), 400
        elif cmd_type == 'qr':
            pass
        else:
            return jsonify({"status": "error", "message": f"Unknown command type: {cmd_type}"}), 400
            
        jobs.append((cmd_type, content))
        
    if not jobs:
        return jsonify({"status": "error", "message": "No valid commands provided"}), 400

    # We skip the status check here to avoid EBUSY race conditions.
    # print_job itself will handle connection and report failure if unreachable.
    success, message = printer.print_job(jobs)
    if success:
        return jsonify({"status": "success", "message": "Job sent to printer"}), 200
    else:
        # Map specific errors if needed, but 503 is generally correct for unreachable printer
        return jsonify({"status": "error", "message": message}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
