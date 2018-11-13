from patient import Patient
import random 
import numpy as np
from statistics import *
#Patients are recieved for 3(180 minutes) hours then a 1 hour(60 minutes) break then again for 3.5 (210 minutes) hours. The time will be calculated by minutes in the day. 
class Clinic:
    
    yearly_patient_list = []
    yearly_lunch = []
    total_hours = []
    overtime_hours = []
    doctor_wait_time = []
    general_percent = 0.0
    late = False
    file_title = ""
    greedy = False
    
    def __init__(self,genPercent,late,greedy, file_title):
        self.general_percent = genPercent
        self.late = late
        self.greedy = greedy
        self.file_title = file_title
    #create a schedule for one day
    def create_day_schedule(self):
        daily_patient_list = []
        daily_lunch = 0
        minute_count = 0
        while(minute_count < 480):
            if self.greedy:
                if minute_count == 0 or minute_count == 300:
                    p = self.schedule_appointment(minute_count ,0)
                    daily_patient_list.append(p)
            if random.random() > self.general_percent:
                p = self.schedule_appointment(minute_count ,0)
                minute_count += 15
            else:
                p = self.schedule_appointment(minute_count,1)
                minute_count += 30
            daily_patient_list.append(p)
            
            if minute_count > 200 and minute_count <= 300:
                delay = ((daily_patient_list[-1].get_appointment_end())-200)
                if delay <= 0:
                    continue
                elif delay >= 40:
                    daily_lunch = 1
                minute_count = 300
        self.total_hours.append(self.calc_total_hours(daily_patient_list))
        if(self.total_hours[-1] - 480 > 0):
            self.overtime_hours.append(self.total_hours[-1] - 480)
        else:
            self.overtime_hours.append(0)
        self.yearly_lunch.append(daily_lunch)
        self.calculate_wait_time(daily_patient_list)
        self.calculate_late_time(daily_patient_list)
        self.yearly_patient_list.append(daily_patient_list)
    #schedule an appointment for a new patient
    def calc_total_hours(self,arr):
        sum = 0
        for i in range (len(arr)):
            sum += arr[i].get_appointment_length()
        return sum
    def display_stats(self):
        file = open(self.file_title,"w") 
        wait_time = []
        daily_patients = []
        long_wait_time = []
        long_wait_time_minutes = []
        patients_canclled = []
        for day in self.yearly_patient_list:
            long_wait = 0
            cancled = 0
            long_wait_minutes = 0
            for p in day:
                wait_time.append(p.get_wait_time())
                if p.get_wait_time() >= 15:
                    long_wait += 1
                    long_wait_minutes += p.get_wait_time()
                if p.appCancled:
                    cancled += 1
            long_wait_time.append(long_wait)
            patients_canclled.append(cancled)
            long_wait_time_minutes.append(long_wait_minutes)
            daily_patients.append(len(day))
        file.write("1")
        file.write("\nStandard deviation, Daily Patient count ,%s"% format(stdev(daily_patients) , '.2f'))
        file.write("\nMean, Daily Patient count ,%s"%format(mean(daily_patients), '.2f'))
        file.write("\n2")
        file.write("\nStandard deviation, Daily wait time ,%s"%format(stdev(wait_time), '.2f'))
        file.write("\nMean, Daily wait time ,%s"%format(mean(wait_time), '.2f'))
        file.write("\n3")
        file.write("\nStandard deviation, Long wait time count ,%s"%format(stdev(long_wait_time), '.2f'))
        file.write("\nMean, Long wait time count ,%s"%format(mean(long_wait_time), '.2f'))
        file.write("\n4")
        file.write("\nStandard deviation, Long wait time ,%s"%format(stdev(long_wait_time_minutes), '.2f'))
        file.write("\nMean, Long wait time ,%s"%format(mean(long_wait_time_minutes), '.2f'))
        file.write("\n5")
        file.write("\nStandard deviation, Patients canclled ,%s"%format(stdev(patients_canclled), '.2f'))
        file.write("\nMean, Patients canclled ,%s"%format(mean(patients_canclled), '.2f'))
        file.write("\n6")
        file.write("\nStandard deviation, Doctor Lunch Skipped ,%s"%format(stdev(self.yearly_lunch), '.2f'))
        file.write("\nMean, Doctor Lunch Skipped ,%s"%format(mean(self.yearly_lunch), '.2f'))
        file.write("\n7")
        file.write("\nStandard deviation, Total Minutes ,%s"%format(stdev(self.total_hours), '.2f'))
        file.write("\nMean, Total Minutes ,%s"%format(mean(self.total_hours), '.2f'))
        file.write("\n8")
        file.write("\nStandard deviation, Overtime Minutes ,%s"%format(stdev(self.overtime_hours), '.2f'))
        file.write("\nMean, Overtime Minutes ,%s"%format(mean(self.overtime_hours), '.2f'))
        file.write("\n9")
        file.write("\nStandard deviation, Idle Minutes ,%s"%format(stdev(self.doctor_wait_time), '.2f'))
        file.write("\nMean, Idle Minutes ,%s"%format(mean(self.doctor_wait_time), '.2f'))
    #schedules a single appointment
    def schedule_appointment(self, appointment_time, appointment_type):
        patient = Patient(appointment_time,appointment_type,self.late)
        return patient
    #calculates the wait time for the patients
    def calculate_wait_time(self,daily_patient_list):
        for i in range(1,len(daily_patient_list)):
            this_patient = daily_patient_list[i]
            prev_patient = daily_patient_list[i-1]
            wait_time = prev_patient.get_appointment_length() - (this_patient.get_appointment_time() - prev_patient.get_appointment_time())
            if wait_time > 0:
                this_patient.set_wait_time(wait_time)
            #set the finishing time for the doctor
            this_patient.set_finish_time(this_patient.get_appointment_time() + this_patient.get_wait_time())
            
#gets the total amount of idle time a doctor has waiting for patients per day    
    def calculate_late_time(self, daily_patient_list):
        wait_time_sum = 0
        for p in daily_patient_list:
            wait_time_sum += p.get_delay()
        self.doctor_wait_time.append(wait_time_sum)
#runs it for a certian number of days    
    def run_for_days(self, days):
        for i in range(days):
            self.create_day_schedule()
        self.display_stats()
            
    


    


