#!/usr/bin/env python
# discardChimeras.py
# 10/20/2014 Sarah J. Spencer, Alm Lab, MIT
# Takes an input fasta file and a text file of identified non-chimeric
# sequence IDs, then exports a fasta file of non-chimeric sequences.

from optparse import OptionParser

def main():
    #Gather input and output file paths
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="i",
		      help="Input fasta file to be filtered for chimeras.",
		      metavar="INPUT")
    parser.add_option("-n", "--non-chimeras", dest="nc",
		      help="Text file indicating non-chimeric sequence IDs.",
		      metavar="NON-CHIMERAS")
    parser.add_option("-o", "--output", dest="o",
		      help="Output fasta file of non-chimeric sequences.",
		      metavar="OUTPUT")
    (options, args) = parser.parse_args()
    inputFile = open(options.i, 'r')
    ncFile = open(options.nc, 'r')
    outputFile = open(options.o, 'w')

    #Create arrays for input and non-chimeric sequences
    nc = []
    for line in ncFile:
	nc.append(line.strip())
    ncFile.close()
    inputData = []
    for line in inputFile:
	inputData.append(line)
    inputFile.close()

    #Store input sequences in a dictionary with sequence IDs mapping to the full
    #sequence information
    seqDict = {}
    for i,line in enumerate(inputData):
	if '>' in line:
	    seqID = line.replace('>','')
	    seqID = seqID.split(' ')
	    seqID = seqID[0]
	    seqDict[seqID] = [line, inputData[i+1]]

    #Find and export the intersection of non-chimeric sequence IDs with input
    #sequence IDs. Export full sequence header and sequence data in fasta
    #format.
    ncKeys = set(nc).intersection(seqDict)
    for key in ncKeys:
	outputFile.write(seqDict[key][0])
	outputFile.write(seqDict[key][1])
    outputFile.close()

if __name__ == "__main__":
    main()
