# Import necessary libraries.
import random
import os, sys
import shutil

# Function to generate one random range that matches the size of the input range.
# Chromosomes and coordinates will be chosen to fit with the organism supplied in
# the argument arr.
def generate_one_range(range, arr):
	random_range = '"chr","start","end"' + "\n"
	
	# Generate the range.
	for line in range.splitlines()[1:]:
		tmp = ""
		list = line.split(',')
		chr = int(list[0])
		start = int(list[1])
		stop = int(list[2])
	
		length = stop - start
	
		randChr = random.randint(1,arr[0])
		randStart = random.randint(1, arr[randChr] - (length+1))
		randEnd = randStart + length
		tmp = str(randChr) + "," + str(randStart) + "," + str(randEnd) + "\n"
		random_range = random_range + tmp
	
	# Return the range	
	return random_range

# Function to generate n random ranges that match the size of the input range.
# Chromosomes and coordinates will be chosen to fit with the organism supplied in
# the argument arr.
def generateRandom(range, arr):
	
	# Change the value of n to change the number of random ranges generates.
	i = 0
	n = 100 
	
	# Creates the path for the random ranges files to be stored.
	randomFileName = int(random.random()*1000)
	pathName = 'static/random/' + str(randomFileName) + '/'
	os.mkdir( pathName, 0755 );
	
	# Each time through this loop, one set of random ranges is generated.
	# The loop terminates when there are n sets of ranges.
	while i < n:
		random_range = [];
		random_range.append("chr,start,end")
		for line in range.splitlines():
			tmp = ""
			list = line.split(',')
			chr = int(list[0])
			start = int(list[1])
			stop = int(list[2])
		
			length = stop - start
		
			randChr = random.randint(1,arr[0])
			randStart = random.randint(1, arr[randChr] - (length+1))
			randEnd = randStart + length
		
			tmp = str(randChr) + "," + str(randStart) + "," + str(randEnd)
		
			random_range.append(tmp)
			
		# Print the ranges to a file.
		fileName = 'static/random/' + str(randomFileName) + '/' + str(i) + '.csv'
		f = open(fileName,'w')
		for item in random_range:
  			print>>f, item
  		i = i + 1
  	
  	# Put the generated ranges into a ZIP file.
	shutil.make_archive(pathName + "results", 'zip', pathName)
	
	# Return the path name to the ZIP file.
	return pathName