#!/usr/bin/env python

import glob
import os

'''
This script converts pdb, mol, mol2, xyz and cif files into pdb files using obabel
It also saves the original files in the folder, 'originals'
'''
def main():
    if not os.path.exists('originals/'):
        os.makedirs('originals/')
    mol_files = glob.glob('originals/*')

    file_types = ('*.vasp','*.sdf','*.pdb','*.mol', '*.mol2', '*.cif', '*.xyz') # the tuple of file types
    all_files = []
    for filename in file_types:
        all_files.extend(sorted(glob.glob(filename)))

    mod = 'module load openbabel/2.4.1; '
    for filename in all_files:
        print('Processing: ' + filename)
        pdbfilename = filename.split('.')[0] + '.pdb'
        os.system(mod + 'obabel ' + filename + ' -O ' + pdbfilename)
        os.system('cp ' + '\'' + filename + '\'' + ' \'originals/' + filename + '\'')

# Organization:
    current_folder = os.listdir("./")
    for item in current_folder:
        if item.endswith(".cif"):
           os.remove(os.path.join("./", item))
        if item.endswith(".vasp"):
           os.remove(os.path.join("./", item))
        if item.endswith(".sdf"):
           os.remove(os.path.join("./", item))
        if item.endswith(".xyz"):
           os.remove(os.path.join("./", item))
        if item.endswith(".mol"):
           os.remove(os.path.join("./", item))
        if item.endswith(".mol2"):
           os.remove(os.path.join("./", item))
    print('File conversion complete.')
