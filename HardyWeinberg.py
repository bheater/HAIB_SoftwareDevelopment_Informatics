from __future__ import division
import csv
import numpy as np
from scipy.stats import chisquare

with open('exac_parsed.tsv','rb') as tsvin, open('new.csv', 'wb') as csvout:
	tsvin = csv.reader(tsvin, delimiter='\t')
	csvout = csv.writer(csvout)
	
	# Counter for the number of inconsistent data points.
	num_inconsistent = 0
	max_diff=0
	for i, row in enumerate(tsvin):
		#print row
		if i >= 2:
			#adjusted AC and AN were used because they corresponded to AC_Het and AC_Hom
			alleleCount = int(row[7]) 
			alleleNum = int(row[15])
			#print "alleleCount = "+str(alleleCount)+"\talleleNum = "+str(alleleNum)

			# Verify that AC_Het+2*AC_Hom == alleleCount
			alleleCountHet = int(row[23])
			alleleCountHom = int(row[31])
			verify = alleleCountHet+2*alleleCountHom
			#print "Verify: " + str(verify) +" =? "+ str(alleleCount)
			# If C_Het+2*AC_Hom == alleleCount, continue with calculations
			try:
				assert(verify == alleleCount)
				pass
			# If C_Het+2*AC_Hom ~= alleleCount, set allelCount = verify to keep calcs consistent
			# and count the number of inconsistent data points
			except:
				position = int(row[1])
				print "ERROR AC_Het + 2*AC_Hom: "+ str(verify)+ "~= alleleCount: "+str(alleleCount)+" @ position "+str(position)
				diff_inconsistent = abs(alleleCount-verify)
				print "Difference b/w alleleCount and AC_Het + 2*AC_Hom = "+ str(diff_inconsistent)
				alleleCount = verify
				# count the number of inconsistencies
				num_inconsistent = num_inconsistent+1
				if diff_inconsistent>max_diff:
					max_diff = diff_inconsistent
				#exit()

			alleleFreq = alleleCount/alleleNum
			#print "alleleFreq = alleleCount/alleleNum = " +str(alleleFreq)

			# Hardy-Weinberg Calculation
			# p: reference allele	q = alternate allele
			p = alleleFreq
			q = (alleleNum-alleleCount)/alleleNum
			p_sqr = p*p
			pq2 = 2*p*q
			q_sqr = q*q
			sumHW = p_sqr+ pq2 + q_sqr
			#print "Expected: "+str(p_sqr)+" + "+str(pq2)+" + "+str(q_sqr)+" = "+str(sumHW)

			# Compare to known data from ExAC
			# Observation 2
			# Total population is the 1/2 of the total number of alleles, since humans are diploid
			totalPop = alleleNum/2
			obs_p_sqr = alleleCountHom/totalPop
			obs_pq2 = alleleCountHet/totalPop
			obs_q_sqr = 1-obs_p_sqr-obs_pq2
			obs_sum = obs_p_sqr+obs_pq2+obs_q_sqr
			#print "Observed: "+str(obs_p_sqr)+" + "+str(obs_pq2)+" + "+str(obs_q_sqr)+" = "+str(obs_sum)

			# Determine if the observed data is significantly different than the expected data
			expected = [p_sqr, pq2, q_sqr]
			observed = [obs_p_sqr, obs_pq2, obs_q_sqr]

			results = chisquare(np.array(observed),f_exp=np.array(expected))
			chisq = results[0]
			Pval = results[1]
			#print "Chi-Squared = "+str(chisq) + "\t P value = "+str(Pval)
			'''
			diff = np.absolute(np.array(expected)-np.array(observed))
			alpha = 0.005
			if np.any(diff)>alpha:
				if abs(diff[0])>alpha:
					print "Significant diffrerence b/w p-squared expected and observed: " + str(diff[0])
				elif abs(diff[1])>alpha:
					print "Significant diffrerence b/w 2pq expected and observed: " + str(diff[1])
				elif abs(diff[2])>alpha:
					print "Significant diffrerence b/w q-squared expected and observed: " + str(diff[2])

			diff_p_sqr = abs(p_sqr-obs_p_sqr)
			if diff_p_sqr>alpha:
				print "Populatation size: "+ str(totalPop)
				if p_sqr>obs_p_sqr:
					print "Expected p^2("+str(p_sqr)+") > Observed p^2 (" + str(obs_p_sqr) +")"
				else:
					print "Expected p^2("+str(p_sqr)+") < Observed p^2 (" + str(obs_p_sqr) +")"
			'''
	print "num_inconsistent = " +str(num_inconsistent)
	total_variants = i-2
	print "total entries = " + str(total_variants)
	inconsistency_rate = num_inconsistent/total_variants
	print "inconsistency rate = " + str(inconsistency_rate)
	print "max difference in inconsistency = "+ str(max_diff)
			
