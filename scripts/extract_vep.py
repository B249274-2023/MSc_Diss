import os

# Define the directory containing the files and the output file
input_file = '../../../human/GTEx/all_GTEx_hg19.bed'
output_file = 'vep_input_signif.txt'

# Function to process and reformat the columns from a file
def process_bed_file(file_path, output_writer, unique_lines):
    with open(file_path, 'rt') as f:
        next(f)  # Skip the first line (header)
        for line in f:
            columns = line.strip().split('\t')
            if len(columns) >= 4:
                col_four = columns[3].split('_')
                col_six = columns[5]
                if len(col_four) >= 4:
                    chr = col_four[0]
                    start = col_four[1]
                    end = str(int(col_four[1]) + 1)
                    snp = col_four[2] + '/' + col_four[3]
                    strand = col_six
                    
                    # Create the output line
                    output_line = '\t'.join([chr, start, end, snp, strand])
                    
                    # Write the output line if it's unique
                    if output_line not in unique_lines:
                        unique_lines.add(output_line)
                        output_writer.write(output_line + '\n')

# Initialize the output file and a set to track unique lines
unique_lines = set()
with open(output_file, 'w') as output:
    # Process the input file
    try:
        process_bed_file(input_file, output, unique_lines)
    except Exception as e:
        print("Error processing file {}: {}".format(input_file, e))

print("Extraction complete. Results saved in {}.".format(output_file))
