# Load necessary libraries
library(dplyr)
library(Hmisc)

# Sample data
eQTL_count <- read.table("tissue_eQTL_counts.txt", sep = "\t", header = T)
cons_rate <- read.table("eQTL_locations/average_conservation.txt", header = TRUE, sep = "\t")

data <-  merge(eQTL_count, cons_rate, by= "Tissue_Type")
data <-  subset(data, select = -c(Total_Conservation))

# Rank the data
data <- data %>%
  mutate(
    Conservation_Rank = rank(-Average_Conservation_Percentage), # rank in descending order
    eQTLs_Rank = rank(-Number_of_eQTLs), # rank in descending order
    sample_Rank = rank(-sample_size)
  )

# Calculate Spearman rank correlation
spearman_result <- rcorr(as.matrix(data[, c("Conservation_Rank", "eQTLs_Rank")]), type = "spearman")
rank2 <- rcorr(as.matrix(data[, c("sample_Rank", "eQTLs_Rank")]), type = "spearman")
rank3 <- rcorr(as.matrix(data[, c("sample_Rank", "Conservation_Rank")]), type = "spearman")


# Output the results
correlation <- spearman_result$r[1, 2]
p_value <- spearman_result$P[1, 2]

correlation <- rank2$r[1, 2]
p_value <- rank2$P[1, 2]

cat("Spearman Rank Correlation: ", correlation, "\n")
cat("P-value: ", p_value, "\n")
