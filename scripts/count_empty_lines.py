import gzip
from matplotlib import pyplot as plt

infile = gzip.open("/home/simon/Arbeit/hackathon_DC/BettaMetaData/data/ncbi-biosample/summary/ncbi-summary.txt.gz", "r")
l = []
for line in infile:
	cols = line.split("\t")
	l.append(0)
	for col in cols:
		if not col or col in ["missing", "Missing"]:
			l[-1]+=1

p = plt.hist(l)
plt.savefig(open("/home/simon/Arbeit/hackathon_DC/BettaMetaData/data/ncbi-biosample/summary/missing_cols.png","w"))

print len(cols)