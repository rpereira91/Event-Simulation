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
    regular_waiting_room = []
    urgent_waiting_room = []
    waiting_room = []
    free_doc = []
    type_of_appointment = 0
    rate = 0
    title = ""

    def __init__(self, rate, type_of_appointment, title):
        #create doctors with staggered lunches
        self.reset_doctors()
        self.rate = rate
        self.type_of_appointment = type_of_appointment
        self.title = title
    #run the simulation for a year
    def run_year(self):
        for i in range(250):
            self.run_day()
        self.print_daily_info()
    #run the simulation for a day
    def run_day(self):
        #populate the waiting rooms
        self.populate_waiting_rooms()
        current_min = 0
        daily_patient_list = []
        #run till the main waiting room is empty
        while len(self.waiting_room) > 0:
            #check the urgent waiting room if there is a patient in there that can be helped give them to a doctor
            if self.peek_earliest_patient(self.urgent_waiting_room) != 0:
                p = self.get_earliest_patient(self.urgent_waiting_room)
                if p.get_arrival_time() <= current_min:
                    for d in self.doctor_array:
                        if d.busy_till == 0:                      
                            p.set_admit_time(current_min)
                            d.admit_patient(p)
                            daily_patient_list.append(p)
                            break 
                #if there's no doctor avalable 
                if p.admit_time == 0:
                    self.urgent_waiting_room.insert(0,p) 
    #check through the main waiting room for any patients that can be helped, if its empty the search is over
            if self.peek_earliest_patient(self.waiting_room) == 0:
                break
            #if its an urgent care matter help them first,
            if self.peek_earliest_patient(self.waiting_room).get_arrival_time() <= current_min:
                p = self.get_earliest_patient(self.waiting_room)
                if p.urgent:
                    for d in self.doctor_array:
                        if d.busy_till == 0:
                            p.set_admit_time(current_min)
                            d.admit_patient(p)
                            daily_patient_list.append(p)
                            break
        #if they don't have room yet add them to the urgent care waiting room
                    if p.admit_time == 0:
                        self.urgent_waiting_room.append(p)
                else:
                    #if its a non urgent care patient make them search through the doctors till they find someone
                    for d in self.doctor_array:
                        if d.busy_till == 0:
                            if p.choosy:
                                if d.id != p.md1 or d.id != p.md2 or d.id != p.md3:
                                    p.set_admit_time(current_min)
                                    d.admit_patient(p)
                                    daily_patient_list.append(p)
                                    break
                            else:
                                p.set_admit_time(current_min)
                                d.admit_patient(p)
                                daily_patient_list.append(p)
                                break
                    #if the patient still hasn't found a doctor add them to the waiting room queue
                    if p.admit_time == 0:
                        self.regular_waiting_room.append(p)
            #check the regular waiting room, using similar logic as the previous normal priority patients
            if self.peek_earliest_patient(self.regular_waiting_room) != 0:
                p = self.get_earliest_patient(self.regular_waiting_room)
                for d in self.doctor_array:
                    if d.busy_till == 0:
                        if p.choosy:
                            if d.id != p.md1 or d.id != p.md2 or d.id != p.md3:
                                p.set_admit_time(current_min)
                                d.admit_patient(p)
                                daily_patient_list.append(p)
                                break
                        else:
                            p.set_admit_time(current_min)
                            d.admit_patient(p)
                            daily_patient_list.append(p)
                            break
                if p.admit_time == 0:
                    self.regular_waiting_room.insert(0,p) 
            self.discharge(current_min)        
            current_min += 1
        self.daily_patient_wait_time(daily_patient_list)
        self.daily_patient_count(daily_patient_list)
        self.reset_doctors()
    #gather all the user data         
    def daily_patient_wait_time(self, daily_patient_list):
        wait_time = 0
        long_wait_time = 0
        long_wait_count = 0
        daily_treatment_time = 0
        for p in daily_patient_list:
            wait_time += p.get_wait_time()
            daily_treatment_time += p.treatment_length
        self.yearly_treatment_time.append(daily_treatment_time)
        self.yearly_patient_wait_time.append(wait_time)

    #adds to the daily patient count    
    def daily_patient_count(self, daily_patient_list):
        self.yearly_patient_count.append(len(daily_patient_list)) 

    #check if a doctor can discharage any patients          
    def discharge(self,minute_count):
        for d in self.doctor_array:
            if d.get_busy_till() <= minute_count:
                d.discharge_patient()
                  
    
    #reset the doctor's information
    def reset_doctors(self):
        self.doctor_array = []
        for i in range(10):
            self.doctor_array.append(Doctor(180 + (i%4) * 30 , 1))
    
    def create_appointment(self,arrival_time):
        random.seed(datetime.now())
        md_choose = random.random()
        #70% chance of them liking all the MD's
        if md_choose <= 0.7:
            self.waiting_room.append(Patient(int(random.expovariate(1.0/self.type_of_appointment)),arrival_time,False,False,-1,-1,-1))
        elif md_choose > 0.7 and md_choose <= 0.8:
            #10% chance of them hating only 1 MD
            self.waiting_room.append(Patient(int(random.expovariate(1.0/self.type_of_appointment)),arrival_time,False,False, int(random.uniform(0,9)),-1,-1))                
        elif md_choose > 0.8 and md_choose <= 0.9:
            #10% chance of them hating 2 MD's, but they need to be unique
            md1 = int(random.uniform(0,9))
            md2 = int(random.uniform(0,9))
            while md2 == md1:
                    md2 = int(random.uniform(0,9))
            self.waiting_room.append(Patient(int(random.expovariate(1.0/self.type_of_appointment)),arrival_time,False,False,md1,md2,-1))                
        else:
            #10% chance of them hating 3 MD's, but they need to be unique, bit more work than 2 MD's
            md1 = int(random.uniform(0,9))
            md2 = int(random.uniform(0,9))
            while md2 == md1:
                    md2 = int(random.uniform(0,9))
            md3 = int(random.uniform(0,9))
            while md3 == md1 or md3 == md2:
                    md3 = int(random.uniform(0,9))
            self.waiting_room.append(Patient(int(random.expovariate(1.0/self.type_of_appointment)),arrival_time,False,False,md1,md2,md3))
                
    #creates a walk in, if its urgent or not
    def create_walkin(self, minute_count):
        random.seed(datetime.now())
        #at that point it's a 50/50 shot if it's urgent or not
        if random.random() >= 0.5:
            self.waiting_room.append(Patient(int(random.expovariate(1.0/10.0)),int(random.expovariate(1.0/15.0) + minute_count), True,True,-1,-1,-1))
        else:
            self.waiting_room.append(Patient(int(random.expovariate(1.0/10.0)),int(random.expovariate(1.0/15.0) + minute_count), False,True,-1,-1,-1))
    #populate the waiting rooms based on if its an appointment or its a walk in       
    def populate_waiting_rooms(self):
        random.seed(datetime.now())
        minute_count = 0
        while(minute_count < 450):
            #if it's less than 1/3 the patient is a walk in
            if random.random() <= 0.33:
                self.create_walkin(minute_count)
            #if its not a walk in its an appointment
            else:
                self.create_appointment(minute_count)
            minute_count += int(60/self.rate)
    #returns the patient and takes it off the stack
    def get_earliest_patient(self, waiting_room):
        earliest_index = 0
        for p in range(len(waiting_room)):
            if waiting_room[earliest_index].get_arrival_time() > waiting_room[p].get_arrival_time():
                earliest_index = p
        return waiting_room.pop(earliest_index)
    # get the earliest patient without removing it from the list
    def peek_earliest_patient(self, waiting_room):
        try:
            first = waiting_room[0]
        except IndexError:
            return 0
        for p in waiting_room:
            if first.get_arrival_time() > p.get_arrival_time():
                first = p
        return first
    #creating the file with the information
    def print_daily_info(self):
        file = open(self.title,"w") 
        file.write("\nStandard deviation, Daily Patient count , %s" % format(stdev(self.yearly_patient_count), '.2f'))
        file.write("\nMean, Daily Patient count , %s" % format(mean(self.yearly_patient_count), '.2f'))
        file.write("\nStandard deviation, Daily Patient wait time , %s" % format(stdev(self.yearly_patient_wait_time), '.2f'))
        file.write("\nMean, Daily Patient wait time , %s" % format(mean(self.yearly_patient_wait_time), '.2f'))

#paramaters set up to run    
c1 = Clinic(20, 30.0, "30.0_mean_appointment_length.csv")
c2 = Clinic(30, 15.0, "15.0_mean_appointment_length.csv")
c3 = Clinic(60, 10.0, "10.0_mean_appointment_length.csv")

c1.run_year()
c2.run_year()
c3.run_year()