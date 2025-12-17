import subprocess
import json

open_json = open("./codes.json", "r")
keys = json.load(open_json)

print(keys["off"])
# command
subprocess.run(["cgir", "send", "off"])
