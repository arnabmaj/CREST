#!/usr/bin/env python

"""
Created on 30th November, 2022
This code converts pdb files to xyz format using Obabel 2.4.1.

A new foler 'xyz_files' will be created with all the newly created xyz files.

Usage:
     # Run the code in the folder containing all the pdb files.

@author: Arnab Majumdar
"""

import os
import glob

def main():
    os.makedirs('xyz_files') # creating the 'xyz_files' folder
    mod = 'module load openbabel/2.4.1;' # loading the Obabel module
    print('Converting the files to xyz format')
    for filename in sorted(glob.glob('*.pdb')):
        xyzfilename = filename.split('.')[0] + '.xyz'
        os.system(mod + 'obabel ' + '\'' + filename + '\'' + ' -O ' + '\'' + xyzfilename + '\' >/dev/null 2>&1;') # converting pdb to xyz using obabel

    os.system('cp ' + '*.xyz ' + 'xyz_files/') # copying the new xyz files to the folder 'xyz_files'
    os.system('rm *.pdb')
