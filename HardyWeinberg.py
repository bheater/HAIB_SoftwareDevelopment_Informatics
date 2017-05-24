from __future__ import division
import csv
import numpy as np

with open('exac_parsed.tsv','rb') as tsvin, open('new.csv', 'wb') as csvout:
	tsvin = csv.reader(tsvin, delimiter='\t')
	csvout = csv.writer(csvout)
	
	for i, row in enumerate(tsvin):
		#print row
		if i >= 2:
			#adjusted AC and AN were used because they corresponded to AC_Het and AC_Hom
			alleleCount = int(row[7]) 
			alleleNum = int(row[15])
			#print "alleleCount = "+str(alleleCount)+"\talleleNum = "+str(alleleNum)

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
			alleleCountHet = int(row[23])
			alleleCountHom = int(row[31])
			verify = alleleCountHet+2*alleleCountHom
			#print "Verify: " + str(verify) +" =? "+ str(alleleCount)
			while True:
				try:
					verify == alleleCount
					break
				except ValueError:
					print "ERROR AC_Het + 2*AC_Hom: "+ str(verify)+ "~= alleleCount: "+str(alleleCount)
			# Observation 2
			# Total population is the 1/2 of the total number of alleles, since humans are diploid
			totalPop = alleleNum/2
			obs_p_sqr = alleleCountHom/totalPop
			obs_pq2 = alleleCountHet/totalPop
			obs_q_sqr = 1-obs_p_sqr-obs_pq2
			obs_sum = obs_p_sqr+obs_pq2+obs_q_sqr
			#print "Observed: "+str(obs_p_sqr)+" + "+str(obs_pq2)+" + "+str(obs_q_sqr)+" = "+str(obs_sum)

			# Determine if the observed data is significantly different than the expected data
			alpha = 0.005
			expected = [p_sqr, pq2, q_sqr]
			observed = [obs_p_sqr, obs_pq2, obs_q_sqr]
			diff = np.absolute(np.array(expected)-np.array(observed))
			#print diff
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



			#break
			
