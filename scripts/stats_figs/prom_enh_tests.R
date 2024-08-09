library(dplyr)
library(stats)

## Statistical testing for observed vs expected

# Observed counts
observed_data <- data.frame(
  File = c('present', 'GTEx', 'not_present', 'freq'),
  prom_counts = c(42264, 43056, 746, 92),
  enhD_counts = c(725311, 725311, 6482, 1144),
  enhP_counts = c(137030, 138967, 1801, 272),
  CTCF_counts = c(59710, 60378, 628, 80),
  K4m3_counts = c(29456, 29941, 467, 36)
)

# Expected counts
expected_counts <- c(
  prom_counts = 34803,
  enhD_counts = 667599,
  enhP_counts = 141830,
  CTCF_counts = 56766,
  K4m3_counts = 25537
)

# Initialize a list to store the Chi-squared test results
chi_squared_results <- list()

# Perform Chi-squared test for each file against the expected counts
for (i in 1:nrow(observed_data)) {
  # Create a contingency table for each file
  observed_counts <- as.numeric(observed_data[i, -1])
  
  # Construct the contingency table
  contingency_table <- rbind(observed_counts, expected_counts)
  
  # Perform Chi-squared test
  chi_squared_test <- chisq.test(contingency_table, correct = FALSE)
  
  # Store the results
  chi_squared_results[[observed_data$File[i]]] <- chi_squared_test
}

# View the results
chi_squared_results

## Statistical test for between groups

data <- data.frame(
  File = c('present', 'GTEx', 'not_present', 'multiple'),
  prom_counts = c(42264, 43056, 746, 92),
  enhD_counts = c(725311, 725311, 6482, 1144),
  enhP_counts = c(137030, 138967, 1801, 272),
  CTCF_counts = c(59710, 60378, 628, 80),
  K4m3_counts = c(29456, 29941, 467, 36)
)

#Remove the first column as it's not needed for the test
contingency_table <- as.matrix(data[, -1])

# Perform the Chi-squared test
chisq_test_result <- chisq.test(contingency_table)

# View the results
print(chisq_test_result)


## testing group associations
multiple_vs_present <- matrix(c(42264,	725311.00,	137030.00,	59710.00,	29456.00,
                      92,	1144.00,	272.00,	80.00,	36.00), nrow = 2, byrow = TRUE)
chisq.test(multiple_vs_present)

absent_vs_present <- matrix(c(42264,	725311.00,	137030.00,	59710.00,	29456.00,
                              746,	6482.00,	1801.00,	628.00,	467.00), nrow = 2, byrow = TRUE)
chisq.test(absent_vs_present)

all_vs_present <- matrix(c(42264,	725311.00,	137030.00,	59710.00,	29456.00,
                           43056,	732365.00,	138967.00,	60378.00,	29941.00), nrow = 2, byrow = TRUE)
chisq.test(all_vs_present)
