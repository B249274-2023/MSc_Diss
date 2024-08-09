import os
import pandas as pd

# Directory containing the input files
input_directory = "./"  # Adjust this path as needed
output_file = "prom_enh_counts.txt"

# Values to count in the 13th column
values_to_count = ['prom', 'enhD', 'enhP', 'CTCF', 'K4m3']

# Function to process each file
def process_file(file_path):
    count_dict = {value: 0 for value in values_to_count}
    total_lines = 0

    with open(file_path, 'r') as f:
        for line in f:
            total_lines += 1
            columns = line.strip().split()
            if len(columns) >= 5:
                value = columns[4]
                if value in count_dict:
                    count_dict[value] += 1

    return count_dict, total_lines

# Main processing function
def main():
    all_counts = []

    # Iterate through all the files in the directory
    for filename in os.listdir(input_directory):
        if filename.startswith("prom_enh_") and filename.endswith("_hg19.bed"):
            base_filename = filename[len("prom_enh_"):-len("_hg19.bed")]
            file_path = os.path.join(input_directory, filename)
            count_dict, total_lines = process_file(file_path)
            # Calculate the total count for the file
            total_count = sum(count_dict.get(value, 0) for value in values_to_count)
            # Include the base file name, group counts, and total count in the row
            row = [base_filename] + [count_dict.get(value, 0) for value in values_to_count] + [total_count]
            all_counts.append(row)

    # Create a DataFrame from the collected counts
    df = pd.DataFrame(all_counts, columns=['File'] + values_to_count + ['Total'])

    # Save the DataFrame to a tab-delimited file
    df.to_csv(output_file, sep='\t', index=False)

    print("Processing complete. Output written to:", output_file)

# Run the main function
if __name__ == "__main__":
    main()
