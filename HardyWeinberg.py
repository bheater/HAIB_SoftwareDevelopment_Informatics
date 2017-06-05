#!/usr/bin/env python
from __future__ import division
import csv
import json
import numpy as np
from scipy.stats import chisquare
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from pprint import pprint

# Counter for the number of inconsistent data points.


def parseExacTsv(filename, num_inconsistent, inconsistencies,chisq_vals,Pvals):
	# Pull and Parse ExAC Data for Calculations
	with open(filename,'rb') as tsvin, open('exacChromPosPval.tsv', 'wb') as tsvout:
		tsvin = csv.reader(tsvin, delimiter='\t')
		tsvout = csv.writer(tsvout, delimiter='\t')

		for i, row in enumerate(tsvin):
			#print row
			if i >= 2:
				chrom = str(row[0])
				position = int(row[1])
				#adjusted AC and AN were used because they corresponded to AC_Het and AC_Hom
				alleleCount = int(row[7]) 
				alleleNum = int(row[15])
				#print "alleleCount = "+str(alleleCount)+"\talleleNum = "+str(alleleNum)

				# Verify that AC_Het+2*AC_Hom == alleleCount
				alleleCountHet = int(row[23])
				alleleCountHom = int(row[31])
				num_inconsistent=HWcalcExac(alleleCount,alleleNum,alleleCountHet,alleleCountHom,num_inconsistent, inconsistencies,chisq_vals,Pvals)
				tsvout.writerow([chrom,position,Pvals[-1]])
				#print [chrom,position,Pvals[-1]]
	return num_inconsistent



def HWcalcExac(alleleCount,alleleNum,alleleCountHet,alleleCountHom,num_inconsistent,inconsistencies,chisq_vals,Pvals):

	verify = alleleCountHet+2*alleleCountHom
	#print "Verify: " + str(verify) +" =? "+ str(alleleCount)
	# If C_Het+2*AC_Hom == alleleCount, continue with calculations
	try:
		assert(verify == alleleCount)
		diff_inconsistent = 0
		inconsistencies.append(diff_inconsistent)
		pass
	# If C_Het+2*AC_Hom ~= alleleCount, set allelCount = verify to keep calcs consistent
	# and count the number of inconsistent data points
	except:
		diff_inconsistent = abs(alleleCount-verify)
		inconsistencies.append(diff_inconsistent)
		#print "Difference b/w alleleCount and AC_Het + 2*AC_Hom = "+ str(diff_inconsistent)
		alleleCount = verify
		# count the number of inconsistencies
		num_inconsistent = num_inconsistent+1
	alleleFreq = alleleCount/alleleNum
	#print "alleleFreq = alleleCount/alleleNum = " +str(alleleFreq)
	totalPop = alleleNum/2

	# Hardy-Weinberg Calculation
	# p: reference allele	q = alternate allele
	p = alleleFreq
	q = (alleleNum-alleleCount)/alleleNum
	p_sqr = p*p*totalPop
	pq2 = 2*p*q*totalPop
	q_sqr = q*q*totalPop
	sumHW = p_sqr+ pq2 + q_sqr
	#print "Expected: "+str(p_sqr)+" + "+str(pq2)+" + "+str(q_sqr)+" = "+str(sumHW)

	# Compare to known data from ExAC
	# Observation 2
	# Total population is the 1/2 of the total number of alleles, since humans are diploid
	obs_p_sqr = alleleCountHom
	obs_pq2 = alleleCountHet
	obs_q_sqr = totalPop - obs_p_sqr-obs_pq2
	obs_sum = obs_p_sqr+obs_pq2+obs_q_sqr
	#print "Observed: "+str(obs_p_sqr)+" + "+str(obs_pq2)+" + "+str(obs_q_sqr)+" = "+str(obs_sum)

	# Determine if the observed data is significantly different than the expected data
	expected = [p_sqr, pq2, q_sqr]
	observed = [obs_p_sqr, obs_pq2, obs_q_sqr]

	results = chisquare(np.array(observed),f_exp=np.array(expected))
	chisq = results[0]
	chisq_vals.append(chisq)
	Pval = results[1]
	#if Pval<0.6:
		#print Pval, expected,observed
	Pvals.append(Pval)
	#stats.append(results)
	return num_inconsistent


if __name__ == "__main__":
	num_inconsistent = 0
	inconsistencies = []
	Pvals = []
	chisq_vals = []

	exac_filename='exac_parsed.tsv'
	exac_filelist = [exac_filename]
	file_num = 0
	total_files = len(exac_filelist) 
	while file_num<total_files:
		#print filelist[file_num]
		num_inconsistent=parseExacTsv(exac_filelist[file_num],num_inconsistent, inconsistencies,chisq_vals,Pvals)
		if file_num>0:
			num_inconsistent +=num_inconsistent
		#chisq_vals, Pvals, inconsistencies=HWcalc(alleleCount,alleleNum,alleleCountHet,alleleCountHom,i,num_inconsistent)
		file_num=file_num+1
	print "num inconsistencies = "+ str(num_inconsistent)
	total_variants = len(inconsistencies)
	print "total entries = " + str(total_variants)
	inconsistency_rate = num_inconsistent/total_variants
	print "inconsistency rate = " + str(inconsistency_rate)
	print "max difference in inconsistency = "+ str(max(inconsistencies))
	# Writing JSON data
	with open('ExAC_inconsistencies.json', 'w') as f:
		json.dump(inconsistencies, f)
	with open('ExAC_Pval.json', 'w') as f:
		json.dump(Pvals, f)
	n, bins, patches = plt.hist(inconsistencies,bins=[0, 10, 100, 1000, 10000, 100000, 1000000])
	plt.xlabel('Magnitude of Inconsistency')
	plt.ylabel('Occurances')
	plt.title(r'Histogram of Inconsistencies')
	#plt.axis([0, 50000, 0, 0.03])
	plt.grid(True)
	plt.xscale('symlog')
	plt.yscale('symlog')
	plt.show()

# add manhattan plot of the pvalues


