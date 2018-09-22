import gzip
from matplotlib import pyplot as plt


def missing_hist(infile,outfile,blankword_list):
	l = []
	for line in infile:
		cols = line.split("\t")
		l.append(0)
		for col in cols:
			if col and not col in blankword_list:
				l[-1] += 1
			#if not col or col in ["missing", "Missing"]:
			#	l[-1] += 1

	print l

	counts, bins, bars = plt.hist(l,histtype="stepfilled",align="mid",color="cornflowerblue")
	print counts
	print bins
	print bars
	plt.title("Number of non-empty fields")
	#plt.show()
	plt.savefig(outfile)
	infile.close()
	outfile.close()




def main():
	infile = gzip.open("/home/simon/Arbeit/hackathon_DC/BettaMetaData/data/ncbi-biosample/summary/ncbi-summary.txt.gz", "r")
	outfile = open("/home/simon/Arbeit/hackathon_DC/BettaMetaData/data/ncbi-biosample/summary/missing_cols.png", "w")
	blankword_list = ["missing", "Missing", "NA", "na", "NONE", "None","not applicable","Not applicable","Not available","Not available","not available","N/A", "unknown", "Unknown"]
	missing_hist(infile, outfile, blankword_list)



if __name__ == '__main__':
	main()