# This program filters patient screening demographic information based on patient numbers
from sys import argv


patno_file_open = open('PATNO_extremes.csv', 'r')
patno_file_read = patno_file_open.readlines()
patno_str = patno_file_read[0]
patno_list = patno_str.split(',')
#print 'patno_list = ',patno_list
num_patno = len(patno_list)
print 'Number of PATNO in patno_list= ', num_patno
patno_file_open.close

filter_file_data = argv[1]
filter_file_name = filter_file_data+'.txt'

# Open file with information on all patients
file_open = open(filter_file_name, 'r')
# Read the file contents line by line, since each line correspconds to 1 patno
file_read = file_open.readlines()
#file_list = file_read.splitlines()
#print file_list
# Count the number of initial patients (lines)  
# compare to final number of patients with exome data
num_lines = len(file_read)
num_init_pat = num_lines
print "num_init_pat = ",num_init_pat
output_file_name = 'exome_extremes_'+filter_file_name
print output_file_name
exome_patient_file = open(output_file_name,'w+')

#file_read= file_read[0]
#print file_list
#print 'titles = ',titles
#print file_read

for line in file_read:
	line_list = line.splitlines()
	titles = line_list[0]

	print titles
	all_data = line_list[1:]
	#print all_data
	for lines in all_data:
		tab = lines.split()
		patno = tab[2]
		#print lines

		# Determine whether patno in patno list, if so write line to file
		if patno in patno_list:
			exome_patient_file.write(lines+'\n')
	
	#for item in patno_list:
		#if item == patno:
			#exome_patient_file.write(line_str+'\n')
			#print 'patno found in ScreeningDemographics.csv'


# Count final number of patients in newly written file
exome_patient_file.close
exome_patient_file = open(output_file_name,'r')
new_file_read = exome_patient_file.readlines()
#print new_file_read
new_num_lines = len(new_file_read)
num_exome_pat = new_num_lines
print "num_exome_pat = ", num_exome_pat
print num_exome_pat, 'patno found in ', output_file_name
exome_patient_file.close
file_open.close

with file(output_file_name, 'r') as original: data = original.read()
with file(output_file_name, 'w') as modified: modified.write(titles +'\n'+ data)

# run with
# python filter_csv_by_patno_severe_cases.py <filename>
# python filter_csv_by_patno_severe_cases.py Use_of_PD_Medication
# python filter_csv_by_patno_severe_cases.py Initiation_of_PD_Medication-_incidents
# python filter_csv_by_patno_severe_cases.py Concomitant_Medications