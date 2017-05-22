import json
from pprint import pprint

with open('CompareAlleleFreq/codi_filtered_json/MCW2015-000554_codi_filtered.json') as data_file:    
    data = json.load(data_file)

#pprint(data.keys())

total_entries =len(data["children"])


for entry in data["children"]:
	gene_id = entry["id"]
	print "gene id: " +gene_id
	gene_name = entry["name"]
	print "gene name: "+ gene_name
	variant_id = entry["children"][0]["id"]
	print"variant_id: "+variant_id
	variant_name = entry["children"][0]["name"]
	print"variant_name: "+variant_name
	exac = entry["children"][0]["ExAC"]
	print "Allel Freq: "+ exac
print "total_entries: "+str(total_entries)+'\n'

