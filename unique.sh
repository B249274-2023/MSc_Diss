#!/usr/bin/bash

declare -a species=('C57B6J' 'bosTau8' 'panTro4' 'gorGor3' 'ponAbe2' 'rheMac3' 'Rattus' 'micOch1' 'jacJac1' 'oryCun2' 'oviBos' 'oviAri3' 'canFam3' 'felCat8' 'loxAfr3')

# Output file for row counts
output_file="shuffled_row_counts.txt"

# Initialize the output file
echo -n "" > $output_file


for genome in "${species[@]}" 
	do
		infile="full_alignments/${genome}_shuffled.bed.gz"
		outfile="full_alignments/${genome}_unique_shuffled.bed"
    	
		# Process the infile to create the outfile
		zcat "${infile}" | awk '{print $4}' | sort | uniq > "${outfile}"

    	# Count the number of lines in the outfile
		line_count=$( wc -l < "${outfile}")

		# Calculate the conservation rate 
		conservation_rate=$(echo "scale=3; (${line_count}/11959405)*100" | bc)

   		# Write the genome name, row count, and conservation rate to the output file
		echo "${genome} ${line_count} ${conservation_rate}" >> ${output_file}

		# Compress the outfile
		gzip "${outfile}"
		
	done
