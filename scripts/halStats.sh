#$ -cwd  #current dir
#$ -V
#$ -l h_rt=96:00:00   #runtime
#$ -l h_vmem=6G
#$ -l rl9=true

# module unload python
# python/2.7.10
# Module load
module load igmm/apps/python/2.7.10 igmm/apps/R/3.3.0 igmm/apps/BEDTools/2.25.0 igmm/libs/ncurses/6.0 igmm/apps/samtools/1.3 igmm/apps/bcftools/1.3 igmm/apps/vcftools/0.1.13 igmm/libs/ensembl_api/86 igmm/apps/last/847 igmm/compilers/gcc/5.5.0

#/exports/cmvm/eddie/sbms/groups/young-lab/rob/scripts/hal/halStats  /exports/cmvm/eddie/sbms/groups/young-lab/genomes/1509_outgroups.hal --allCoverage > all_coverage.txt

/exports/cmvm/eddie/sbms/groups/young-lab/rob/scripts/hal/halStats --percentID hg19 /exports/cmvm/eddie/sbms/groups/young-lab/genomes/1509_outgroups.hal > percentID.txt
