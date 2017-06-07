#!/usr/bin/env python
from __future__ import division
import csv
import json
import numpy as np
from scipy.stats import chisquare
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from pprint import pprint
import os
import glob
import math


# Pull and Parse GNomad Data for Calculations
# /gnomad/genome

def readGnomad(filename,alleleCount0,alleleNum0,chisq,Pval,negLog10):


	with open(filename,'rb') as tsvin, open('gnomadChromPosPval02.tsv', 'wb') as tsvout, open('gnomadHW02.csv', 'wb') as csvout:
		tsvin = csv.reader(tsvin, delimiter='\t')
		tsvout = csv.writer(tsvout, delimiter='\t')
		csvout = csv.writer(csvout, delimiter=',')
		
		# Counter for the number of inconsistent data points.

		for i, row in enumerate(tsvin):
			#if '00'in filename and i >= 2 or '00' not in filename:
			# add if statement below for first file
			#if i>=2:
			# No adjusted data in gnomad
			chrom = int(row[0])
			position = int(row[1])
			ref = str(row[2])
			alt = str(row[3])
			alleleCount = int(row[4]) 
			alleleNum = int(row[5])
			#print "alleleCount = "+str(alleleCount)+"\talleleNum = "+str(alleleNum)
			alleleCountHom = int(row[6])
			alleleCountHemi = int(row[7])

			# hemizygous: sex chromosomes for Male individuals only have 1 X,
			# so they can only be hemizygous at those loci (minus the psuedoautosomal regions)
			# so that value should be zero for anything that is not on X

			if alleleNum != int(0) and alleleCount != int(0):
				expected, observed = HWcalcGnomad(alleleCount,alleleNum,alleleCountHemi,alleleCountHom,chisq,Pval,negLog10)
				# chisq.append(results[0])
				# Pval.append(results[1])
				#print [chrom,position,Pval[-1]]
				#print [chrom,position,ref,alt,expected[0], expected[1], expected[2], observed[0], observed[1], observed[2],Pval[-1]]
				tsvout.writerow([chrom,position,Pval[-1]])
				csvout.writerow([chrom,position,ref,alt,expected[0], expected[1], expected[2], observed[0], observed[1], observed[2],negLog10[-1]])

			else:
				if alleleNum == 0:
					alleleNum0 = alleleNum0+1
					assert alleleCountHom==0 & alleleCountHemi==0, "alleleNum == 0: alleleCountHemi or alleleCountHom !=0"

				if alleleCount==0:
					alleleCount0 = alleleCount0+1
					assert alleleCountHom==0 & alleleCountHemi==0, "alleleCount==0: alleleCountHemi or alleleCountHom !=0"
	return alleleNum0,alleleCount0

def HWcalcGnomad(alleleCount,alleleNum,alleleCountHemi,alleleCountHom,chisq,Pval,negLog10):
	

	alleleFreq = alleleCount/alleleNum
	#print alleleFreq


	# Calculate the count of Heterozygotes at a given location 
	# Het. count = alt. allele count (AC) - ((Hom. count * 2) + Hemi. count)
	alleleCountHet = alleleCount-((alleleCountHom*2)+alleleCountHemi)

	totalPop = alleleNum/2
	# Hardy-Weinberg Calculation
	# p: reference allele	q = alternate allele
	p = alleleFreq
	q = (alleleNum-alleleCount)/alleleNum
	p_sqr = p*p*totalPop
	pq2 = 2*p*q*totalPop
	q_sqr = q*q*totalPop
	#sumHW = p_sqr+ pq2 + q_sqr
	#print "Expected: "+str(p_sqr)+" + "+str(pq2)+" + "+str(q_sqr)+" = "+str(sumHW)

	# Compare to known data from GNomad
	# Observation 2
	# Total population is the 1/2 of the total number of alleles, since humans are diploid
	obs_p_sqr = alleleCountHom
	obs_pq2 = alleleCountHet
	obs_q_sqr = totalPop-obs_p_sqr-obs_pq2
	#obs_sum = obs_p_sqr+obs_pq2+obs_q_sqr
	#print "Observed: "+str(obs_p_sqr)+" + "+str(obs_pq2)+" + "+str(obs_q_sqr)+" = "+str(obs_sum)

	# Determine if the observed data is significantly different than the expected data
	expected = [p_sqr, pq2, q_sqr]
	observed = [obs_p_sqr, obs_pq2, obs_q_sqr]
	results = chisquare(np.array(observed),f_exp=np.array(expected))
	chisq.append(results[0])
	Pval.append(results[1])
	if math.isinf(abs(np.log10(results[1]))):
		negLog10.append(10000)
	else:
		negLog10.append(abs(np.log10(results[1])))

	return expected, observed
	#print results
	#return results


if __name__ == "__main__":

	chisq = []
	Pval = []
	negLog10 = []
	alleleCount0 = 0
	alleleNum0 = 0

	path = 'gnomad/genome/*.tsv'
	#for filename in glob.glob(path):
	filename = 'gnomad/genome/gnomadgenomeparsed_part02.tsv'
	# below goes in for loop above
	print 'Reading ' + filename + ' and calculating the Hardy-Weinberg frequencies'
	alleleNum0, alleleCount0=readGnomad(filename,alleleCount0,alleleNum0,chisq,Pval,negLog10)
	alleleNum0 += alleleNum0
	alleleCount0 += alleleCount0
	print 'alleleNum0 = '+str(alleleNum0)+'\talleleCount0 = '+str(alleleCount0) 
	# print 'chisq \n'
	# print chisq
	# print'Pval \n'
	# print Pval
	# end for loop code
	# with open('GNomad_Pval.json', 'w') as f:
	# 	json.dump(Pval, f)


	total_variants = len(chisq)
	print "total entries = " + str(total_variants)
	print "alleleCount0 = "+ str(alleleCount0)
	print "alleleNum0 = " + str(alleleNum0)
	'''
	# Writing JSON data
	Pval_output_filename = orig_filename.split('.')[0]+'GNomad_Pval.json'
	print 'output_filename' + output_filename
	with open(output_filename, 'w') as f:
		json.dump(Pval, f)
	'''