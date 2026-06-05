import requests

url = 'http://localhost/print'

# Alphanumeric
alphanumeric = "Alphanumeric: ABCabc123\n"

# Box drawing characters using Unicode (which Flask/Python will encode to CP866)
pseudographics = (
    "Box drawing (CP866):\n"
    "\u250c\u2500\u2510\n"  # ┌─┐
    "\u2502 \u2502\n"  # │ │
    "\u2514\u2500\u2518\n"  # └─┘
    "\u2554\u2550\u2557\n"  # ╔═╗
    "\u2551 \u2551\n"  # ║ ║
    "\u255a\u2550\u255d\n"  # ╚═╝
    "\n"
)

payload = [
    {"type": "text", "content": "--- START CHARACTER TEST ---\n"},
    {"type": "text", "content": alphanumeric},
    {"type": "text", "content": pseudographics},
    {"type": "text", "content": "--- END CHARACTER TEST ---\n\n\n\n"}
]

try:
    print("Sending character test payload...")
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
