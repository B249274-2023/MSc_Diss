#get alignments from halformat

import os
from subprocess import call
import subprocess
import random
import sys
import datetime
import time
import re
sys.path.insert(0, '/exports/cmvm/eddie/sbms/groups/young-lab/rob/scripts/')
from modules import *
from Bio.Seq import Seq

job_id = sys.argv[1] # job id can now accept jobs of 1 to 100

# quick test
hal_genome = 'hg19'
species = ['gorGor3', 'ponAbe2', 'rheMac3']
species_names = ['gorilla',  'orangutan', 'macaque']



infile = '../../../human/GTEx/all_GTEx_hg19.bed'
genome = 'hg19'
genome_dir = genome
output_dir = 'temp'

if genome == 'mm10':
        hal_genome = 'C57B6J'
else:
        hal_genome = genome


print(job_id)
print(infile)

replicate = str(int(job_id) % 100)
print(replicate)

progress = 0
with open(infile) as infile, open('temp/' + str(job_id) + '.bed', 'w') as outfile:
        for line in infile:

                if 'ID' not in line:
                        progress += 1
                        if ((progress % 100) == (int(replicate))):
                                chrom = line.split()[0]
                                start = line.split()[1]
                                end = line.split()[2]
                                build = line.split()[3]

                                midpoint = (int(start) + int(end))/2

                                id = chrom + ':' + start + '-' + end
#                       id = chrom + ':' + start + '-' + end + ':' + line.split()[3]
#                       id = line.split()[3]

                                if 'fix' not in line:
                                    outfile.write(bed_write(chrom = chrom, start = start, score = 0, end = end, name = build) + '\n')

list_infile = 'temp/' + job_id + '.bed'
#mv = 'mv ' + list_infile + '.2 ' + list_infile
#print mv
#call(mv, shell=True)
total_wc = int(subprocess.check_output('wc -l ' + list_infile + ' | awk \'{print $1}\'', shell=True).rstrip())
print total_wc

for target_genome in species:

        print target_genome
        complete_liftOver = 0

        if os.path.exists(output_dir + '/' + str(job_id) + '_' + target_genome + '.bed.gz'):
                complete_liftOver += 1

        if os.path.exists(output_dir + '/' + str(job_id) + '_' + target_genome + '_temp.bed'):
                complete_liftOver = 0
                #call('rm -f ' + output_dir + '/' + str(job_id) + '_' + target_genome + '_temp.bed',shell=True)

        if complete_liftOver == 0:

                halLiftover = '/exports/cmvm/eddie/sbms/groups/young-lab/rob/scripts/hal/halLiftover /exports/cmvm/eddie/sbms/groups/young-lab/genomes/1509_outgroups.hal ' + hal_genome + ' temp/' + str(job_id) + '.bed ' + target_genome + ' ' + output_dir + '/' + str(job_id) + '_' + target_genome + '_temp.bed'
                print(halLiftover)
                call(halLiftover, shell=True)

                # Concatenate or move results 
                if os.path.exists(output_dir + '/' + str(job_id) + '_' + target_genome + '.bed'):
                        cat = 'cat ' + output_dir + '/' + str(job_id) + '_' + target_genome + '.bed ' + output_dir + '/' + str(job_id) + '_' + target_genome + '_temp.bed > ' + output_dir + '/' + str(job_id) + '_' + target_genome + '.bed2'
                        print(cat)
                        call(cat, shell=True)
                        mv = 'mv ' + output_dir + '/' + str(job_id) + '_' + target_genome + '.bed2 ' + output_dir + '/' + str(job_id) + '_' + target_genome + '.bed'
                        print(mv)
                        call(mv, shell=True)

                else:
                        mv = 'mv ' + output_dir + '/' + str(job_id) + '_' + target_genome + '_temp.bed ' + output_dir + '/' + str(job_id) + '_' + target_genome + '.bed'
                        print (mv)
                        call(mv, shell=True)

                # Clean up temporary file
                call('rm -f ' + output_dir + '/' + str(job_id) + '_' + target_genome + '_temp.bed',shell=True)
                #Compress the final output
                call('gzip ' + output_dir + '/' + str(job_id) + '_' + target_genome + '.bed', shell=True)

                complete_liftOver = 1

        # If the liftover is complete, skip to the next target genome
        if complete_liftOver == 1:
                continue


