import subprocess
import time
from data.get_data import get_people_count

# by people count backet
keys = ["off", "temperture=24.0", "temperture=23.5", "temperture=23.0", "temperture=22.5", "temperture=22.0", "temperture=21.5", "temperture=21.0", "temperture=20.5", "temperture=20.0"]

pres_people = -1

while(True):
    current_people = get_people_count()
    if pres_people != current_people and pres_people == 0:
        subprocess.run(["cgir", "send", "heat-om"])
        time.sleep(1)
    if pres_people != current_people:
        # command
        print(current_people)
        subprocess.run(["cgir", "send", keys[current_people]])
        pres_people = current_people
    time.sleep(10)
