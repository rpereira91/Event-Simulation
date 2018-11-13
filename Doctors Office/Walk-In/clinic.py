from doctor import Doctor
from patient import Patient
import random
from statistics import *
from datetime import datetime

class Clinic:
    doctor_array = []
    yearly_patient_list = []
    yearly_patient_count = []
    yearly_doc_idle_time = []
    yearly_patient_wait_time = []
    yearly_patient_long_wait_time = []
    yearly_patient_long_wait_count = []
    yearly_doc_skipped_lunch_count = []
    yearly_treatment_time = []
    yearly_overtime = []
    yearly_overtime_hours_worked = []
    waiting_room = []
    minute_count = 0
    doctor_count = 0

    def __init__(self, doctor_count):
        self.doctor_count = doctor_count
        #create doctors with staggered lunches
        self.reset_doctors()

    def run_year(self, title):
        for i in range(250):
            self.run_day()
        self.print_daily_info(title)

    def run_day(self):
        self.fill_waiting_room()
        daily_patient_list = []
        minute_count = 0   
        lunch_skipped = 0     
        # patient = self.get_earliest_patient()
        while len(self.waiting_room) > 0:
            for d in self.doctor_array:
                if d.on_lunch(minute_count):
                    continue 
                elif d.current_patient == 0:
                    #if the index is currently empty break out of the loop
                    if self.peek_earliest_patient() == 0:
                        break
                    elif self.peek_earliest_patient().get_arrival_time() <= minute_count:
                        patient = self.get_earliest_patient()
                        patient.set_admit_time(minute_count)
                        d.admit_patient(patient)
                        daily_patient_list.append(patient)
                    else:
                        d.increment_idle()
                elif d.get_busy_till() <= minute_count:
                    if d.lunch_skipped(minute_count):
                        lunch_skipped = 1
                    d.discharge_patient()
            minute_count += 1
        self.reset_doctors()
        self.yearly_overtime_hours_worked.append(minute_count-480 if minute_count-480 > 0 else 0)
        self.yearly_doc_skipped_lunch_count.append(lunch_skipped)
        self.daily_patient_wait_time(daily_patient_list)
        self.daily_patient_count(daily_patient_list)
#resets all the doctor information
    def reset_doctors(self):
        idle_time = 0
        for d in self.doctor_array:
            idle_time += d.get_idle()
        self.yearly_doc_idle_time.append(idle_time)
        self.doctor_array = []
        for i in range(self.doctor_count):
            self.doctor_array.append(Doctor(180 + (i%4) * 30))
        
    def daily_patient_wait_time(self, daily_patient_list):
        wait_time = 0
        long_wait_time = 0
        long_wait_count = 0
        daily_treatment_time = 0
        for p in daily_patient_list:
            wait_time += p.get_wait_time()
            if p.extra_long_wait:
                long_wait_count += 1
                long_wait_time += p.get_wait_time()
            daily_treatment_time += p.treatment_length
        self.yearly_treatment_time.append(daily_treatment_time)
        self.yearly_patient_wait_time.append(wait_time)
        self.yearly_patient_long_wait_count.append(long_wait_count)
        self.yearly_patient_long_wait_time.append(long_wait_time)

    #adds to the daily patient count    
    def daily_patient_count(self, daily_patient_list):
        self.yearly_patient_count.append(len(daily_patient_list))    
    #get a new patient 
    def new_patient(self, min_count):
        if (min_count < 450):
            return Patient(min_count)
        return False
    #returns the patient and takes it off the stack
    def get_earliest_patient(self):
        earliest_index = 0
        for p in range(len(self.waiting_room)):
            if self.waiting_room[earliest_index].get_arrival_time() > self.waiting_room[p].get_arrival_time():
                earliest_index = p
        return self.waiting_room.pop(earliest_index)
    # get the earliest patient
    def peek_earliest_patient(self):
        try:
            first = self.waiting_room[0]
        except IndexError:
            return 0
        for p in self.waiting_room:
            if first.get_arrival_time() > p.get_arrival_time():
                first = p
        return first
    #fill in the waiting room
    def fill_waiting_room(self):
        min_count = 0
        self.waiting_room = []
        random.seed(datetime.now())
        p = self.new_patient(min_count)
        self.waiting_room.append(p)
        while p:
            p = self.new_patient(min_count)
            if p:
                self.waiting_room.append(p)
            min_count += int(random.expovariate(1.0/15.0))
            
    def print_daily_info(self, title):
        file = open(title,"w") 
        title2 = "i_" + title
        file2 = open(title2,"w")
        file.write("10")
        file.write("\nStandard deviation, Daily Patient count , %s" % format(stdev(self.yearly_patient_count), '.2f'))
        file.write("\nMean, Daily Patient count , %s" % format(mean(self.yearly_patient_count), '.2f'))
        file.write("\n11")
        file.write("\nStandard deviation, Daily Patient wait time , %s" % format(stdev(self.yearly_patient_wait_time), '.2f'))
        file.write("\nMean, Daily Patient wait time , %s" % format(mean(self.yearly_patient_wait_time), '.2f'))
        file.write("\n12")
        file.write("\nStandard deviation, Long patient count , %s" % format(stdev(self.yearly_patient_long_wait_count), '.2f'))
        file.write("\nMean, Long patient count , %s" % format(mean(self.yearly_patient_long_wait_count), '.2f'))
        file.write("\n13")
        file.write("\nStandard deviation, Long patient time , %s" % format(stdev(self.yearly_patient_long_wait_time), '.2f'))
        file.write("\nMean, Long patient time , %s" % format(mean(self.yearly_patient_long_wait_time), '.2f'))
        file.write("\n14")
        file.write("\nStandard deviation, Daily lunch skipped , %s" % format(stdev(self.yearly_doc_skipped_lunch_count), '.2f'))
        file.write("\nMean, Daily lunch skipped , %s" % format(mean(self.yearly_doc_skipped_lunch_count), '.2f'))
        file.write("\n15")
        file.write("\nStandard deviation, Daily patient treatment , %s" % format(stdev(self.yearly_treatment_time), '.2f'))
        file.write("\nMean, Daily patient treatment , %s" % format(mean(self.yearly_treatment_time), '.2f'))
        file.write("\n16")
        file.write("\nStandard deviation, Daily Overtime , %s" % format(stdev(self.yearly_overtime_hours_worked), '.2f'))
        file.write("\nMean, Daily Overtime , %s" % format(mean(self.yearly_overtime_hours_worked), '.2f'))
        file.write("\n17")
        file.write("\nStandard deviation, Daily doctor idle , %s" % format(stdev(self.yearly_doc_idle_time), '.2f'))
        file.write("\nMean, Daily doctor idle , %s" % format(mean(self.yearly_doc_idle_time), '.2f'))
        # file.write("\nPercent of long waiting patients: %s %" % format(((sum(self.yearly_patient_long_wait_count)/sum(self.yearly_patient_count))*100))
        percent_waiting = (sum(self.yearly_patient_long_wait_count)/sum(self.yearly_patient_count)*100)
        file2.write("\nPercent of long waiting patients , %s" % format(percent_waiting, '.2f'))
        file2.write("\n")

