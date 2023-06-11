import numpy as np
import matplotlib.pyplot as plt

def extract_data(filename, line_start, element_loc):
    Mg_Fe_abundances = []
    with open(filename, "r") as f:
        lines = f.readlines()

        for l in lines[line_start:]:
            Mg_Fe_abundances.append(l.split()[element_loc])

    return(Mg_Fe_abundances)





#main program
file = "OneDrive/Documents/Physics/Year4/Project/Open box/JINAPyCEE/solar_Mg_Fe.txt"

datas = extract_data(file, line_start=7, element_loc=2)
MgFe_array = []
for num in datas:
    MgFe_array.append(float(num))

np.array(MgFe_array)

MgFe_plot_data = np.array(MgFe_array)
#print(MgFe_plot_data)

file_2 = "OneDrive/Documents/Physics/Year4/Project/Open box/JINAPyCEE/age_data_file.txt"

age_data = extract_data(file_2, line_start = 9, element_loc=2)

age_data_array = []

for age in age_data:
    age_data_array.append(float(age))

obs_age = np.array(age_data_array)

#print(obs_age)

age_data_error = extract_data(file_2, line_start=9, element_loc=3)
error_array = []
for error in age_data_error:
    error_array.append(float(error))

error_plot = np.array(error_array)

#print(error_plot)