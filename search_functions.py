import re
import os.path
import os, sys
import shutil
import pandas
from StringIO import StringIO
from format_conversion_functions import CSVFormatConversion, dotFormatConversion, dashFormatConversion, snpFormatConversion
import random

def do_search(org_1, org_2, format, org_1_ranges, org_2_ranges, snpRange1, snpRange2):
	
	#Convert the range input to the proper csv format
	#if format == "csv":
	#	org_1_ranges = CSVFormatConversion(org_1_ranges_input)
	#	org_2_ranges = CSVFormatConversion(org_2_ranges_input)
	#
	#if format == "dots":
	#	org_1_ranges = dotFormatConversion(org_1_ranges_input)
	#	org_2_ranges = dotFormatConversion(org_2_ranges_input)
	#	
	#if format == "dash":
	#	org_1_ranges = dashFormatConversion(org_1_ranges_input)
	#	org_2_ranges = dashFormatConversion(org_2_ranges_input)
	#	
	#if format == "snp":
	#	#range = request.form['range'] #Fix This
	#	org_1_ranges = snpFormatConversion(org_1_ranges_input, snpRange1)
	#	org_2_ranges = snpFormatConversion(org_2_ranges_input, snpRange2)
	#	
	#if format == "done":
	#	org_1_ranges = org_1_ranges_input
	#	org_2_ranges = org_2_ranges_input
		
	#Convert the range searches into searchable objects
	search1 = pandas.read_csv(StringIO(org_1_ranges))
	search2 = pandas.read_csv(StringIO(org_2_ranges))
	
	#select the right data file (automatic based on org inputs)
	org_1 = org_1.replace(" ", "-");
	org_2 = org_2.replace(" ", "-");
	
	selected_species_list = [org_1, org_2]
	
	species_data_file = "static/data/" + selected_species_list[0] + "_" + selected_species_list[1] + ".csv"
	
	if os.path.isfile(species_data_file):
		df = pandas.read_csv(species_data_file)
	
		#Get relevant rows from org1 search ranges
		full1 = pandas.DataFrame()
		for index, row in search1.iterrows():
			tmp = df[(df["Homolog > Gene 1 > Chromosome Location . Start"] >= row[1]) & (df["Homolog > Gene 1 > Chromosome Location . End"] <= row[2]) & (df["Homolog > Gene 1 > Chromosome > Name"].map(lambda x: x.lstrip('Chromosomechromosome0')) == str(row[0]).lstrip('Chromosomechromosome0'))] 
			full1 = full1.append(tmp)
	
		#Get relevant rows from org2 search ranges
		full2 = pandas.DataFrame()
		for index, row1 in search2.iterrows():
			tmp = df[(df["Homolog > Gene 2 > Chromosome Location . Start"] >= row1[1]) & (df["Homolog > Gene 2 > Chromosome Location . End"] <= row1[2]) & (df["Homolog > Gene 2 > Chromosome > Name"].map(lambda x: x.lstrip('Chromosomechromosome0')) == str(row1[0]).lstrip('Chromosomechromosome0'))]
			full2 = full2.append(tmp)

		#Final list of orthologous genes
		ortho = pandas.merge(full1, full2, how='inner')
		ortho.drop_duplicates(inplace=True)
	
		return ortho
		
	else:
		return -1