library(dplyr)
library(ggplot2)
library(wesanderson)


tissues <-c('Adipose - Subcutaneous', 'Adipose - Visceral Omentum', 'Adrenal Gland', 'Artery - Aorta', 'Artery - Coronary', 'Artery - Tibial', 'Brain - Anterior cingulate cortex (BA24)', 'Brain - Caudate (basal ganglia)', 'Brain - Cerebellar Hemisphere', 'Brain - Cerebellum', 'Brain - Cortex', 'Brain - Frontal Cortex (BA9)', 'Brain - Hippocampus', 'Brain - Hypothalamus', 'Brain - Nucleus accumbens (basal ganglia)', 'Brain - Putamen (basal ganglia)', 'Breast - Mammary Tissue', 'Cells - EBV-transformed lymphocytes', 'Cells - Cultured fibroblasts', 'Colon - Sigmoid', 'Colon - Transverse', 'Esophagus - Gastroesophageal Junction', 'Esophagus - Mucosa', 'Esophagus - Muscularis', 'Heart - Atrial Appendage', 'Heart - Left Ventricle', 'Liver', 'Lung', 'Muscle - Skeletal', 'Nerve - Tibial', 'Ovary', 'Pancreas', 'Pituitary', 'Prostate', 'Skin - Not Sun Exposed (Suprapubic)', 'Skin - Sun Exposed (Lower leg)', 'Small Intestine - Terminal Ileum', 'Spleen', 'Stomach', 'Testis', 'Thyroid', 'Uterus', 'Vagina', 'Whole Blood')

# Create a mapping of original tissue names to the new tissue names
original_tissues <- c('Adipose_Subcutaneous', 'Adipose_Visceral_Omentum', 'Adrenal_Gland', 
                      'Artery_Aorta', 'Artery_Coronary', 'Artery_Tibial', 
                      'Brain_Anterior_cingulate_cortex_BA24', 'Brain_Caudate_basal_ganglia', 
                      'Brain_Cerebellar_Hemisphere', 'Brain_Cerebellum', 'Brain_Cortex', 
                      'Brain_Frontal_Cortex_BA9', 'Brain_Hippocampus', 'Brain_Hypothalamus', 
                      'Brain_Nucleus_accumbens_basal_ganglia', 'Brain_Putamen_basal_ganglia', 
                      'Breast_Mammary_Tissue', 'Cells_EBV-transformed_lymphocytes', 
                      'Cells_Transformed_fibroblasts', 'Colon_Sigmoid', 'Colon_Transverse', 
                      'Esophagus_Gastroesophageal_Junction', 'Esophagus_Mucosa', 
                      'Esophagus_Muscularis', 'Heart_Atrial_Appendage', 'Heart_Left_Ventricle', 
                      'Liver', 'Lung', 'Muscle_Skeletal', 'Nerve_Tibial', 'Ovary', 'Pancreas', 
                      'Pituitary', 'Prostate', 'Skin_Not_Sun_Exposed_Suprapubic', 
                      'Skin_Sun_Exposed_Lower_leg', 'Small_Intestine_Terminal_Ileum', 
                      'Spleen', 'Stomach', 'Testis', 'Thyroid', 'Uterus', 'Vagina', 'Whole_Blood')

# Create a mapping data frame
tissue_mapping <- data.frame(
  Original = original_tissues,
  New = tissues
)

# Read in Average Conservation File
data <- read.table("eQTL_locations/average_conservation.txt", header = TRUE, sep = "\t")

# Join the data with the mapping to get the new tissue names
data <- merge(data, tissue_mapping, by.x = "Tissue_Type", by.y = "Original")
data <- data %>% select(-Tissue_Type) %>% rename(Tissue_Type = New)


tissue_groups <- list(
  Neurological = c('Brain - Anterior cingulate cortex (BA24)', 'Brain - Caudate (basal ganglia)', 
                   'Brain - Cerebellar Hemisphere', 'Brain - Cerebellum', 'Brain - Cortex', 
                   'Brain - Frontal Cortex (BA9)', 'Brain - Hippocampus', 'Brain - Hypothalamus', 
                   'Brain - Nucleus accumbens (basal ganglia)', 'Brain - Putamen (basal ganglia)', 
                   'Nerve - Tibial'),
  Immunological = c('Cells - EBV-transformed lymphocytes', 'Cells - Cultured fibroblasts', 'Spleen', 
                    'Whole Blood'),
  Reproductive = c('Breast - Mammary Tissue', 'Ovary', 'Prostate', 'Testis', 'Uterus', 'Vagina'),
  Other = c('Adipose - Subcutaneous', 'Adipose - Visceral Omentum', 'Adrenal Gland', 'Artery - Aorta', 
            'Artery - Coronary', 'Artery - Tibial', 'Colon - Sigmoid', 'Colon - Transverse', 
            'Esophagus - Gastroesophageal Junction', 'Esophagus - Mucosa', 'Esophagus - Muscularis', 
            'Heart - Atrial Appendage', 'Heart - Left Ventricle', 'Liver', 'Lung', 'Muscle - Skeletal', 
            'Pancreas', 'Pituitary', 'Skin - Not Sun Exposed (Suprapubic)', 
            'Skin - Sun Exposed (Lower leg)', 'Small Intestine - Terminal Ileum', 'Stomach', 'Thyroid')
)

# Convert tissue groups to a data frame
tissue_group_df <- stack(tissue_groups)
colnames(tissue_group_df) <- c('Tissue_Type', 'TissueGroup')

## Plot 1 <- histogram of 

# Merge tissue group information with the data
data <- merge(data, tissue_group_df, by = 'Tissue_Type')
data <- data %>% arrange(TissueGroup, Tissue_Type)

# Create the histogram
plot_ordered <- ggplot(data, aes(x = reorder(Tissue_Type, Average_Conservation_Percentage), y = Average_Conservation_Percentage, fill = TissueGroup)) +
  geom_bar(stat = 'identity') + 
  theme_classic()+ 
  theme(axis.text.x = element_text(angle = 60, hjust = 1, vjust = 1), legend.position = "left") +
  ylim(0,50) + 
  labs(title = 'Average Conservation Rate by Tissue Type', 
       x = 'Tissue Type', 
       y = 'Average Conservation Rate (%)', 
       fill = 'Tissue Group') +
  scale_fill_manual(values = wes_palette("GrandBudapest2", n = 4))
print(plot_ordered)
ggsave("average_tissue_scores_ordered.png", plot = plot_ordered, width = 10, height = 7)

data$Tissue_Type <- factor(data$Tissue_Type, levels = unique(data$Tissue_Type[order(data$TissueGroup)]))


plot_grouped <- ggplot(data, aes(x = Tissue_Type, y = Average_Conservation_Percentage, fill = TissueGroup)) +
  geom_bar(stat = 'identity') + 
  theme_classic()+ 
  theme(axis.text.x = element_text(angle = 60, hjust = 1, vjust = 1)) +
  scale_y_continuous(expand = expansion(mult = c(0, 0.05))) +
  theme(legend.position="left", axis.title.x = element_blank(), legend.title = element_blank())+
  labs(title = 'Average Conservation Rate by Tissue Type', 
       y = 'Average Conservation Rate (%)', 
       fill = 'Tissue Group') +
  scale_fill_manual(values = wes_palette("GrandBudapest2", n = 4)) 
print(plot_grouped)
ggsave("average_tissue_scores_grouped.png", plot = plot_grouped, width = 10, height = 7)




## Plot 2 <-  box plot
# Define the mapping from species codes to human-readable names
species_mapping <- data.frame(
  species_code = c('panTro4', 'gorGor3', 'ponAbe2', 'rheMac3', 'felCat8', 'canFam3', 'oviBos', 'bosTau8', 'oviAri3', 'loxAfr3', 'oryCun2', 'jacJac1', 'micOch1', 'Rattus', 'C57B6J'),
  species_name = c('Chimpanzee', 'Gorilla', 'Orangutan', 'Rhesus Macaque', 'Cat', 'Dog', 'Musk Ox', 'Cow', 'Sheep', 'Elephant', 'Rabbit', 'Egyptian Jerboa', 'Prairie Vole', 'Rat', 'Mouse')
)

# Function to read data from each file and calculate adjusted scores
read_species_data <- function(file_path, species_mapping) {
  data <- read.table(file_path, header = TRUE, sep = "\t")
  species_code <- basename(file_path)
  species_code <- sub("_conservation_scores.txt$", "", species_code)
  
  species_name <- species_mapping$species_name[species_mapping$species_code == species_code]
  
  avg_conservation_rate <- mean(data$Conservation_Percentage, na.rm = TRUE)
  data <- data %>%
    mutate(Species = species_name)
  
  return(data)
}

# Folder containing the files
folder_path <- "eQTL_locations/species_conservation"

# List all files in the folder
files <- list.files(folder_path, full.names = TRUE, pattern = "\\.txt$")
# Read and combine all data
all_data <- do.call(rbind, lapply(files, read_species_data, species_mapping))
all_data <- merge(all_data, tissue_mapping, by.x = "Tissue_Type", by.y = "Original")
all_data <- all_data %>% select(-Tissue_Type) %>% rename(Tissue_Type = New)

all_data <- merge(all_data, tissue_group_df, by = 'Tissue_Type')
all_data <- data %>% arrange(TissueGroup, Tissue_Type)

# Calculate the species average
species_avg <- all_data %>%
  group_by(Species) %>%
  summarize(AvgConservationRate = mean(Conservation_Percentage, na.rm = TRUE))

# Merge average data with the original data
plot_data <- merge(all_data, species_avg, by = "Species")
plot_data$Species <- factor(plot_data$Species, levels = species_mapping$species_name)

# plot figure
boxplots<- ggplot(plot_data, aes(x = Species, y = Conservation_Percentage)) +
  geom_boxplot() +
  geom_jitter(aes(color = TissueGroup), width = 0.2, alpha = 0.9) +
  labs(title = 'Conservation Rate by Species For All Tissue Types',
       y = 'Conservation Rate (%)') +
  ylim(0,100)+
  theme_classic() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 16), axis.title.x = element_blank(), legend.position = "right", axis.text.y = element_text(size = 16), axis.title.y = element_text(size = 18), plot.title = element_text(size = 22)) +
  scale_colour_manual(values = wes_palette("GrandBudapest2", n = 4))
print(boxplots)
ggsave("tissue_boxplots.png", plot = boxplots, width = 8, height = 7)


