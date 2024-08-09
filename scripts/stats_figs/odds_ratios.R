library(dplyr)
library(ggplot2)
library(forcats)

species = c('panTro4', 'gorGor3', 'ponAbe2', 'rheMac3', 'felCat8', 'canFam3', 'oviBos', 'bosTau8', 'oviAri3', 'loxAfr3', 'oryCun2', 'jacJac1', 'micOch1', 'Rattus', 'C57B6J')
species_names = c('Chimpanzee', 'Gorilla', 'Orangutan', 'Rhesus', 'Cat', 'Dog', 'Musk Ox', 'Cow', 'Sheep', 'Elephant', 'Rabbit', 'Egyptian Jeroba', 'Prairie Vole', 'Rat', 'Mouse')

# Map species to species names
species_mapping <- data.frame(
  Species = c('panTro4', 'gorGor3', 'ponAbe2', 'rheMac3', 'felCat8', 'canFam3', 'oviBos', 'bosTau8', 'oviAri3', 'loxAfr3', 'oryCun2', 'jacJac1', 'micOch1', 'Rattus', 'C57B6J'),
  SpeciesName = c('Chimpanzee', 'Gorilla', 'Orangutan', 'Rhesus', 'Cat', 'Dog', 'Musk Ox', 'Cow', 'Sheep', 'Elephant', 'Rabbit', 'Egyptian Jeroba', 'Prairie Vole', 'Rat', 'Mouse')
)

# read in the files with row counts
all_counts <- read.table("all_row_counts.txt", sep = " ")
all_counts <- all_counts[order(all_counts$V2, decreasing = T),]
shuffled_counts <-  read.table("shuffled_row_counts.txt", sep = " ")
shuffled_counts <- shuffled_counts[order(shuffled_counts$V2, decreasing = T),]

contingency_tables <- list()

fisher_results_df <- data.frame(Species = character(),
                                OddsRatio = numeric(),
                                ConfInt_Lower = numeric(),
                                ConfInt_Upper = numeric(),
                                P_Value = numeric(),
                                stringsAsFactors = FALSE)

# go through each species and create the contingency tables
for (sp in species) {
  # get the counts for the current species
  all_count <- all_counts %>% filter(V1 == sp) %>% pull(V2)
  shuffled_count <- shuffled_counts %>% filter(V1 == sp) %>% pull(V2)
  
  # Calculate the other values for the contingency table
  all_count_complement <- 11959405 - all_count
  shuffled_count_complement <- 11959405 - shuffled_count
  
  # Create the 2x2 contingency table
  contingency_table <- matrix(c(all_count, all_count_complement, 
                                shuffled_count, shuffled_count_complement),
                              nrow = 2, byrow = TRUE)
  rownames(contingency_table) <- c("All", "Shuffled")
  colnames(contingency_table) <- c("Count", "Complement")
  
  # Add the contingency table to the list
  contingency_tables[[sp]] <- contingency_table
  
  # Run Fisher's exact test
  fisher_test <- fisher.test(contingency_table)
  
  # Extract the results
  odds_ratio <- fisher_test$estimate
  conf_int <- fisher_test$conf.int
  p_value <- fisher_test$p.value
  
  # Add the results to the data frame
  fisher_results_df <- fisher_results_df %>%
    add_row(Species = sp, 
            OddsRatio = odds_ratio, 
            ConfInt_Lower = conf_int[1], 
            ConfInt_Upper = conf_int[2], 
            P_Value = p_value)
}

# Save the results to a file
write.table(fisher_results_df, file = "fisher_results_OR.txt", row.names = FALSE, sep = "\t", quote = F)



fishers_results <- read.table("fisher_results_OR.txt", header = T)
fishers_results <- merge(fishers_results, species_mapping, by = "Species")
fishers_results$SpeciesName <- factor(fishers_results$SpeciesName, levels = species_mapping$SpeciesName)
fishers_results$LogOddsRatio <- log(fishers_results$OddsRatio)
fishers_results$logCU <- log(fishers_results$ConfInt_Upper)
fishers_results$logCL <- log(fishers_results$ConfInt_Lower)
fishers_results <- fishers_results %>% arrange(desc(LogOddsRatio))
write.table(fishers_results, "fishers_lOR.txt", quote = F, sep = '\t', row.names = F)

#making the plot for GTEx eQTL
png(filename = "forest_plot2.png", width = 1920, height = 1080, res = 175)
par(mar = c(5, 8, 4, 2))

# define axes limits
xlim <- c(-1,1.5)
ylim <- c(0.5, 15.5)

plot(1, type = "n", xlim = xlim, ylim = ylim, 
     xaxt = "n", yaxt = "n", xlab = "log2(Odds Ratio)", ylab = "", bty = "n")
title(main="Forest Plot of the Odds Ratio For All 15 Species")

# Add x-axis
axis(1)

# Add y-axis with species labels
axis(2, at = 1:15, labels = rev(fishers_results$SpeciesName), las = 2)

# Plot the data
for (i in 1:15) {
  species <- 16 - i  # Reverse the order for proper display
  
  lower_ext <- fishers_results$logCL[i]
  upper_ext <- fishers_results$logCU[i]
  
  segments(lower_ext, species, upper_ext, species, col = "blue3", lwd = 2)
  
  # Vertical lines at the ends of the confidence interval
  segments(lower_ext, species - 0.3, lower_ext, species + 0.3, col = "blue3", lwd = 1)
  segments(upper_ext, species - 0.3, upper_ext, species + 0.3, col = "blue3", lwd = 1)
  
  points(fishers_results$LogOddsRatio[i], species, pch = 19, col = "blue4")
  
}
abline(v=0,col="red3")
dev.off()

