from patient import Patient


class Doctor:
    current_patient = 0
    busy_till = 0
    lunch_start = 0
    lunch_end = 0
    idle_time = 0
    id = -1

    def __init__(self, lunch_time, id):
        self.lunch_start = lunch_time
        self.lunch_end = lunch_time + 60
        self.id = id

    #sets the new patient
    def admit_patient(self, patient):
        self.current_patient = patient
        self.busy_till = self.current_patient.get_exit_time()
    #discharges the patient
    def discharge_patient(self):
        self.current_patient = 0
        self.busy_till = 0

    def get_busy_till(self):
        return self.busy_till