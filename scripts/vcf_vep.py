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

# Use bedtools intersect to create files for VEP analysis
# cat eQTL_locations/species/*_SNPs.bed | sort -k2,2n | uniq -c > species_input.bed
# bedtools sort -i species.bed > species_eQTLs_sorted.bed

#subprocess.run("bedtools intersect -a species_eQTLs_sorted.bed -b GTEx_eQTLs_sorted.bed -sorted > vep_tissue_eQTLs.bed", shell=True) # BED file that contains the eQTLs that are present in the species
#subprocess.run("bedtools intersect -a GTEx_eQTLs_sorted.bed -b species_eQTLs_sorted.bed -sorted -v > eQTLs_not_in_species.bed", shell=True) # BED file that contains the eQTLs that aren't present in the species
#subprocess.run("bedtools intersect -b eQTL_ge16.bed -a species_eQTLs_sorted.bed > frequent_eQTLs.bed", shell=True) # BED file that contains the eQTLs that appear more than 16 times 


def bed_to_vcf(bed_file, vcf_file):
    with open(bed_file, 'rt') as bed, open(vcf_file, 'w') as vcf:
        # Write VCF header
        vcf.write("##fileformat=VCFv4.2\n")
        vcf.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")

        for line in bed:
            columns = line.strip().split('\t')
            if len(columns) >= 4:
                chr = columns[0]
                start = int(columns[1]) + 1  # Convert 0-based BED start to 1-based VCF position
                ref_alt = columns[3].split('/')
                if len(ref_alt) == 2:
                    ref = ref_alt[0]
                    alt = ref_alt[1]
                    
                    # Create the VCF line
                    vcf_line = f"{chr}\t{start}\t.\t{ref}\t{alt}\t.\t.\t.\n"
                    vcf.write(vcf_line)

# Convert bed files into vcf files for VEP analysis
bed_to_vcf("vep_tissue_eQTLs.bed", "input/vep_tissue_eQTLs.vcf")
bed_to_vcf("eQTLs_not_in_species.bed", "input/eQTLs_not_in_species.vcf")
bed_to_vcf("frequent_eQTLs.bed", "input/frequent_eQTLs.vcf")

# run vep analysis
os.chdir("../ensembl-vep")
subprocess.call("./vep -i ../vep/input/vep_input_signif.vcf -o ../vep/output/vep_all_output.txt --cache --dir_cache ../vep/cache --assembly GRCh37 --offline", shell=True)
subprocess.call("./vep -i ../vep/input/vep_tissue_eQTLs.vcf -o ../vep/output/vep_tissue_output.txt --cache --dir_cache ../vep/cache --assembly GRCh37 --offline", shell=True)
subprocess.call("./vep -i ../vep/input/eQTLs_not_in_species.vcf -o ../vep/output/vep_non_species_output.txt --cache --dir_cache ../vep/cache --assembly GRCh37 --offline", shell=True)
subprocess.call("./vep -i ../vep/input/frequent_eQTLs.vcf -o ../vep/output/vep_tissue_output.txt --cache --dir_cache ../vep/cache --assembly GRCh37 --offline", shell=True)




