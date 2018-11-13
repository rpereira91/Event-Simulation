from clinic import Clinic

clinics = []
for i in range(1,22):
    title = str(i) + "_Doctors.csv"
    clinics.append(Clinic(i))
    clinics[i-1].run_year(title)