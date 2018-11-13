import random
from datetime import datetime

class Patient:
    arrivial_time = 0
    admit_time = 0
    treatment_length = 0
    exit_time = 0
    wait_time = 0
    extra_long_wait = False

    def __init__(self,arrivial_time):
        self.arrivial_time = arrivial_time
        random.seed(datetime.now())
        self.treatment_length = int(random.expovariate(1.0/10.0))

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
    #method used for debugging
    def print_info(self):
        print("Patient arrive time: " , self.arrivial_time,"Patient admit time: " , self.admit_time, "Treatment length: " ,  self.treatment_length , "Wait time: " , self.wait_time)