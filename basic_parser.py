#!/env/python2.7

# basic_parser.py
# Created 9/20/18 by Sam Westreich, github.com/transcript
# Function - read through a set of downloaded EBI metadata and give info about the entries in each column.

import sys, re

try:
	infile = open(sys.argv[1], "r")
except IndexError:
	sys.exit("Specify the downloaded metadata file as ARGV1.")

line_counter = 0
dic_list = []

for line in infile:
	line_counter += 1
	# header row
	if line_counter == 1:
		dic_names = line.strip().split("\t")
		dic_list = [dict() for item in line.strip().split('\t')]
	# past header row
	else:
		line = line.strip()
		split = re.split(r'\t', line)
		for i in range(0, len(split)-1):
			datum=split[i]
			position = i
			if datum == "":
				datum = "!blank"
			if datum.isspace() == True:
				datum = "!blank"
#			print position, datum
			try:
				dic_list[position][datum] += 1
			except KeyError:
				dic_list[position][datum] = 1
				continue

print len(dic_list)

infile.close()

# outfile stuff
if "-F" in sys.argv:
	outfile = open("outfile.txt", "w")
	for dictionary in dic_names:
		exclude = ["accession", "secondary_sample_accession"]
		if dictionary not in exclude:
			outfile.write(dictionary + "\n")
			for k, v in sorted(dic_list[dic_names.index(dictionary)].items(), key=lambda kv: -kv[1])[:100]:
				outfile.write(k + "\t" + str(v) + "\n")
			outfile.write("\n")

outfile.close()
