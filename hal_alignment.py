# Extract alignments from halformat

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
species = ['hg19', 'C57B6J', 'Rattus', 'micOch1', 'jacJac1', 'oryCun2', 'panTro4', 'gorGor3', 'ponAbe2', 'rheMac3', 'oviBos', 'oviAri3', 'bosTau8', 'canFam3', 'felCat8', 'loxAfr3']
species_names = ['human', 'mouse', 'rat', 'prairie_vole', 'egyptian_jerboa', 'rabbit', 'chimpanzee', 'gorilla', 'orangutan', 'macaque', 'musk_ox', 'sheep', 'cow', 'dog', 'cat', 'elephant']

infile = '../../human/GTEx/all_GTEx_hg19.bed'
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
#print total_wc

# Test liftOver -> this takes ~ 4mins for 750 regions -> just over 1 hr in total
# Needs to be shrunk down to ~ 500 regions at a time
for target_genome in species:

#       print target_genome
        complete_liftOver = 0

        if os.path.exists(output_dir + '/' + str(job_id) + '_' + target_genome + '.bed'):
                complete_liftOver += 1

        if os.path.exists(output_dir + '/' + str(job_id) + '_' + target_genome + '_temp.bed'):
                complete_liftOver = 0
#               call('rm -f ' + output_dir + '/' + str(job_id) + '_' + target_genome + '_temp.bed',shell=True)

        if complete_liftOver == 0:

                for window in range(500,(total_wc+500),500):
                        #head_line = window

                        #get_temp = 'head -n ' + str(head_line) + ' temp/' + str(job_id) + '.bed | tail -n500 > temp/' + str(job_id) + '_temp.bed'
                        #print(get_temp)
                        #call(get_temp, shell=True)
                        
                        halLiftover = '/exports/cmvm/eddie/sbms/groups/young-lab/rob/scripts/hal/halLiftover /exports/cmvm/eddie/sbms/groups/young-lab/genomes/1509_outgroups.hal ' + hal_genome + ' temp/' + str(job_id) + '_temp.bed ' + target_genome + ' ' + output_dir + '/' + str(job_id) + '_' + target_genome + '_temp.bed'
                        #print(str(datetime.datetime.now()))
                        print(halLiftover)

                        call(halLiftover, shell=True)
#                       print str(datetime.datetime.now())

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

                call('rm -f ' + output_dir + '/' + str(job_id) + '_' + target_genome + '_temp.bed',shell=True)
                call('gzip ' + output_dir + '/' + str(job_id) + '_' + target_genome + '.bed', shell=True)




