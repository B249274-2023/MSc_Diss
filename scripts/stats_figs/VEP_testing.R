library(dplyr)

multiple_snp <- 11686
multiple_indel <- 2777+8909
absent_snp <- 213151
absent_indel <- 13773+36363
present_snp <- 10685998
present_indel <- 424652+585467
all_snp <- 10899149
all_indel <- 438425+621830

# Define the counts for SNPs and indels in each group
data <- list(
  multiple = list(snp = multiple_snp, indel = multiple_indel),
  absent = list(snp = absent_snp, indel = absent_indel),
  presnet = list(snp = present_snp, indel = present_indel),
  all = list(snp = all_snp, indel = all_indel))

# Define the names of the groups
groups <- names(data)

fisher_results <- data.frame(Comparison = character(),
                                OddsRatio = numeric(),
                                ConfInt_Lower = numeric(),
                                ConfInt_Upper = numeric(),
                                P_Value = numeric(),
                                stringsAsFactors = FALSE)

chisq_results <- data.frame(Comparison = character(),
                            Test_Statistic = numeric(),
                            DF = numeric(),
                            P_Value = numeric(),
                            stringsAsFactors = FALSE)

# Loop through each pair of groups and run the Chi-square test
for (i in 1:(length(groups) - 1)) {
  for (j in (i + 1):length(groups)) {
    group1 <- groups[i]
    group2 <- groups[j]
    
    # Create the contingency table
    contingency_table <- matrix(
      c(data[[group1]]$snp, data[[group1]]$indel,
        data[[group2]]$snp, data[[group2]]$indel), nrow = 2, byrow = TRUE)
    colnames(contingency_table) <- c("SNP", "Indel")
    rownames(contingency_table) <- c(group1, group2)
    
    # Perform the Chi-square test
    chisq <- chisq.test(contingency_table)
    fishers <- fisher.test(contingency_table)
    
    # Extract the results
    comparison <- paste(group1, group2, sep = "_vs_")
    odds_ratio <- fishers$estimate
    conf_int <- fishers$conf.int
    p_value_fe <- fishers$p.value
    df <- chisq$parameter
    test_statistic <-  chisq$statistic
    p_value_cs <-  chisq$p.value
    
    # Add the results to the data frames
    fisher_results <- fisher_results %>%
      add_row(Comparison = comparison, 
              OddsRatio = odds_ratio, 
              ConfInt_Lower = conf_int[1], 
              ConfInt_Upper = conf_int[2], 
              P_Value = p_value_fe)
    chisq_results <- chisq_results %>%
    add_row(Comparison = comparison, 
            DF = df,
            Test_Statistic = test_statistic,
            P_Value = p_value_cs)
    
  }
}

# Function to format the results for output
format_results <- function(test_results) {
  formatted_results <- ""
  for (comparison in names(test_results)) {
    result <- test_results[[comparison]]
    formatted_results <- paste(formatted_results,
                               "\nComparison:", comparison,
                               "\n\nTest statistic:", result$statistic,
                               "\np-value:", result$p.value,
                               "\nDegrees of freedom:", ifelse(is.null(result$parameter), "N/A", result$parameter),
                               "\n\n", sep = "\n")
  }
  return(formatted_results)
}

# Write Chi-square results to file
write.table(chisq_results, "chi_square_results.txt", quote = F, row.names = F, sep = '\t')

# Write Fisher's exact test results to file
write.table(fisher_results, "fisher_results_VEP.txt", quote = F, row.names = F, sep = '\t')

# Print a message to indicate that the results have been saved
cat("Results have been saved to 'chi_square_results.txt' and 'fisher_results.txt'.\n")
