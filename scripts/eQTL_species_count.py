import os
import gzip
from collections import defaultdict

# Directory containing the input files
input_directory = "../full_alignments"
output_file = "../eQTL_species_count.txt"
temp_file = "../eQTL_temp_count.txt"

# Function to process each file and return a dictionary of counts and files
def process_file(file_path, base_name):
    local_dict = defaultdict(lambda: {'count': 0, 'files': set()})
    with gzip.open(file_path, 'rt') as f:
        for line in f:
            columns = line.strip().split()
            if len(columns) >= 1:  # We need at least one column
                id = columns[0]
                local_dict[id]['count'] += 1
                local_dict[id]['files'].add(base_name)
    return local_dict

# Aggregate results from all files and periodically write to a temporary file
def aggregate_results():
    global_dict = defaultdict(lambda: {'count': 0, 'files': set()})

    # Iterate through all the files in the directory
    for filename in os.listdir(input_directory):
        if filename.endswith("_unique_all.bed.gz"):
            file_path = os.path.join(input_directory, filename)
            base_name = filename.replace("_unique_all.bed.gz", "")
            local_dict = process_file(file_path, base_name)
            
            # Update the global dictionary with local results
            for id, data in local_dict.items():
                global_dict[id]['count'] += data['count']
                global_dict[id]['files'].update(data['files'])
            
            # Write intermediate results to the temp file to free memory
            write_temp_results(global_dict)
            global_dict.clear()

    # Return the final global dictionary
    return global_dict

# Write intermediate results to the temporary file
def write_temp_results(data_dict):
    with open(temp_file, 'a') as temp_f:
        for key, value in data_dict.items():
            id = key
            count = value['count']
            files = ",".join(value['files'])
            file_count = len(value['files'])
            temp_f.write("{0}\t{1}\t{2}\t{3}\n".format(id, count, file_count, files))

# Merge intermediate results from the temporary file
def merge_temp_results():
    final_dict = defaultdict(lambda: {'count': 0, 'files': set()})
    
    with open(temp_file, 'r') as temp_f:
        for line in temp_f:
            columns = line.strip().split('\t')
            if len(columns) == 4:
                id = columns[0]
                count = int(columns[1])
                file_count = int(columns[2])
                files = set(columns[3].split(","))
                final_dict[id]['count'] += count
                final_dict[id]['files'].update(files)

    return final_dict

# Main processing function
def main():
    # Remove existing temporary file
    if os.path.exists(temp_file):
        os.remove(temp_file)

    # Aggregate results and write to temp file
    aggregate_results()

    # Merge results from the temp file
    final_dict = merge_temp_results()

    # Write the final results to the output file
    with open(output_file, 'w') as out_f:
        out_f.write("GTEx_ID\tCount\tFile_Count\tFiles\n")
        for key, value in final_dict.items():
            id = key
            count = value['count']
            files = ",".join(value['files'])
            file_count = len(value['files'])
            out_f.write("{0}\t{1}\t{2}\t{3}\n".format(id, count, file_count, files))

    print("Processing complete. Output written to:", output_file)

# Run the main function
if __name__ == "__main__":
    main()