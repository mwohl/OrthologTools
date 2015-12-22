#Dot Format Conversion Function

def CSVFormatConversion(range):
	formatted_range = '"chr","start","end"' + "\n"
	for line in range.splitlines():
		line = line + "\n"
		formatted_range += line
	return formatted_range

def dotFormatConversion(range):
	formatted_range = '"chr","start","end"' + "\n"
	for line in range.splitlines():
		line = line.replace(":", ",", 1)	
		line = line.replace("..", ",", 1)
		line = line + "\n"
		formatted_range += line
	return formatted_range

#Dash Format Conversion Function	
def dashFormatConversion(range):
	formatted_range = '"chr","start","end"' + "\n"
	for line in range.splitlines():
		line = line.replace(":", ",", 1)	
		line = line.replace("-", ",", 1)
		line = line + "\n"
		formatted_range += line
	return formatted_range
	
#SNP Format Conversion Function
def snpFormatConversion(range, number):
	formatted_range = '"chr","start","end"' + "\n"
	for line in range.splitlines():
		list = line.split(':')
		start_stop = str( int(list[1]) - int(number) ) + "," + str( int(list[1]) + int(number) )
		tmp = str(list[0]) + "," + str(start_stop) + "\n"
		formatted_range += tmp
	return formatted_range
	
	
#possibly add a snp value to the search so that it can be added easily to the end csv later?