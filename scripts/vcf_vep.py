import pandas as pd
import os
import subprocess

# Define the directory containing the files and the output file
input_bed_file = '../../../human/GTEx/all_GTEx_hg19.bed'
output_vcf_file = '../vep/vep_input_signif.vcf'

def GTEx_bed_file(file_path, output_writer, unique_lines):
    with open(file_path, 'rt') as f:
        next(f)  # Skip the first line (header)
        for line in f:
            columns = line.strip().split('\t')
            if len(columns) >= 6:
                col_four = columns[3].split('_')
                col_six = columns[5]
                if len(col_four) >= 4:
                    chr = col_four[0]
                    pos = int(col_four[1]) + 1  # VCF is 1-based
                    ref = col_four[2]
                    alt = col_four[3]
                    strand = col_six
                    
                    # Create the VCF output line
                    vcf_line = f"{chr}\t{pos}\t.\t{ref}\t{alt}\t.\t.\t."
                    
                    # Write the output line if it's unique
                    if vcf_line not in unique_lines:
                        unique_lines.add(vcf_line)
                        output_writer.write(vcf_line + '\n')


vcf_header = [
    "##fileformat=VCFv4.2",
    "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO"
]

unique_lines = set()

with open(output_vcf_file, 'w') as output_writer:
    # Write the VCF header
    for line in vcf_header:
        output_writer.write(line + '\n')
    
    # Process the BED file and write the VCF lines
    GTEx_bed_file(input_bed_file, output_writer, unique_lines)

