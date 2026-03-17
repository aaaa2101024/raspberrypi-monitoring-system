import subprocess
import time
from data.get_data import get_people_count

SLEEP_TIME = 10

class Send_infrared:
    def __init__(self):
        self.keys = ["off", "temperture=24.0", "temperture=23.5", "temperture=23.0", "temperture=22.5", "temperture=22.0", "temperture=21.5", "temperture=21.0", "temperture=20.5", "temperture=20.0"]
        self.pres_people = -1
    
    # by people count backet
    def control_airconditioner(self, current_people : int):
        if current_people >= 0:
            if self.pres_people != current_people and self.pres_people == 0:
                subprocess.run(["cgir", "send", "heat-on"])
                time.sleep(1)
        if self.pres_people != current_people:
            # command
            print(current_people)
            subprocess.run(["cgir", "send", self.keys[min([current_people, 7])]])
            self.pres_people = current_people
        # return flag
        if self.pres_people == 0:
            return 0
        else:
            return 1

if __name__ == "__main__":
    send_infrared = Send_infrared()
    while True:
        send_infrared.control_airconditioner(get_people_count())
        time.sleep(SLEEP_TIME)
