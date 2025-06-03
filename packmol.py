#!/usr/bin/env python
# -*- coding: utf-8 -*-


from itertools import combinations
import os
import glob
from os import listdir


def main():
    mypath = './'
    onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]

    pair_list = list(combinations(onlyfiles, 2))

    if os.path.exists('original_pdb_files') == False:
        os.makedirs('original_pdb_files')
     
    for molecule in onlyfiles:
        name = molecule.split('.pdb')[0]
        pair_name = name + '_' + name + '.inp'
        with open(pair_name, 'w') as pf:
                pf.write('tolerance 2.0' + '\n')
                pf.write('filetype pdb' + '\n')
                pf.write('output ' +  name + '_' + name + '.pdb' + '\n')
                pf.write('\n')
                pf.write('structure ' + molecule  + '\n')
                pf.write('  number 1' + '\n')
                pf.write('  inside box 0. 0. 0. 40. 40. 40.' + '\n')
                pf.write('end structure' + '\n')
                pf.write('\n')
                pf.write('structure ' + molecule  + '\n')
                pf.write('  number 1' + '\n')
                pf.write('  inside box 0. 0. 0. 40. 40. 40.' + '\n')
                pf.write('end structure' + '\n')

    for pair in pair_list:
        name1 = pair[0].split('.pdb')[0]
        name2 = pair[1].split('.pdb')[0]
        pair_name = name1 + '_' + name2 + '.inp'
        with open(pair_name, 'w') as pf:
                pf.write('tolerance 2.1' + '\n')
                pf.write('filetype pdb' + '\n')
                pf.write('output ' +  name1 + '_' + name2 + '.pdb' + '\n')
                pf.write('\n')
                pf.write('structure ' + pair[0]  + '\n')
                pf.write('  number 1' + '\n')
                pf.write('  inside box 0. 0. 0. 40. 40. 40.' + '\n')
                pf.write('end structure' + '\n')
                pf.write('\n')
                pf.write('structure ' + pair[1]  + '\n')
                pf.write('  number 1' + '\n')
                pf.write('  inside box 0. 0. 0. 40. 40. 40.' + '\n')
                pf.write('end structure' + '\n')

    allfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    for filename in allfiles:
        if '.inp' in filename: 
            os.system('/mnt/cephfs/home/arnabm/cpu_stuff/packmol/packmol < ' + filename + '> output')
    
    for filename in onlyfiles:
        os.system('mv ' + filename + ' original_pdb_files')

    os.system('rm output *.inp')
