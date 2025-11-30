import threading
import datetime

# ANSI escape colors
RESET = "\033[0m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"

_lock = threading.Lock()

def _ts():
    return datetime.datetime.now().strftime("%H:%M:%S")

def info(msg):
    with _lock:
        print(f"{GREEN}[INFO { _ts() }] {RESET}{msg}")

def warn(msg):
    with _lock:
        print(f"{YELLOW}[WARN { _ts() }] {RESET}{msg}")

def error(msg):
    with _lock:
        print(f"{RED}[ERROR { _ts() }] {RESET}{msg}")

def debug(msg):
    with _lock:
        print(f"{CYAN}[DEBUG { _ts() }] {RESET}{msg}")

