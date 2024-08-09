import os
import gzip
from collections import defaultdict

# Directory containing the input files
input_directory = "../../../human/GTEx/GTEx_Analysis_v6p_eQTL/"
output_file = "../eQTL_tissue_appearances.txt"

# Dictionary to hold the counts and file names
data_dict = defaultdict(lambda: {'count': 0, 'files': set()})

# Function to process each file
def process_file(file_path, base_name):
    with gzip.open(file_path, 'rt') as f:
        for line in f:
            columns = line.strip().split()
            if len(columns) >= 5:
                id = columns[0]
                key = (id)
                data_dict[key]['count'] += 1
                data_dict[key]['files'].add(base_name)

# Iterate through all the files in the directory
for filename in os.listdir(input_directory):
    if filename.endswith("_Analysis.v6p.signif_snpgene_pairs.txt.gz"):
        file_path = os.path.join(input_directory, filename)
        base_name = filename.replace("_Analysis.v6p.signif_snpgene_pairs.txt.gz", "")
        process_file(file_path, base_name)

# Write the results to the output file
with open(output_file, 'w') as out_f:
    out_f.write("GTEx_ID\tCount\tFiles\n")
    for key, value in data_dict.items():
        id = key
        count = value['count']
        files = ",".join(value['files'])
        file_count = len(value['files'])
        out_f.write("{0}\t{1}\t{2}\t{3}\n".format(id, count, file_count, files))

print("Processing complete. Output written to:", output_file)
