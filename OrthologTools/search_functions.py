from OrthologTools import app
import re
import os.path
import os, sys
import shutil
import pandas
from StringIO import StringIO
from format_conversion_functions import CSVFormatConversion, dotFormatConversion, dashFormatConversion, snpFormatConversion
import random

def do_search(org_1, org_2, search1, search2, type):
		
	#select the right data file (automatic based on org inputs)
	org_1 = org_1.replace(" ", "-");
	org_2 = org_2.replace(" ", "-");
	
	selected_species_list = [org_1, org_2]
	
	#species_data_file = "OrthologTools/static/data/" + selected_species_list[0] + "_" + selected_species_list[1] + ".csv"
	species_data_file = app.config['DATA_DIR'] + selected_species_list[0] + "_" + selected_species_list[1] + ".csv"
        	
	if os.path.isfile(species_data_file):
		df = pandas.read_csv(species_data_file)
	
		#Get relevant rows from org1 search ranges
		full1 = pandas.DataFrame()
		for index, row in search1.iterrows():
			tmp = df[(df["Homolog > Gene 1 > Chromosome Location . Start"] >= row[1]) & (df["Homolog > Gene 1 > Chromosome Location . End"] <= row[2]) & (df["Homolog > Gene 1 > Chromosome > Name"].map(lambda x: x.lstrip('Chromosomechromosome0')) == str(row[0]).lstrip('Chromosomechromosome0'))] 
			full1 = full1.append(tmp)
	
  		print "----1----"
  		print full1.apply(pandas.Series.nunique)
  	
	
		#Get relevant rows from org2 search ranges
		full2 = pandas.DataFrame()
		for index, row1 in search2.iterrows():
			tmp = df[(df["Homolog > Gene 2 > Chromosome Location . Start"] >= row1[1]) & (df["Homolog > Gene 2 > Chromosome Location . End"] <= row1[2]) & (df["Homolog > Gene 2 > Chromosome > Name"].map(lambda x: x.lstrip('Chromosomechromosome0')) == str(row1[0]).lstrip('Chromosomechromosome0'))]
			full2 = full2.append(tmp)
			
		print "----2----"
  		print full2.apply(pandas.Series.nunique)

		#Final list of orthologous genes
		ortho = pandas.merge(full1, full2, how='inner')
		ortho.drop_duplicates(inplace=True)
	
		return ortho
		
	else:
		return -1
