#!/usr/bin/env python
# filterLength.py
# 10/20/2014 Sarah J. Spencer, Alm Lab, MIT
# Trim 16S fasta sequences to a user-specified length in order to enable
# alignment and comparison with EPIC PCR 16S sequences.

from optparse import OptionParser

def main():
    #Gather input and output file paths along with user-specified length
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="i",
		      help="Input fasta file to be filtered for chimeras.",
		      metavar="INPUT")
    parser.add_option("-l", "--length", dest="l",
		      help="Length to trim output sequences.",
		      metavar="LENGTH")
    parser.add_option("-o", "--output", dest="o",
		      help="Output fasta file of non-chimeric sequences.",
		      metavar="OUTPUT")
    (options, args) = parser.parse_args()
    inputFile = open(options.i, 'r')
    outputFile = open(options.o, 'w')
    inputData = []
    for line in inputFile:
	inputData.append(line)
    inputFile.close()
    outputLength = int(options.l)

    #Only export sequence data that is long enough to trim to the user-
    #specified length
    for i,line in enumerate(inputData):
	if (('>' not in line) and (len(line) > outputLength)
	    and (line[outputLength-1] != '\n')):
	    outputFile.write(inputData[i-1])
	    outputFile.write(inputData[i][0:outputLength] + '\n')
    outputFile.close()

if __name__ == "__main__":
    main()
