import json
import random
import time
from datetime import datetime
import requests

LOKI_URL = "http://localhost:3100/loki/api/v1/push"

ENDPOINTS = [
    "/api/v1/login",
    "/api/v1/checkout",
    "/api/v1/products",
    "/images/banner.png",
    "/admin/dashboard",
    "/api/v1/user/profile",
]
STATUS_CODES = [200, 200, 200, 200, 201, 400, 403, 404, 500, 502]
IP_LIST = [
    "192.168.1.10",
    "192.168.1.25",
    "203.0.113.42",
    "198.51.100.2",
    "10.0.0.15",
]


def generate_log_line():
    ip = random.choice(IP_LIST)
    endpoint = random.choice(ENDPOINTS)
    status = random.choice(STATUS_CODES)
    bytes_sent = random.randint(200, 5000)
    response_time_ms = random.randint(15, 650)
    # Combined Log Format style
    return f'{ip} - - [{datetime.utcnow().strftime("%d/%b/%Y:%H:%M:%S +0000")}] "GET {endpoint} HTTP/1.1" {status} {bytes_sent} rt={response_time_ms}ms'


def push_batch():
    batch = [generate_log_line() for _ in range(10)]
    now_ns = str(time.time_ns())
    payload = {
        "streams": [
            {
                "stream": {
                    "job": "web_server_access_logs",
                    "environment": "production",
                },
                "values": [[now_ns, line] for line in batch],
            }
        ]
    }
    try:
        res = requests.post(
            LOKI_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        if res.status_code == 204:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 10 logs pushed")
        else:
            print(f"Failed with status: {res.status_code}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    print("Streaming logs to Loki... (Ctrl+C to stop)")
    while True:
        push_batch()
        time.sleep(2)