from patient import Patient
class Doctor:
    current_patient = 0
    busy_till = 0
    lunch_start = 0
    lunch_end = 0
    idle_time = 0

    def __init__(self, lunch_time):
        self.lunch_start = lunch_time
        self.lunch_end = lunch_time + 60

    def is_free(self, current_time):
        return True if current_time > self.busy_till else False

    #checks to see if the doctor is on lunch
    def on_lunch(self, current_time):
        if self.lunch_start <= current_time and current_time < self.lunch_end:
            return True
        else:
            return False
    def lunch_skipped(self, current_time):
        if self.lunch_start+40 <= current_time and current_time < self.lunch_end:
            return True
        else:
            return False
    #sets the new patient
    def admit_patient(self, patient):
        self.current_patient = patient
        self.busy_till = self.current_patient.get_exit_time()
    #discharges the patient
    def discharge_patient(self):
        self.current_patient = 0
        self.busy_till = 0
    
    def get_lunch_time(self):
        return self.lunch_start
    
    def get_busy_till(self):
        return self.busy_till

    def increment_idle(self):
        self.idle_time += 1

    def get_idle(self):
        return self.idle_time