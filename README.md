# DNA sequence conversion

Converts binary file containing DNA sequence to FASTQ format.

Takes two parameters: input file and L number

Input file is read by L bytes. Each byte of input file is considered to contain A-C-G-T base in 2 most significant bits. The rest 6 bits contain quality score.

Implemented both in Python and java.
