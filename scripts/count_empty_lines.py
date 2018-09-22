import gzip
from matplotlib import pyplot as plt


def missing_hist(infile,outfile):
	l = []
	for line in infile:
		cols = line.split("\t")
		l.append(0)
		for col in cols:
			if col and not col in ["missing", "Missing", "NA", "na", "NONE", "None",]:
				l[-1] += 1
			#if not col or col in ["missing", "Missing"]:
			#	l[-1] += 1

	print l

	plt.hist(l,histtype="stepfilled")
	plt.show()
	#plt.savefig(outfile)
	infile.close()
	outfile.close()




def main():
	infile = gzip.open("/home/simon/Arbeit/hackathon_DC/BettaMetaData/data/ncbi-biosample/summary/ncbi-summary.txt.gz", "r")
	outfile = open("/home/simon/Arbeit/hackathon_DC/BettaMetaData/data/ncbi-biosample/summary/missing_cols.png", "w")
	missing_hist(infile, outfile)



if __name__ == '__main__':
	main()