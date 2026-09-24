import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_URL = "http://localhost/gym/api/fingerprint-checkin.php"
API_KEY = os.environ.get("FINGERPRINT_API_KEY", "gym-fingerprint-dev-2026")

# Mock: เทสเฉพาะโป้ง 1
MOCK_FINGER = {
    "label": "โป้ง 1",
    "sensor_slot": 1,
    "confidence": 90,
}

def check_in(sensor_slot: int, confidence: int) -> None:
    payload = json.dumps({
        "sensor_slot": sensor_slot,
        "confidence": confidence,
    }).encode("utf-8")

    request = Request(
        API_URL,
        data=payload,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-API-Key": API_KEY,
        },
    )

    try:
        with urlopen(request, timeout=10) as response:
            print_response(response.read())

    except HTTPError as error:
        print(f"API error: {error.code}")
        print_response(error.read())

    except URLError as error:
        print("เชื่อมต่อ API ไม่ได้:", error.reason)

def print_response(raw_response: bytes) -> None:
    response_text = raw_response.decode("utf-8", errors="replace")
    try:
        result = json.loads(response_text)
    except json.JSONDecodeError:
        print(response_text)
        return

    print(json.dumps(result, ensure_ascii=False, indent=2))

if not API_KEY:
    raise RuntimeError("กรุณาตั้ง FINGERPRINT_API_KEY ก่อนรัน")

print(f"พร้อมทดสอบ {MOCK_FINGER['label']}")
print("กด Enter เพื่อจำลองการสแกน, Ctrl+C เพื่อหยุด")

try:
    while True:
        input()

        print(
            f"Mock scan: {MOCK_FINGER['label']} | "
            f"slot={MOCK_FINGER['sensor_slot']} | "
            f"confidence={MOCK_FINGER['confidence']}"
        )

        check_in(
            MOCK_FINGER["sensor_slot"],
            MOCK_FINGER["confidence"],
        )

except KeyboardInterrupt:
    print("\nStopped")