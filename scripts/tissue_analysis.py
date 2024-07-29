import os

species_names = ['mouse', 'cow', 'chimpanzee', 'gorilla', 'orangutan', 'macaque', 'rat', 'prairie_vole', 'egyptian_jerboa', 'rabbit', 'musk_ox', 'sheep', 'dog', 'cat', 'elephant']
species = ['C57B6J', 'bosTau8', 'panTro4', 'gorGor3', 'ponAbe2', 'rheMac3', 'Rattus', 'micOch1', 'jacJac1', 'oryCun2', 'oviBos', 'oviAri3', 'canFam3', 'felCat8', 'loxAfr3']

tissue_types = ['Adipose_Subcutaneous', 'Adipose_Visceral_Omentum', 'Adrenal_Gland', 'Artery_Aorta', 'Artery_Coronary', 'Artery_Tibial', 'Brain_Anterior_cingulate_cortex_BA24', 'Brain_Caudate_basal_ganglia', 'Brain_Cerebellar_Hemisphere', 'Brain_Cerebellum', 'Brain_Cortex', 'Brain_Frontal_Cortex_BA9', 'Brain_Hippocampus', 'Brain_Hypothalamus', 'Brain_Nucleus_accumbens_basal_ganglia', 'Brain_Putamen_basal_ganglia', 'Breast_Mammary_Tissue', 'Cells_EBV-transformed_lymphocytes', 'Cells_Transformed_fibroblasts', 'Colon_Sigmoid', 'Colon_Transverse', 'Esophagus_Gastroesophageal_Junction', 'Esophagus_Mucosa', 'Esophagus_Muscularis', 'Heart_Atrial_Appendage', 'Heart_Left_Ventricle', 'Liver', 'Lung', 'Muscle_Skeletal', 'Nerve_Tibial', 'Ovary', 'Pancreas', 'Pituitary', 'Prostate', 'Skin_Not_Sun_Exposed_Suprapubic', 'Skin_Sun_Exposed_Lower_leg', 'Small_Intestine_Terminal_Ileum', 'Spleen', 'Stomach', 'Testis', 'Thyroid', 'Uterus', 'Vagina', 'Whole_Blood']

base_directory = "../eQTL_locations/"
eQTL_counts_file = "../tissue_eQTL_counts.txt"

# Read the total number of eQTLs for each tissue type
eQTL_counts = {}
with open(eQTL_counts_file, 'r') as f:
    for line in f:
        columns = line.strip().split()
        if len(columns) >= 2:
            tissue_name = columns[0]
            count = int(columns[1])
            eQTL_counts[tissue_name] = count

# Create a directory to store species conservation files
species_conservation_dir = os.path.join(base_directory, "species_conservation")
if not os.path.exists(species_conservation_dir): # Check if the directory exists, if not make it
    os.makedirs(species_conservation_dir)

# Initialize dictionaries to store conservation scores per species
species_conservation = {sp: [] for sp in species}

# Open the file to store the average percent of eQTLs conserved for each tissue type
avg_conservation_file = os.path.join(base_directory, "average_conservation.txt")
with open(avg_conservation_file, "w") as avg_outfile:
    avg_outfile.write("Tissue_Type\tTotal_Conservation\tAverage_Conservation_Percentage\n")

    # Loop through each tissue type folder
    for tissue in tissue_types:
        tissue_path = os.path.join(base_directory, tissue)
        
        # Check if the folder exists
        if not os.path.exists(tissue_path):
            continue
        
        # Open the output file for writing
        output_file = os.path.join(base_directory, "{0}_conservation.txt".format(tissue))
        
        total_conservation_percentage = 0
        species_count = 0
        total_eQTLs = eQTL_counts.get(tissue, 1)  # Default count to 1 to avoid division by zero if nothing present
        
        with open(output_file, "w") as outfile:
            outfile.write("Species\tLine_Count\tTissue_eQTLs\tConservation_Percentage\n")
            # Loop through each file in the folder
            for filename in os.listdir(tissue_path):
                if filename.endswith(".bed"):
                    # Extract species name from the filename
                    species_name = filename.split('_')[0]
                    
                    # Construct the full file path
                    file_path = os.path.join(tissue_path, filename)
                    
                    # Count the number of lines in the file
                    with open(file_path, 'rt') as file:
                        line_count = sum(1 for _ in file)
                    
                    # Calculate the conservation percentage
                    conservation_percentage = (float(line_count) / total_eQTLs) * 100
                    total_conservation_percentage += conservation_percentage
                    species_count += 1

                    # Add the conservation percentage to the species dictionary
                    if species_name in species:
                        species_conservation[species_name].append((tissue, conservation_percentage))

                    # Write the result to the output file
                    outfile.write("{0}\t{1}\t{2}\t{3:.3f}\n".format(species_name, line_count, total_eQTLs, conservation_percentage))
        
        # Calculate the average conservation percentage for the tissue type
        if species_count > 0:
            avg_conservation_percentage = total_conservation_percentage / species_count
        else:
            avg_conservation_percentage = 0
        
        # Write the average conservation percentage to the average conservation file
        avg_outfile.write("{0}\t{1}\t{2:.3f}\n".format(tissue, total_conservation_percentage, avg_conservation_percentage))

# Calculate the overall average conservation rate for each species
species_overall_conservation_rate = {}
for sp in species:
    species_conservation_sum = sum(conservation for _, conservation in species_conservation[sp])
    species_conservation_count = len(species_conservation[sp])
    
    if species_conservation_count > 0:
        overall_conservation_rate = species_conservation_sum / species_conservation_count
    else:
        overall_conservation_rate = 1  # Default to 1 if no data available
    
    species_overall_conservation_rate[sp] = overall_conservation_rate

# Write the conservation scores for each species to individual files, adjusting by the new species-specific overall conservation rate
for sp in species:
    species_file = os.path.join(species_conservation_dir, "{0}_conservation_scores.txt".format(sp))
    with open(species_file, "w") as sp_outfile:
        sp_outfile.write("Tissue_Type\tConservation_Percentage\tAdjusted_Conservation_Rate\n")
        for tissue, conservation in species_conservation[sp]:
            adjusted_conservation_rate = conservation / species_overall_conservation_rate[sp]
            sp_outfile.write("{0}\t{1:.3f}\t{2:.3f}\n".format(tissue, conservation, adjusted_conservation_rate))

# Open the final output file for writing unique row counts for each tissue type
final_output_file = os.path.join(base_directory, "tissue_unique_eQTL_count.txt")
with open(final_output_file, "w") as final_outfile:
    final_outfile.write("Tissue_Type\tUnique_Row_Count\n")
    
    # Loop through each tissue type folder
    for tissue in tissue_types:
        tissue_path = os.path.join(base_directory, tissue)
        
        # Check if the folder exists
        if not os.path.exists(tissue_path):
            continue
        
        # Set to store unique lines
        unique_lines = set()
        
        # Loop through each file in the folder
        for filename in os.listdir(tissue_path):
            if filename.endswith(".bed"):
                # Construct the full file path
                file_path = os.path.join(tissue_path, filename)
                
                # Read and add lines to the set
                with open(file_path, 'rt') as f:
                    for line in f:
                        unique_lines.add(line.strip())
        
        # Count the number of unique lines
        unique_line_count = len(unique_lines)
        
        # Write the result to the final output file
        final_outfile.write("{0}\t{1}\n".format(tissue, unique_line_count))
