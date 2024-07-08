#!/bin/bash

# Declare an array of species names
species=('hg19' 'C57B6J' 'bosTau8' 'panTro4' 'gorGor3' 'ponAbe2' 'rheMac3' 'Rattus' 'micOch1' 'jacJac1' 'oryCun2' 'oviBos' 'oviAri3' 'canFam3' 'felCat8' 'loxAfr3')

input_dir="shuffled"
output_dir="full_alignments"

# Loop through each genome in the species array
for genome in "${species[@]}"; do
  # Create a variable to hold the concatenated filename
  final_file="${output_dir}/${genome}_shuffled.bed.gz"  

  # Check if the concatenated file already exists
  if [ -f "$final_file" ]; then
    echo "File $final_file already exists. Skipping $genome."
    continue
  fi

  # Find all files for the current species
  species_files=("${input_dir}"/*_"${genome}".bed.gz)
  
  # Check if there are exactly 100 files
  if [ ${#species_files[@]} -eq 100 ]; then
    # Create temporary concatenated file
    concat_file="${output_dir}/${genome}_shuffled.bed"
    
    # Concatenate all files for the current species
    zcat "${species_files[@]}" > "$concat_file"
    
    # Gzip the concatenated file
    gzip "$concat_file"
    
    echo "Processed $genome with 100 files."
  else
    echo "Skipping $genome, found ${#species_files[@]} files instead of 100."
  fi
done

