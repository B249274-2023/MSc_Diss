library(dplyr)
library(ggplot2)
library(forcats)

species = c('panTro4', 'gorGor3', 'ponAbe2', 'rheMac3', 'felCat8', 'canFam3', 'oviBos', 'bosTau8', 'oviAri3', 'loxAfr3', 'oryCun2', 'jacJac1', 'micOch1', 'Rattus', 'C57B6J')
species_names = c('Chimpanzee', 'Gorilla', 'Orangutan', 'Rhesus', 'Cat', 'Dog', 'Musk Ox', 'Cow', 'Sheep', 'Elephant', 'Rabbit', 'Egyptian Jeroba', 'Prairie Vole', 'Rat', 'Mouse')

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
write.table(fisher_results_df, file = "fisher_results.txt", row.names = FALSE, sep = "\t", qoute = F)

forest_plot <- ggplot(fisher_results_df, aes(x = OddsRatio, y = Species)) +
  geom_point(size = 2) +
  geom_errorbarh(aes(xmin = ConfInt_Lower, xmax = ConfInt_Upper), height = 1) +
  xlim(0, 3.5) +
  geom_vline(xintercept = 1, color = "red", alpha = 0.5) +
  labs(title = "Forest Plot of Odds Ratios with 95% Confidence Intervals") +
  xlab("Odds Ratio (95% CI)") +
  theme_classic()+
  scale_y_discrete(limits = rev(species))
plot(forest_plot)
ggsave("forest_plot.png", forest_plot, width = 10, height = 8)
