#!/usr/bin/bash

species=('hg19' 'C57B6J' 'bosTau8' 'panTro4' 'gorGor3' 'ponAbe2' 'rheMac3' 'Rattus' 'micOch1' 'jacJac1' 'oryCun2' 'oviBos' 'oviAri3' 'canFam3' 'felCat8' 'loxAfr3']

for genome in "${species[@]}"; do
  # Create a variable to hold the concatenated filename
  concat_file="${genome}_all.bed"
  
  # Find and concatenate all files for the current species
  cat *_"${target}"_temp.bed > "$concat_file"
  
  # Gzip the concatenated file
  gzip "$concat_file"
done
