import logging
import threading
import time
import webbrowser

from uvicorn import run
from aiconsole.patched_interpreter.utils.display_markdown_message import display_markdown_message

from aiconsole.utils.is_update_needed import is_update_needed

log = logging.getLogger(__name__)


def open_webbrowser():
    time.sleep(2)
    webbrowser.open("http://localhost:8000/")


def backend():
    run(
        "aiconsole.app:app_only_backend",
        host="0.0.0.0",
        port=8000,
        reload=True,
        factory=True,
    )


def aiconsole():
    if is_update_needed():
        display_markdown_message(
            "> **A new version of AIConsole is available.**\n>Please run: `pip install --upgrade aiconsole`\n\n---")

    webbrowser_thread = threading.Thread(target=open_webbrowser)
    webbrowser_thread.start()
    try:
        run(
            "aiconsole.app:app_full",
            host="0.0.0.0",
            port=8000,
            reload=False,
            factory=True,
        )
    except KeyboardInterrupt:
        webbrowser_thread.join()
        log.info("Exiting ...")
