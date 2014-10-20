#!/usr/bin/env python
# filterDSRb.py
# 10/20/2014 Sarah J. Spencer, Alm Lab, MIT
# Filter Illumina sequence reads for matches to a section of the dsrB
# gene and known bridge primer sequences.

from optparse import OptionParser
import re

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

# Parse the joined fasta reads for designed primer sequence structure
# Output: sequences that match the designed structure
def fwdparse(rawHeaders, rawSeqs, outputLength):
    usableHeaders = []
    usableSeqs = []
    primerfwd = '[CT][AG][CT][AG][ACG]AG[ACG]AT[GC]GCGAT[AG]TCGGA'
    primerbridge = 'C[AG]CC[AG]CACAT[AG]TT[GC]AGGCACAGC[AC]GCCGCGGTA'
    for i,rawSeq in enumerate(rawSeqs):
	if ((re.search(primerfwd, rawSeq[0:22])) and
	    (re.search(primerbridge, rawSeq))):
	    pass
	else:
	    continue
	splitSeq = re.split(primerbridge,rawSeq)
	if len(splitSeq[1]) < outputLength+1:
	    continue
	if splitSeq[1][outputLength] == '\n':
	    continue
	usableHeaders.append(rawHeaders[i])
	usableSeqs.append(splitSeq[1][1:outputLength+1] + '\n')
    return usableHeaders, usableSeqs

# This wrapper function takes user-defined input and output directories as well
# as the common length to trim 16S sequences. These variables are used to parse
# and export fasta sequences that match the dsrB fusion structure.
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

    #Filter each sample for sequence structure and save filtered sequences
    rawHeaders, rawSeqs = importData(options.i)
    usableHeaders, usableSeqs = fwdparse(rawHeaders, rawSeqs, int(options.l))
    outFile = open(options.o, 'w')
    for i, header in enumerate(usableHeaders):
	outFile.write(usableHeaders[i])
	outFile.write(usableSeqs[i])
    outFile.close()

if __name__ == "__main__":
    main()
