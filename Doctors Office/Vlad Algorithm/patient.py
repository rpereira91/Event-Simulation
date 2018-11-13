import random
from datetime import datetime

class Patient:
    arrivial_time = 0
    admit_time = 0
    treatment_length = 0
    exit_time = 0
    wait_time = 0
    appointment_length = 0
    extra_long_wait = False
    urgent = False
    walk_in = False
    md1 = -1
    md2 = -1
    md3 = -1
    choosy = False
    def __init__(self,appointment_length,arrivial_time,urgent,walk_in,md1,md2,md3):
        self.appointment_length = appointment_length
        self.urgent = urgent
        self.walk_in = walk_in
        self.arrivial_time = arrivial_time
        self.md1 = md1
        self.md2 = md2
        self.md3 = md3
        if self.md1 > -1:
            self.choosy = True
    
    def get_md1(self):
        return self.md1
    
    def get_md2(self):
        return self.md2
    
    def get_md3(self):
        return self.md3
    def set_admit_time(self, admit_time):
        self.admit_time = admit_time
        self.exit_time = self.treatment_length + self.admit_time
        self.wait_time = self.admit_time - self.arrivial_time 
        if self.wait_time >= 15:
            self.extra_long_wait = True

    def get_admit_time(self):
        return self.admit_time
    #find out what time the patient leaves
    def get_exit_time(self):
        return self.exit_time
    #get the wait time for the patient
    def get_wait_time(self):
        return self.wait_time
    def get_arrival_time(self):
        return self.arrivial_time
        
