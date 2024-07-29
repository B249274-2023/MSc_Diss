#!/bin/python
import os
import gzip
import subprocess

# make bed files for each of the tissue types
directory="../../../human/GTEx/GTEx_Analysis_v6p_eQTL/"

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

tissue_eQTL_counts_file = "tissue_eQTL_counts.txt"

with open(tissue_eQTL_counts_file_counts_file, 'a') as row_counts:
    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith("_Analysis.v6p.signif_snpgene_pairs.txt.gz"):
            # Define the path to the input file
            input_path = os.path.join(directory, filename)
        
            # Define the path to the output file
            output_filename = filename.replace("_Analysis.v6p.signif_snpgene_pairs.txt.gz", "_tissue_snps.bed")
            output_path = os.path.join("eQTL_locations/", output_filename)

            # Extract base filename for row_counts
            base_filename = filename.replace("_Analysis.v6p.signif_snpgene_pairs.txt.gz", "")

            line_count = 0 # Create empty variable to count number of lines in file
            # Edit Variant ID to fit bed file format
            with gzip.open(input_path, 'rt') as infile, open(output_path, 'w') as outfile:
                for line in infile:
                    columns = line.strip().split()
                    if len(columns) > 0:
                        first_col = columns[0].split('_')
                        if len(first_col) >= 2 and is_int(first_col[1]):
                            col1 = first_col[0]
                            col2 = first_col[1]
                            col2_int = int(col2)
                            col3 = str(col2_int + 1)                        
                            outfile.write("{0}\t{1}\t{2}\n".format(col1, col2, col3))
                            line_count += 1
            # Write the filename and line count to the row counts file
            row_counts.write("{0}\t{1}\n".format(filename, line_count))

# Make bed files for each of the different mammals
mammal_dir = "full_alignments/"

for filename in os.listdir(mammal_dir):
    if filename.endswith("_unique_all.bed.gz"):
        # Define the path to the input file
        input_path = os.path.join(mammal_dir, filename)
        
        # Define the path to the output file
        output_filename = filename.replace("_unique_all.bed.gz", "_SNPs.bed")
        output_path = os.path.join("eQTL_locations/species", output_filename)
        
        with gzip.open(input_path, 'rt') as infile, open(output_path, 'w') as outfile:
            for line in infile:
                columns = line.strip().split()
                if len(columns) > 0:
                    first_col = columns[0].split('_')
                    if len(first_col) >= 2 and is_int(first_col[1]):
                        col1 = first_col[0]
                        col2 = first_col[1]
                        col2_int = int(col2)
                        col3 = str(col2_int + 1)                        
                        outfile.write("{0}\t{1}\t{2}\n".format(col1, col2, col3))

# intersect analysis
# Define the directory containing the files
in_dir = "eQTL_locations/"

# Get the list of all _SNPs.bed files and _tissue_snps.bed files
mammals_files = [f for f in os.listdir(in_dir) if f.endswith('_SNPs.bed')]
tissue_snps_files = [f for f in os.listdir(in_dir) if f.endswith('_tissue_snps.bed')]

# Iterate through each combination of _SNPs.bed file and _tissue_snps.bed file to perform bedtools intersect on each combo
for mammal in mammals_files:
    for tissue in tissue_snps_files:
        # Define the input file paths
        snps_path = "os.path.join(in_dir, mammal)"
        tissue_snps_path = os.path.join(in_dir, tissue)
        
        # Define the output file path
        output_filename = "{0}_intersect_{1}.bed".format(os.path.splitext(mammal)[0], os.path.splitext(tissue)[0])
        output_path = os.path.join(in_dir, output_filename)
        
        # Run bedtools intersect
        command = "bedtools intersect -a {0} -b {1} > {2}".format(snps_path, tissue_snps_path, output_path)

        subprocess.call(command, shell=True)
