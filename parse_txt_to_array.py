# This program parses the tab delimited .txt file (converted from excel) into nested dictionaries for unguided analysis
# This Python file uses the following encoding: utf-8
import os, sys

import pprint
pp=pprint.PrettyPrinter(indent=0)

file_open = open ("SKIV2L_TTC37_gene_dataset_SVM.txt","r+")
file_read = file_open.readlines()

# Variables for column locations
patient_num_col = 0
patient_name_col = 1
data_source_col = 2
#age_col = 3
#gestation_col = 4
#weight_col=5
age_onset_col = 3
#diarrhea_col =  7
#failure_to_thrive_col= 8
#facial_dysmorphism_col = 9
hair_col = 4
trichorrhexis_nodosa_col = 5
iugr_col = 6
immune_def_col = 7
peg_teeth_col = 8
skin_col = 9
cafe_au_lait_col = 10
mental_retardation_col = 11
pn_age_col = 12
pn_duration_col = 13
gene_col = 14
mutation1_type_col = 15
cdna_mutation1_col = 16
protein_mutation1_col = 17
mutation2_type_col = 18
cdna_mutation2_col = 19
protein_mutation2_col = 20
villous_atrophy_col = 21
liver_biopsy_col = 22
ethnicity_col = 23
sex_col = 24
consanguity_col = 25
outcome_col = 26
cardiac_abnormality_col = 27
thrombocytosis_col = 28
large_platelets_col = 29
skeletal_abnormaltiy_col = 30
devlpmt_delay_col = 31

# Set empty dictionary of patient to add data
patient_dict = {}
patient_def_dict = {}
mutation_dict = {}
gene_def_dict = {}

lines = file_read[0]
line_list = lines.splitlines()
# Iterate through each line in the text file, spliting the lines by the tabs
for line in line_list:
	print line
	line = line.split('#')[0]
	if len(line) == 0:
		continue
	data = line.split()
	# Split at tabs is default: i.e. empty brackets.
	# Insert space or comma in parenthesis () if that denotes separation.

	# Variables for data in column locations
	patient_num = data[patient_num_col]
	# Paper reference information
	patient_name = data[patient_name_col]
	data_source = data[data_source_col]
	# Symptom data variables
	#age = data[age_col]
	#gestation = data[gestation_col]
	#weight = data[weight_col]
	age_onset = data[age_onset_col]
	#diarrhea = data[diarrhea_col]
	#failure_to_thrive = data[failure_to_thrive_col]
	#facial_dysmorphism = data[facial_dysmorphism_col]
	hair = data[hair_col]
	trichorrhexis_nodosa = data[trichorrhexis_nodosa_col]
	iugr = data[iugr_col]
	immune_def = data[immune_def_col]
	peg_teeth = data[peg_teeth_col]
	skin = data[skin_col]
	cafe_au_lait = data[cafe_au_lait_col]
	mental_retardation = data[mental_retardation_col]
	pn_age = data [pn_age_col]
	pn_duration = data [pn_duration_col]
	# Genetic data variables
	gene = data [gene_col]
	mutation1_type = data[mutation1_type_col]
	cdna_mutation1 = data[cdna_mutation1_col]
	protein_mutation1 = data[protein_mutation1_col]
	mutation2_type = data[mutation2_type_col]
	cdna_mutation2 = data [cdna_mutation2_col]
	protein_mutation2 = data[protein_mutation2_col]
	# Symptom data continued
	villous_atrophy = data[villous_atrophy_col]
	liver_biopsy = data[liver_biopsy_col]
	ethnicity = data[ethnicity_col]
	sex = data[sex_col]
	consanguity = data[consanguity_col]
	outcome = data[outcome_col]
	cardiac_abnormality = data[cardiac_abnormality_col]
	thrombocytosis = data[thrombocytosis_col]
	large_platelets = data[large_platelets_col]
	skeletal_abnormaltiy = data[skeletal_abnormaltiy_col]
	devlpmt_delay = data[devlpmt_delay_col]




	# Create dictionary of patients 
	patient_dict [patient_num] = {'patient_num':patient_num}
	# Create dictionary of patient information to nest in patient dictionary by patient num as the key
	patient_def_dict = {'patient_num':patient_num, 'patient_name':patient_name, 'data_source':data_source, 'age_onset':age_onset, \
		'hair':hair, 'trichorrhexis_nodosa':trichorrhexis_nodosa, 'iugr':iugr, 'immune_def':immune_def,	'peg_teeth':peg_teeth, 'skin':skin, \
		'mental_retardation':mental_retardation, 'pn_age':pn_age, 'pn_duration':pn_duration, 'gene':gene, 'mutation1_type':mutation1_type,\
		'cafe_au_lait':cafe_au_lait, 'cdna_mutation1':cdna_mutation1, 'protein_mutation1':protein_mutation1, 'mutation2_type':mutation2_type,\
		'cdna_mutation2':cdna_mutation2, 'protein_mutation2':protein_mutation2, 'villous_atrophy':villous_atrophy, 'liver_biopsy':liver_biopsy,\
		'ethnicity':ethnicity, 'sex':sex, 'consanguity':consanguity, 'outcome':outcome, 'cardiac_abnormality':cardiac_abnormality,\
		'thrombocytosis':thrombocytosis, 'large_platelets':large_platelets, 'skeletal_abnormaltiy':skeletal_abnormaltiy, 'devlpmt_delay':devlpmt_delay }

	patient_dict[patient_num] = patient_def_dict
	'''
	# Create a dictionary of gene
	gene_dict = {'gene':gene}
	# Create a mutation dictionary
	if cdna_mutation1!='ND' and cdna_mutation2 != 'ND':
		for num_mutation in range(1,3,1):
			if num_mutation == 'mutation1':
				mutation_dict ['mutation_type'] = mutation1_type
				mutation_dict ['cDNA'] = cdna_mutation1
				mutation_dict ['protein'] = protein_mutation1
				mutation_dict ['gene'] = gene
				gene_def_dict[num_mutation]=mutation_dict
			elif num_mutation == 'mutation2':
				mutation_dict ['mutation_type'] = mutation2_type
				mutation_dict ['cDNA'] = cdna_mutation2
				mutation_dict ['protein'] = protein_mutation2
				mutation_dict ['gene'] = gene
				gene_def_dict[num_mutation]=mutation_dict
			gene_dict [patient_num] = gene_def_dict
	elif cdna_mutation1!='ND' and cdna_mutation2 == 'ND':
		num_mutation = 'mutation1'
		mutation_dict ['mutation_type'] = mutation1_type
		mutation_dict ['cDNA'] = cdna_mutation1
		mutation_dict ['protein'] = protein_mutation1
		mutation_dict ['gene'] = gene
		gene_def_dict[num_mutation]=mutation_dict
		gene_dict[patient_num]=gene_def_dict
	else:
		for num_mutation in range(1,3,1):
			gene_def_dict [num_mutation] = []
			gene_dict [patient_num]= gene_def_dict
	
	# Create a dictionary of symptoms
	symptom_dict = sorted({'age':age, 'gestation':gestation, 'weight':weight, 'age_onset':age_onset, 'diarrhea':diarrhea, 'failure_to_thrive':failure_to_thrive,\
		'facial_dysmorphism':facial_dysmorphism, 'hair':hair, 'trichorrhexis_nodosa':trichorrhexis_nodosa, 'iugr':iugr, 'immune_def':immune_def,\
		'peg_teeth':peg_teeth, 'skin':skin, 'mental_retardation':mental_retardation, 'pn_age':pn_age, 'pn_duration':pn_duration, 'cafe_au_lait':cafe_au_lait,\
		'villous_atrophy':villous_atrophy, 'liver_biopsy':liver_biopsy,'ethnicity':ethnicity, 'sex':sex, 'consanguity':consanguity, 'outcome':outcome,\
		'cardiac_abnormality':cardiac_abnormality, 'thrombocytosis':thrombocytosis, 'large_platelets':large_platelets, 'skeletal_abnormaltiy':skeletal_abnormaltiy,\
		'devlpmt_delay':devlpmt_delay })

	# Create a dictionary of database information
	db_dict = {'patient_name':patient_name, 'data_source':data_source}
	'''
#print '-------------symptom_dict---------------'
#pp.pprint (symptom_dict)
#print '-------------gene_dict--------------'
#pp.pprint (gene_dict)
pp.pprint (patient_dict)

file_close = file_open.close()

import numpy as np
from sklearn.preprocessing import Imputer
# Imputation of missing values
imp = Imputer(missing_values = 'NaN', strategy = 'most_frequent', axis = 0)
data_array = []
for patient in patient_dict: 
	patient_def_dict = patient_dict[patient]
	# Initially include patient num for debugging purposes
	data_list = [patient_def_dict['patient_num'], patient_def_dict['hair'], patient_def_dict['trichorrhexis_nodosa'], patient_def_dict['iugr'], patient_def_dict['immune_def'], patient_def_dict['peg_teeth'],\
		patient_def_dict['skin'], patient_def_dict['cafe_au_lait'], patient_def_dict['mental_retardation'], patient_def_dict['pn_age'], patient_def_dict['pn_duration'],\
		patient_def_dict['villous_atrophy'], patient_def_dict['sex'], patient_def_dict['consanguity'], patient_def_dict['outcome'], patient_def_dict['cardiac_abnormality'],\
		patient_def_dict['thrombocytosis'], patient_def_dict['large_platelets'], patient_def_dict['skeletal_abnormaltiy'], patient_def_dict['devlpmt_delay']]
	#print data_list
	#line_array = np.array(data_list)
	data_array.append(data_list)
data_array.sort()
print data_array
booleans = [[np.nan if item=='ND' else item for item in each_list[:]] for each_list in data_array]
#print booleans
#print (data_array)
fitted_data_array = imp.fit(booleans)
final_data_array = imp.transform(booleans)
print final_data_array
# Support Vector Machine (SVM) analysis
import matplotlib.pyplot as plt
from sklearn import svm
from matplotlib import style
style.use("ggplot")
#clf is classifier
# X = array of features
X=np.array(final_data_array)
# y =array of labels
y=[]
for patient in patient_dict:
	patient_def_dict = patient_dict[patient]
	y.append(patient_def_dict['patient_num'])
y.sort()
#print y
clf=svm.SVC(kernel='linear', C = 1.0)
clf.fit(X,y)
# code to plot results if only 2 data sets or X had 2 components instead of 12
# w = clf.coef_[0]
# print w
# a = -w[0]/w[1]
# xx = np.linspace(0,49)
# yy = a * xx - clf.intercept_[0] / w[1]