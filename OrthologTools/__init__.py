from flask import Flask, render_template, request, url_for, make_response
import pandas
from StringIO import StringIO
from format_conversion_functions import CSVFormatConversion, dotFormatConversion, dashFormatConversion, snpFormatConversion
import random
from random_data_functions import generateRandom, generate_one_range
import re
import os.path
import os, sys
import shutil
from search_functions import do_search

app = Flask(__name__)

@app.route('/')
def index():

	speciesList = {'A. thaliana', 'Z. mays', 'S. bicolor', 'G. max'};
	return render_template('home.html', speciesList=speciesList)
	
@app.route('/search_step_1')
def start_search():
	speciesList = {'A_thaliana', 'Z_mays', 'S_bicolor', 'G_max', 'O_sativa'};
	return render_template('start_search.html', speciesList=speciesList)
	
@app.route('/random')
def random_data():
	speciesList = {'A. thaliana', 'Z. mays', 'S. bicolor', 'G. max'};
	return render_template('random_data.html', speciesList=speciesList)
	
@app.route('/return_random', methods=['POST'])
def return_random():

	maize = [10,301354135,237068873,232140174,241473504,217872852,169174353,176764762,175793759,156750706,150189435];
	arabidopsis = [5,30427671,19698289,23459830,18585056,26975502];
	sorghum = [10,73933847,78027413,74539055,68108026,62428788,62294152,64407977,55559831,59722314,61076732];
	soybean = [20,55915595,51656713,47781076,49243852,41936504,50722821,44683157,46995532,46843750,50969635,39172790,40113140,44408971,49711204,50939160,37397385,41906774,62308140,50589441,46773167];

	organism = request.form['organism']
	org_1_ranges_input = request.form['org_1_ranges']
	
	arr = [];
	
	if organism == 'A. thaliana':
		arr = arabidopsis
	
	if organism == 'Z. mays':
		arr = maize
		
	if organism == 'S. bicolor':
		arr = sorghum

	if organism == 'G. max':
		arr = soybean
		
	
	#tmp = generateRandom(org_1_ranges_input, arr)
	pathName = generateRandom(org_1_ranges_input, arr)
	
	#for line in tmp:
		#print line
		
	fileToDownload = open(pathName + "results.zip")
	fileToDownloadContents = fileToDownload.read()
	
	response = make_response(fileToDownloadContents)
	response.headers["Content-Disposition"] = "attachment; filename=" + "results.zip"	
	
	return response
	
@app.route('/search', methods=['POST'])
def search():
	arr1 = [];
	arr2 = [];
	
	org_dict = {
		'Z_mays' : ['Z.-mays-AGPv3-5b+'],
		'C_papaya' : ['C.-papaya-r.Dec2008-ASGPBv0.4'],
		'V_vinifera' : ['V.-vinifera-Genoscope.12X-Genoscope.12X'],
		'S_lycopersicum' : ['S.-lycopersicum-iTAGv2.40-iTAGv2.3'],
		'M_truncatula' : ['M.-truncatula-Mt4.0-Mt4.0v1'],
		'A_thaliana' : ['A.-thaliana-TAIR9-TAIR10'],
		'R_communis' : ['R.-communis-TIGR.0.1-v0.1'],
		'L_usitatissimum' : ['L.-usitatissimum-BGIv1.0-v1.0'],
		'C_clementina' : ['C.-clementina-v1-v1.0'],
		'C_sativus' : ['C.-sativus-v1-v1.0'],
		'A_lyrata' : ['A.-lyrata-v1-v1.0'],
		'P_persica' : ['P.-persica-v1-v1.0'],
		'C_rubella' : ['C.-rubella-v1-v1.0'],
		'E_salsugineum' : ['E.-salsugineum-v1-v1.0'],
		'S_moellendorffii' : ['S.-moellendorffii-v1-v1.0'],
		'M_domestica' : ['M.-domestica-v1.0-v1.0'],
		'P_vulgaris' : ['P.-vulgaris-v1.0-v1.0'],
		'S_purpurea' : ['S.-purpurea-v1.0-v1.0'],
		'T_cacao' : ['T.-cacao-CGDv1.0-v1.1'],
		'C_grandiflora' : ['C.-grandiflora-v1-v1.1'],
		'A_coerulea' : ['A.-coerulea-v1-v1.1'],
		'C_sinensis' : ['C.-sinensis-v1-v1.1'],
		'E_grandis' : ['E.-grandis-v1.0-v1.1'],
		'P_virgatum' : ['P.-virgatum-v1.0-v1.1'],
		'F_vesca' : ['F.-vesca-v1.1-v1.1'],
		'B_stricta' : ['B.-stricta-v1-v1.2'],
		'B_rapa FPsc' : ['B.-rapa-FPsc-v1-v1.3'],
		'V_carteri' : ['V.-carteri-v2-v2.0'],
		'C_subellipsoidea C-169' : ['C.-subellipsoidea-C-169-v2.0-v2.0'],
		'M_guttatus' : ['M.-guttatus-v2.0-v2.0'],
		'O_lucimarinus' : ['O.-lucimarinus-v2.0-v2.0'],
		'S_italica' : ['S.-italica-v2-v2.1'],
		'S_bicolor' : ['S.-bicolor-v2.0-v2.1'],
		'G_raimondii' : ['G.-raimondii-v2.0-v2.1'],
		'B_distachyon' : ['B.-distachyon-v2.0-v2.1'],
		'P_patens' : ['P.-patens-v3-v3.0'],
		'M_pusilla CCMP1545' : ['M.-pusilla-CCMP1545-v3.0-v3.0'],
		'M_sp_RCC299' : ['M.-sp.-RCC299-v3.0-v3.0'],
		'P_trichocarpa' : ['P.-trichocarpa-v3.0-v3.0'],
		'S_tuberosum' : ['S.-tuberosum-v3-v3.4'],
		'M_esculenta' : ['M.-esculenta-v4-v4.1'],
		'C_reinhardtii' : ['C.-reinhardtii-v5.0-v5.5'],
		'O_sativa' : ['O.-sativa-v7.0-v7.0'],
		'G_max' : ['G.-max-v2.0-Wm82.a2.v1']
	}
	
	org_1 = request.form['organism1']
	org_2 = request.form['organism2']
	
	arr1 = org_dict.get(org_1)
	arr2 = org_dict.get(org_2)
	
	return render_template('search.html', speciesList1=arr1, speciesList2=arr2)

@app.route('/show', methods=['POST'])
def shows():
	
	#Store user submitted data from the form
	org_1 = request.form['organism1']
	org_2 = request.form['organism2']
	format = request.form['format']
	org_1_ranges_input = request.form['org_1_ranges']
	org_2_ranges_input = request.form['org_2_ranges']
	snpRange1 = request.form['range1']
	snpRange2 = request.form['range2']
	
	random_analysis_check = request.form['random']
	
	if format == "csv":
		org_1_ranges = CSVFormatConversion(org_1_ranges_input)
		org_2_ranges = CSVFormatConversion(org_2_ranges_input)
	
	if format == "dots":
		org_1_ranges = dotFormatConversion(org_1_ranges_input)
		org_2_ranges = dotFormatConversion(org_2_ranges_input)
		
	if format == "dash":
		org_1_ranges = dashFormatConversion(org_1_ranges_input)
		org_2_ranges = dashFormatConversion(org_2_ranges_input)
		
	if format == "snp":
		#range = request.form['range'] #Fix This
		org_1_ranges = snpFormatConversion(org_1_ranges_input, snpRange1)
		org_2_ranges = snpFormatConversion(org_2_ranges_input, snpRange2)
		
	if format == "done":
		org_1_ranges = org_1_ranges_input
		org_2_ranges = org_2_ranges_input
		
	#Convert the range searches into searchable objects
	search1 = pandas.read_csv(StringIO(org_1_ranges))
	search2 = pandas.read_csv(StringIO(org_2_ranges))
	

	print "Search, not random"
	for index, row in search1.iterrows():
		for index2, row2 in search1.iterrows():
			if str(row) == str(row2):
				a = 1
			else:
				if (str(row["chr"]) == str(row2["chr"])):
					if ((row["start"] >= row2["start"]) & (row["start"] <= row2["end"])) | ((row["end"] >= row2["start"]) & (row["end"] <= row2["end"])):
						if row["start"] <= row2["start"]:
							a = 1
						else:
							row["start"] = row2["start"]
						if row["end"] >= row2["end"]:
							a = 1
						else:
							row["end"] = row2["end"]
						search1.drop([index2])
					else:
						a = 1
				else:
					a=1
	search1.drop_duplicates(inplace=True)
		
		
		
	testtest_1 = '"chr","start","end"' + "\n"
	
	for index, row in search1.iterrows():
		tmp = ""
		chr = int(row['chr'])
		start = int(row['start'])
		end = int(row['end'])
	
		tmp = str(chr) + "," + str(start) + "," + str(end) + "\n"
		testtest_1 = testtest_1 + tmp
		
		
				
	for index, row in search2.iterrows():
		for index2, row2 in search2.iterrows():
			if str(row) == str(row2):
				a = 1
			else:
				if (str(row["chr"]) == str(row2["chr"])):
					if ((row["start"] >= row2["start"]) & (row["start"] <= row2["end"])) | ((row["end"] >= row2["start"]) & (row["end"] <= row2["end"])):
						if row["start"] <= row2["start"]:
							a = 1
						else:
							row["start"] = row2["start"]
						if row["end"] >= row2["end"]:
							a = 1
						else:
							row["end"] = row2["end"]
						search2.drop([index2])
					else:
						a = 1
				else:
					a=1
	search2.drop_duplicates(inplace=True)
		
	testtest_2 = '"chr","start","end"' + "\n"
	
	for index, row in search2.iterrows():
		tmp = ""
		chr = int(row['chr'])
		start = int(row['start'])
		end = int(row['end'])

		tmp = str(chr) + "," + str(start) + "," + str(end) + "\n"
		testtest_2 = testtest_2 + tmp
	
	
	type = 's'
	result = do_search(org_1, org_2, search1, search2, type)
	
	print "Search"
  	print result.apply(pandas.Series.nunique)
	
	randonFileName = int(random.random()*1000)
	pathName = 'static/' + str(randonFileName) + '/'
        #pathName = '../../resultFiles/' + str(randonFileName) + '/'
	os.mkdir( pathName, 0755 );
	fileName = 'static/' + str(randonFileName) + '/' + 'result.csv'
        #fileName = '../../resultFiles/' + str(randonFileName) + '/' + 'result.csv'
	result.to_csv(fileName)
	
	range_fileName = 'static/' + str(randonFileName) + '/range_' + 'query' + '.txt'
        #range_fileName = '../../resultFiles/' + str(randonFileName) + '/range_'+'query'+ '.txt'
	f = open(range_fileName,'w')
	print>>f, "1:"
  	print>>f, testtest_1
  	print>>f, "\n"
  	print>>f, "2:"
  	print>>f, testtest_2
  	f.close()
	
	summary_fileName = 'static/' + str(randonFileName) + '/summary' + '.txt'
        #summary_fileName = '../../resultFiles/' + str(randonFileName) + '/summary' + '.txt'
	
	f = open(summary_fileName,'a')
  	print>>f, "Search"
  	print>>f, result.apply(pandas.Series.nunique)
  	f.close()
	
	if random_analysis_check == 'y':
	
		meta_file_name = 'static/' + str(randonFileName) + '/random_' + 'meta' + '.csv'
                #meta_file_name = '../../resultFiles/' + str(randonFileName) + '/random_' + 'meta' + '.csv'
		
		#print "ORG1:" + str(org_1_ranges) + "\n"
		#print "ORG2:" + str(org_2_ranges)
	
		maize = [10,301476924,237917468,232245527,242062272,217959525,169407836,176826311,175377492,157038028,149632204];
		arabidopsis = [5,30427671,19698289,23459830,18585056,26975502];
		sorghum = [10,73727935,77694824,74408397,67966759,62243505,62192017,64263908,55354556,59454246,61085274];
		soybean = [20,56831624,48577505,45779781,52389146,42234498,51416486,44630646,47837940,50189764,51566898,34766867,40091314,45874162,49042192,51756343,37887014,41641366,58018742,50746916,47904181];
		rice = [12,43270923,35937250,36413819,35502694,29958434,31248787,29697621,28443022,23012720,23207287,29021106,27531856];
		
		arr1 = [];
		arr2 = [];
		
		if org_1 == 'A.-thaliana-TAIR9-TAIR10':
			arr1 = arabidopsis
	
		if org_1 == 'Z.-mays-AGPv3-5b+':
			arr1 = maize
		
		if org_1 == 'S.-bicolor-v2.0-v2.1':
			arr1 = sorghum

		if org_1 == 'G.-max-v2.0-Wm82.a2.v1':
			arr1 = soybean
			
		if org_1 == 'O.-sativa-v7.0-v7.0':
			arr1 = rice
			
		if org_2 == 'A.-thaliana-TAIR9-TAIR10':
			arr2 = arabidopsis
	
		if org_2 == 'Z.-mays-AGPv3-5b+':
			arr2 = maize
		
		if org_2 == 'S.-bicolor-v2.0-v2.1':
			arr2 = sorghum

		if org_2 == 'G.-max-v2.0-Wm82.a2.v1':
			arr2 = soybean
			
		if org_2 == 'O.-sativa-v7.0-v7.0':
			arr2 = rice
		
		
		i = 1
		n = 10
		print str(randonFileName) + "\n"
		format = 'done'
		while i <= n:
			org_1_range = generate_one_range(testtest_1, arr1)
			org_2_range = generate_one_range(testtest_2, arr2)
			type = 'r'
			
			#Convert the range searches into searchable objects
			search1 = pandas.read_csv(StringIO(org_1_range))
			search2 = pandas.read_csv(StringIO(org_2_range))
			result = do_search(org_1, org_2, search1, search2, type)
			
			print "Search"
  			print result.apply(pandas.Series.nunique)
			print str(i) + "\n"
			range_fileName = 'static/' + str(randonFileName) + '/range_' + str(i) + '.txt'
                        #range_fileName = '../../resultFiles/' + str(randonFileName) + '/range_' + str(i) + '.txt'
			f = open(range_fileName,'w')
			print>>f, "1:"
  			print>>f, org_1_range
  			print>>f, "\n"
  			print>>f, "2:"
  			print>>f, org_2_range
  			f.close()
  			
  			f = open(summary_fileName,'a')
  			print>>f, "Random" + str(i)
  			print>>f, result.apply(pandas.Series.nunique)
  			f.close()
  			
			fileName = 'static/' + str(randonFileName) + '/random_' + str(i) + '.csv'
                        #fileName = '../../resultFiles/' + str(randonFileName) + '/random_' + str(i) + '.csv'
			result.to_csv(fileName)
			
			i = i + 1
	
		print "Out of while"
		
	print "Out of if"
	
	#Prompt and download the file to the users machine
	print shutil.make_archive(pathName + "results", 'tar', pathName)
	fileToDownload = open(pathName + "results.tar")
	fileToDownloadContents = fileToDownload.read()

	response = make_response(fileToDownloadContents)
	response.headers["Content-Disposition"] = "attachment; filename=" + "results.tar"

	return response
	
if __name__ == '__main__':
    app.debug = True
    app.run()
