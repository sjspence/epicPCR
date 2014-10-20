#!/usr/bin/env python
# compressBar.py
# 10/20/2014 Sarah J. Spencer, Alm Lab, MIT
# Group sequences that share a droplet barcode, check for multiple 16S
# sequences, then collapse to a consensus sequence for downstream analysis.

from optparse import OptionParser

# Import sequence data and convert into a dictionary with droplet barcodes
# mapping to one or more 16S sequences.
# Output: barcode dictionary
def makeBCdict(inputFileName):
    #Import fasta file
    inputFile = open(inputFileName, 'r')
    data = []
    for line in inputFile:
	data.append(line.strip())
    inputFile.close()

    #Create python dictionary based on droplet barcodes
    bcDict = {}
    for i,line in enumerate(data):
	if line[0] == '>':
	    bc = line.split(' ')[5].split('=')[1]
	    seq = data[i+1]
	else:
	    continue
	if bc in bcDict:
	     bcDict[bc].append([line, seq])
	else:
	     bcDict[bc] = [[line, seq]]
    return bcDict

# Iterate through barcode dictionary. For barcodes with multiple 16S sequences,
# find the most abundant sequence and discard other barcode-16S pairs.
# Output: written file containing updated fasta sequences with compressed
# barcode-16S pairs.
def exportCompressed(bcDict, outputFileName):
    compressedFile = open(outputFileName, 'w')
    for bc in bcDict:
	readList = bcDict[bc]
	seqDict = {}
	countDict = {}
	for read in readList:
	    if read[1] in seqDict:
		countDict[read[1]] += 1
	    else:
		seqDict[read[1]] = read[0]
		countDict[read[1]] = 1
	for seq in seqDict:
	    abundance = float(countDict[seq]) / float(len(readList))
	    abundStr = (' drop_abun=' + str(abundance) + '(' +
			str(countDict[seq]) + '/' + str(len(readList)) + ')')
	    if len(readList) > 10:
		compressedFile.write(seqDict[seq] + abundStr + '\n')
	    else:
		compressedFile.write(seqDict[seq] + '\n')
	    compressedFile.write(seq + '\n')
    compressedFile.close()

# This wrapper function takes user-defined input and output files. The input
# file is read and processed to compress identical barcode-16S pairs, then
# these consensus pairs are written to the export file.
def main():
    #Set up options to input the experiment and sample designations to run.
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="i",
                      help="Input fasta file of sequences filtered for barcode structure.",
                      metavar="INPUT")
    parser.add_option("-o", "--output", dest="o",
                      help="Output fasta file of compressed sequences (no duplicate barcode-16S pairs).",
                      metavar="OUTPUT")
    (options, args) = parser.parse_args()

    #Analyze sample for barcode structure
    bcDict = makeBCdict(options.i)

    #Export fasta files compressed by barcode
    exportCompressed(bcDict, options.o)

if __name__ == "__main__":
    main()
