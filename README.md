EPIC PCR
========

Scripts to parse sequence data from EPIC PCR libraries.

10/29/2014 Sarah J. Spencer, Alm Lab, MIT

CONTENTS OF THIS FILE
---------------------
 * Introduction
 * Requirements
 * Installation
 * Command Line Arguments
 * Maintainers
 * References

INTRODUCTION
------------
Starting with raw fastq files of paired-end data, run the following list of
commands to generate curated fasta files of 16S reads as well as Operational
Taxonomic Units within EPIC PCR libraries. Scripts are either included in the
QIIME package or they are custom scripts available at
www.github.com/sjspence/EPIC_PCR.

If you prepared an EPIC PCR reaction with new primer sets and target genes, you
should modify the custom scripts filterBar.py or filterDSRb.py to recognize your
tailored fusion structure.

REQUIREMENTS
------------
 * Perl version 5.10.1
 * Python version 2.7.6
 * QIIME version 1.8.0

INSTALLATION
------------
 * Perl is available for download from www.perl.org/get.html
 * Python is available for download from www.python.org/downloads
 * QIIME is available for download from http://qiime.org
 * The custom python and perl scripts in this directory are not packaged in a
   module. No installation is necessary, simply download the scripts
   and run them using local installations of perl, python, and QIIME.

COMMAND LINE ARGUMENTS
----------------------
**1 Fastq to fasta**

1.1 Join paired-end sequences using fastq quality scores (QIIME script)

      join_paired_ends.py -f [fastq F] -r [fastq R] -o [output directory]

1.2 Extract multiplexed sample barcodes from joined fastq file (custom script)

      perl fastq2Qiime_barcode.pl [joined fastq] > [output file]

1.3 Quality filter and split sample libraries (QIIME script)

      split_libraries_fastq.py -i [joined fastq] -b [barcode file]
      -o [output directory] -m [mapping file] --barcode_type 8
      --min_per_read_length_fraction 0.40 -q 20 --max_barcode_errors 0
      --max_bad_run_length 0

1.4 Separate individual samples into separate files (QIIME script)

      extract_seqs_by_sample_id.py -i [input fasta] -o [output fasta]
      -s [sample ID]

1.5 Check for chimeras within stitched sequences (QIIME script)

      identify_chimeric_seqs.py -m usearch61 -i [input fasta]
      --suppress_usearch61_ref -o [output directory]

1.6 Export fasta file with non-chimeric sequences (custom script)

      python discardChimeras.py -i [input fasta] -n [non-chimeric sample IDs]
      -o [output fasta]

1.7 Filter fasta sequences for fusion structure and export trimmed 16S sequences

    (custom scripts, either for barcode-16S or dsrB-16S fusions)

    (for bulk 16S data, use filterLength.py to trim read lengths)

      python filterBar.py -i [input fasta] -l [16S length] -o [output fasta]
      python filterDSRb.py -i [input fasta] -l [16S length] -o [output fasta]
      python filterLength.py -i [input fasta] -l [16S length] -o [output fasta]

    For barcode-16S fusions, collapse identical barcode-16S pairs into a
    consensus sequence for downstream analysis (custom script)

      python compressBar.py -i [input fasta] -o [output fasta]

**2 Fasta to Operational Taxonomic Units (OTUs)**

NOTE: all the following commands are from the QIIME pipeline

2.1 Pick OTUs using uclust

      pick_otus.py -i [input fasta] -o [output directory]

2.2 Pick representative OTU sequences based on abundance

      pick_rep_set.py -i [otu text file] -f [input fasta]
      -m most_abundant -o [representative fasta]

2.3 Assign taxonomy to representative sequences using the greengenes database

      assign_taxonomy.py -i [representative fasta] -o [output directory]

2.4 Make OTU table

      make_otu_table.py -i [otu text file] -t [taxonomy text file]
      -o [biom file]

2.5 Rarefactions to even the sequencing depth

    NOTE: only perform this step if comparing sensitivity across samples

      multiple_rarefactions_even_depth.py -i [biom file] -d [read depth]
      -o [output directory] --lineages_included

2.6 Summarize taxa based on OTU table

      summarize_taxa.py -i [biom file] -o [output directory]

MAINTAINERS
-----------
Current maintainers:
 * Sarah J. Spencer (sjspence@mit.edu)
 * Sarah P. Preheim (spacocha@mit.edu)

This material by ENIGMA - Ecosystems and Networks Integrated with Genes and Molecular Assemblies (http://enigma.lbl.gov), a Scientific Focus Area Program at Lawrence Berkeley National Laboratory is based upon work supported by the U.S. Department of Energy, Office of Science, Office of Biological & Environmental Research under contract number DE-AC02-05CH11231.

REFERENCES
----------
Caporaso JG, Kuczynski J, Stombaugh J, Bittinger K, Bushman FD, Costello EK, Fierer N, Pena AG, Goodrich JK, Gordon JI, et al. 2010. QIIME allows analysis of high-throughput community sequencing data. Nat Methods 7: 335-336.
