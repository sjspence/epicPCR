#! /usr/bin/perl -w
# fastq2Qiime_barcode.pl
# 10/29/2014 Sarah P. Preheim, Alm Lab, MIT
# Input a fastq file. Script recognizes sample-specific barcodes stored in
# sequence headers. Export barcode file mapping sequence IDs to sample barcodes
# for downstream qiime analysis.


die "Usage: fastq\n" unless (@ARGV);
($new) = (@ARGV);
chomp ($new);

$/="@";
open (IN, "<$new" ) or die "Can't open $new\n";
while ($line =<IN>){
    chomp ($line);
    next unless ($line);
    ($info, @seqs) = split ("\n", $line);
    ($first, $bar)=$info=~/^(.+)\#([ATGCKMRYSWBVHDNX]+)/;
    ($lcbar)=lc($bar);
    print "\@${first}\#${bar}/3\n$bar\n+\n$lcbar\n";
} 
close (IN);

