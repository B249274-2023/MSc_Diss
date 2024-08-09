import os
import gzip
from collections import defaultdict

# Specify the folder path containing the files
folder_path = "../vep/output/"

# Step 1 and Step 2: Process each file individually
for filename in os.listdir(folder_path):
    if filename.endswith("_output_ClinVar.txt.gz"):
        file_path = os.path.join(folder_path, filename)
        base_name = filename.replace("_output_ClinVar.txt.gz", "")
        output_file_path = os.path.join(folder_path, f"{base_name}_filtered_ClinVar.txt")
        count_file_path = os.path.join(folder_path, f"{base_name}_ClinVar_CLNSIG_counts.txt")

        clinvar_clnsig_counts = defaultdict(int)
        unique_ids = set()

        # Step 1: Filter rows that contain 'ClinVar=' and have a unique ID (column 1)
        with gzip.open(file_path, 'rt') as infile, open(output_file_path, 'w') as output_file:
            for line in infile:
                if 'ClinVar=' in line:
                    # Split the line into columns based on tabs (assuming tab-delimited files)
                    columns = line.strip().split('\t')
                    unique_id = columns[0]

                    # Check if the ID is unique
                    if unique_id not in unique_ids:
                        unique_ids.add(unique_id)
                        output_file.write(line)

        # Step 2: Count occurrences of values after 'ClinVar_CLNSIG='
        with open(output_file_path, 'r') as filtered_file:
            for line in filtered_file:
                if 'ClinVar_CLNSIG=' in line:
                    # Extract the value after 'ClinVar_CLNSIG='
                    start_index = line.find('ClinVar_CLNSIG=') + len('ClinVar_CLNSIG=')
                    end_index = line.find(';', start_index)
                    clnsig_value = line[start_index:end_index].strip()
                    clinvar_clnsig_counts[clnsig_value] += 1

        # Step 3: Write the counts to a file
        with open(count_file_path, 'w') as count_file:
            for clnsig_value, count in clinvar_clnsig_counts.items():
                count_file.write(f"'{clnsig_value}': {count} occurrences\n")