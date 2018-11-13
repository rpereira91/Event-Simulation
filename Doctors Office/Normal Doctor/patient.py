import random
from datetime import datetime

class Patient:
    #if the patient will be late
    isLate = False
    #set delay time
    delay = 0
    #start of the appointment
    appointmentTime = 0
    #the type of appointment, if it's a walk in, general visit, or routine
    appType = 0
    #amount of time the patient has to wait
    waitTime = 0
    #length of the appointment
    appLength = 0
    appCancled = False
    #acctual finish time
    finishTime = 0
    def __init__(self,appointmentTime,appType,late):
        self.appointmentTime = appointmentTime
        self.appType = appType
        self.get_appointment_length()
        #if they are late the length of the appointment is added to the delay
        if late:
            self.delay = abs(int(random.normalvariate(3,3)))
            if self.delay >= 15:
                self.appCancled = True

    def set_finish_time(self, finishTime):
        self.finishTime = finishTime
    #sets the wait time 
    def set_wait_time(self,wt):
        self.waitTime = wt
    
    def get_wait_time(self):
        return self.waitTime

    def get_delay(self):
        return self.delay
    def get_appointment_time(self):
        return self.appointmentTime
    def get_appointment_end(self):
        return self.appointmentTime + self.appType 
    # 0 for Routine visit
    # 1 for General visit
    # 3 for Walk-In

    def get_appointment_length(self):
        if self.appType == 0:
            self.appLength = int(random.expovariate(1.0/15.0))
        if self.appType == 1:
            self.appLength = int(random.expovariate(1.0/30.0))
        if self.appType == 3:
            self.appLength = int(random.expovariate(1.0/10.0))
    
    def get_appointment_length(self):
        return self.appLength
    
    def print_patient_info(self):
        print ("Appointment Start:" , self.appointmentTime , " - Appointment Length:" , self.appLength , "minutes - Late time:" , self.delay, "minutes - Wait time:" , self.waitTime)
        