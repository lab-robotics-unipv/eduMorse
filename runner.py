import os
import subprocess

MORSELABPATH = os.environ.get("MORSELABPATH")
SERVERPATH = os.path.join(MORSELABPATH, "test_toml/socket")
TESTPATH = os.path.join(MORSELABPATH, "test_toml")

subprocess.Popen("python3 server.py &".split(" "))
subprocess.Popen("python3 collision.py &".split(" "))
subprocess.Popen("python3 layer.py &".split(" "))
subprocess.Popen("python3 score.py".split(" "))
