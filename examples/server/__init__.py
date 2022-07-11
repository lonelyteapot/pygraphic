import subprocess
import time


def start_server():
    subprocess.Popen("strawberry server example.server.schema:schema")
    time.sleep(3)
