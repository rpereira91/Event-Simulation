from clinic import Clinic

a = Clinic(0.0,False, False,"No_lates.csv")
b = Clinic(0.0,True, False,"Lates_0_General_Visits.csv")
c = Clinic(0.05,True, False,"Lates_5_General_Visits.csv")
d = Clinic(0.1,True, False,"Lates_10_General_Visits.csv")
a1 = Clinic(0.0,False, True,"No_lates_greedy.csv")
b1 = Clinic(0.0,True, True,"Lates_0_General_Visits_greedy.csv")
c1 = Clinic(0.05,True, True,"Lates_5_General_Visits_greedy.csv")
d1 = Clinic(0.1,True, True,"Lates_10_General_Visits_greedy.csv")
a.run_for_days(250)
b.run_for_days(250)
c.run_for_days(250)
d.run_for_days(250)
a1.run_for_days(250)
b1.run_for_days(250)
c1.run_for_days(250)
d1.run_for_days(250)