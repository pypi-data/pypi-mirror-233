import threading
import time
import webbrowser

import requests
from uvicorn import run


def check_frontend_alive(retries=10000, delay=0.25):
    """Polls frontend to see if it's alive. If alive, opens in browser."""
    for _ in range(retries):
        try:
            response = requests.get("http://localhost:3000/")
            if response.status_code == 200:
                webbrowser.open("http://localhost:3000/")
                return
        except requests.ConnectionError:
            # Server is not up yet. Wait for a while.
            time.sleep(delay)
    print("Failed to access frontend. Maybe it's taking longer to start?")


def frontend():
    run("aiconsole.app_frontend:app", host="0.0.0.0", port=3000)


def backend():
    run("aiconsole.app_backend:app", host="0.0.0.0", port=8000, reload=True)


def aiconsole():
    frontend_thread = threading.Thread(target=frontend, daemon=True)
    frontend_thread.start()

    frontend_check_thread = threading.Thread(target=check_frontend_alive, daemon=True)
    frontend_check_thread.start()

    # Start backend in the main thread
    backend()


if __name__ == "__main__":
    aiconsole()
