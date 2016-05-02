import random
import os, sys
import shutil

def generate_one_range(range, arr):
	random_range = '"chr","start","end"' + "\n"
	
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
		
	return random_range

def generateRandom(range, arr):
	#random_range = '"chr","start","end"' + "\n"
	print "CR: " + str(arr[0]) + "\n"
	
	i = 0
	n = 100
	randomFileName = int(random.random()*1000)
	pathName = 'static/random/' + str(randomFileName) + '/'
        
	os.mkdir( pathName, 0755 );
	
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
		
			tmp = str(randChr) + "," + str(randStart) + "," + str(randEnd) #+ "\n"
			#random_range += tmp
			random_range.append(tmp)
			
		
		fileName = 'static/random/' + str(randomFileName) + '/' + str(i) + '.csv'
                
		f = open(fileName,'w')
		for item in random_range:
  			print>>f, item
  		i = i + 1
  		
	shutil.make_archive(pathName + "results", 'zip', pathName)
	
	return pathName
