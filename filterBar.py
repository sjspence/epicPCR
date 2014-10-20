#!/usr/bin/env python
# filterBar.py
# 10/20/2014 Sarah J. Spencer, Alm Lab, MIT
# Filter Illumina sequence reads for matches to synthetic barcode primer
# structure. Export 16S sequences trimmed to common length.

from optparse import OptionParser

# Import data from fasta file and save in header and sequence variables
def importData(inputFileName):
    rawHeaders = []
    rawSeqs = []
    inputFile = open(inputFileName,'r')
    rawHeaders = []
    rawSeqs = []
    track = 'header'
    for line in inputFile:
	if track == 'header':
	    rawHeaders.append(line)
	    track = 'seq'
	else:
	    rawSeqs.append(line)
	    track = 'header'
    inputFile.close()
    return rawHeaders, rawSeqs

# Parse the joined fasta read for designed primer sequence structure
# Output: sequences that match the designed structure
def fwdparse(rawHeaders, rawSeqs, outputLength):
    import sys
    usableHeaders = []
    usableSeqs = []
    barcodes = []
    for i,rawSeq in enumerate(rawSeqs):
	if len(rawSeq) < (60+outputLength):
	    continue
	if rawSeq[59+outputLength] == '\n':
	    continue
	if ((rawSeq[20:49] == 'GATCATGACCCATTTGGAGAAGATGCAGC') and
	    (rawSeq[49] == 'A' or 'C') and
	    (rawSeq[50:59] == 'GCCGCGGTA')):
	    usableHeaders.append(rawHeaders[i].strip() +
				 ' droplet_bc=' + rawSeq[0:20] + '\n')
	    usableSeqs.append(rawSeq[60:60+outputLength] + '\n')
    return usableHeaders, usableSeqs

# This wrapper function takes user-defined input and output directories as well
# as the common length to trim 16S sequences. These variables are used to parse
# and export fasta sequences that match the barcode fusion structure.
def main():
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="i",
		      help="Input fasta file of non-chimeric sequences.",
		      metavar="INPUT")
    parser.add_option("-l", "--length", dest="l",
		      help="Length to trim output sequences.",
		      metavar="LENGTH")
    parser.add_option("-o", "--output", dest="o",
		      help="Output fasta file of structure-filtered sequences.",
		      metavar="OUTPUT")
    (options, args) = parser.parse_args()

    #Filter for sequence structure and save filtered sequences
    rawHeaders, rawSeqs = importData(options.i)
    usableHeaders, usableSeqs = fwdparse(rawHeaders, rawSeqs, int(options.l))
    outFile = open(options.o, 'w')
    for i, header in enumerate(usableHeaders):
	outFile.write(usableHeaders[i])
	outFile.write(usableSeqs[i])
    outFile.close()

if __name__ == "__main__":
    main()
