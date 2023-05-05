#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Code to submit all the crest jobs
Author: Arnab Majumdar
'''

import glob
import os
import shutil


def main():
    current_folder = './'
    foldername = 'crest_calculations'

    for filename in sorted(glob.glob('*.xyz')):
         name = filename.split('.xyz')[0]
         if os.path.exists(foldername + '/' + name + '/') == False:
            os.makedirs(foldername + '/' + name + '/')
         target_folder = foldername + '/' + name + '/'
         shutil.copy2(os.path.join(current_folder, filename), target_folder)
         subsh_file = foldername + '/' + name + '/' + 'submit.sh'
         msubsh_file = foldername + '/' + 'master_submit' + '.sh'

         with open(subsh_file, 'w') as subsh:
                subsh.write('#!/bin/bash' + '\n')
                subsh.write('#SBATCH -N 1' + '\n')
                subsh.write('#SBATCH --tasks-per-node=16' + '\n')
                subsh.write('#SBATCH --mem-per-cpu=7G' + '\n')
                subsh.write('#SBATCH -t 500:00:00' + '\n')
                subsh.write('#SBATCH -J ' + name + '\n')
                subsh.write('#SBATCH -o ' + name + '.o' + '\n')
                subsh.write('crest ' +  filename + ' --noreftopo --nci  --T 16 > result.out' + '\n')


#    os.system('conda activate xtb')
    abs_path = os.path.abspath(foldername)

    for subdir, dirs, files in os.walk(foldername):
        for f in dirs:
            path = abs_path + '/' + f
            os.chdir(path)
            os.system('sbatch submit.sh')

