# This program parses the tab delimited .txt file (converted from excel) into nested dictionaries for unguided analysis
# This Python file uses the following encoding: utf-8
import os, sys

import pprint
pp=pprint.PrettyPrinter(indent=0)

file_open = open ("SKIV2L_TTC37_data_set.txt","r+")
file_read = file_open.readlines()

# Variables for column locations
patient_num_col = 0
patient_name_col = 1
data_source_col = 2
age_col = 3
gestation_col = 4
weight_col=5
age_onset_col = 6
diarrhea_col =  7
failure_to_thrive_col= 8
facial_dysmorphism_col = 9
hair_col = 10
trichorrhexis_nodosa_col = 11
iugr_col = 12
immune_def_col = 13
peg_teeth_col = 14
skin_col = 15
cafe_au_lait_col = 16
mental_retardation_col = 17
pn_age_col = 18
pn_duration_col = 19
gene_col = 20
mutation1_type_col = 21
cdna_mutation1_col = 22
protein_mutation1_col = 23
mutation2_type_col = 24
cdna_mutation2_col = 25
protein_mutation2_col = 26
villous_atrophy_col = 27
liver_biopsy_col = 28
ethnicity_col = 29
sex_col = 30
consanguity_col = 31
outcome_col = 32
cardiac_abnormality_col = 33
thrombocytosis_col = 34
large_platelets_col = 35
skeletal_abnormaltiy_col = 36
devlpmt_delay_col = 37

# Set empty dictionary of patient to add data
patient_dict = {}
patient_def_dict = {}
mutation_dict = {}
gene_def_dict = {}

# Iterate through each line in the text file, spliting the lines by the tabs
for line in file_read:
	#line = line.split('#')[0]
	#if len(line) == 0:
	#	continue
	data = line.split()
	# Split at tabs is default: i.e. empty brackets.
	# Insert space or comma in parenthesis () if that denotes separation.

	# Variables for data in column locations
	patient_num = data[patient_num_col]
	# Paper reference information
	patient_name = data[patient_name_col]
	data_source = data[data_source_col]
	# Symptom data variables
	age = data[age_col]
	gestation = data[gestation_col]
	weight = data[weight_col]
	age_onset = data[age_onset_col]
	diarrhea = data[diarrhea_col]
	failure_to_thrive = data[failure_to_thrive_col]
	facial_dysmorphism = data[facial_dysmorphism_col]
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
	thrombocytosis = data[thrombocytosis]
	large_platelets = data[large_platelets_col]
	skeletal_abnormaltiy = data[skeletal_abnormaltiy_col]
	devlpmt_delay = data[devlpmt_delay_col]




	# Create dictionary of patients 
	patient_dict [patient_num] = {'patient_num':patient_num}
	# Create dictionary of patient information to nest in patient dictionary by patient num as the key
	patient_def_dict = {'patient_num':patient_num, 'patient_name':patient_name, 'data_source':data_source, 'age':age, 'gestation':gestation,\
		'weight':weight, 'age_onset':age_onset, 'diarrhea':diarrhea, 'failure_to_thrive':failure_to_thrive, \
		'facial_dysmorphism':facial_dysmorphism, 'hair':hair, 'trichorrhexis_nodosa':trichorrhexis_nodosa, 'iugr':iugr, 'immune_def':immune_def,\
		'peg_teeth':peg_teeth, 'skin':skin, 'mental_retardation':mental_retardation, 'pn_age':pn_age, 'pn_duration':pn_duration, 'gene':gene,\
		'mutation1_type':mutation1_type, 'cafe_au_lait':cafe_au_lait, 'cdna_mutation1':cdna_mutation1, 'protein_mutation1':protein_mutation1,\
		'mutation2_type':mutation2_type, 'cdna_mutation2':cdna_mutation2, 'protein_mutation2':protein_mutation2, 'villous_atrophy':villous_atrophy,\
		'liver_biopsy':liver_biopsy, 'ethnicity':ethnicity, 'sex':sex, 'consanguity':consanguity, 'outcome':outcome, 'cardiac_abnormality':cardiac_abnormality,\
		'thrombocytosis':thrombocytosis, 'large_platelets':large_platelets, 'skeletal_abnormaltiy':skeletal_abnormaltiy, 'devlpmt_delay':devlpmt_delay }

	patient_dict[patient_num] = patient_def_dict
	
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

pp.pprint (gene_dict)
pp.pprint (patient_dict)
file_close = file_open.close()