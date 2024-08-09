#!/bin/sh
#$ -N prom_enh
#$ -cwd  #current dir
#$ -V
#$ -l rl9=true
#$ -l h_rt=2:00:00   #runtime
#$ -l h_vmem=6G
module load igmm/apps/bedtools/2.31.1

bedtools intersect -a cCREs_hg19.bed -b ../vep/species_eQTLs_sorted.bed -wo > prom_enh_present_hg19.bed

#bedtools intersect -a cCREs_hg19.bed -b ../vep/eQTL_ge16.bed -wo > prom_enh_ge16.bed

bedtools intersect -a cCREs_hg19.bed -b ../vep/eQTLs_not_in_species.bed -wo > prom_enh_not_present_hg19.bed

bedtools intersect -a cCREs_hg19.bed -b ../vep/GTEx_eQTLs_sorted.bed -wo > prom_enh_GTEx_hg19.bed

bedtools intersect -a cCREs_hg19.bed -b ../vep/multiple_eQTLs.bed -wo > prom_enh_multiple_hg19.bed