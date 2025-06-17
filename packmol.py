#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for handling PACKMOL operations to create molecular pairs.
This module creates input files for PACKMOL to generate pairs of molecules
in a specified box size.
"""

import os
from itertools import combinations
from pathlib import Path
from typing import List, Tuple

# Configuration
BOX_SIZE = 40.0
TOLERANCE_SAME = 2.0
TOLERANCE_DIFF = 2.1
PACKMOL_PATH = '/mnt/cephfs/home/arnabm/cpu_stuff/packmol/packmol'

class PackmolHandler:
    def __init__(self, working_dir: str = './'):
        self.working_dir = Path(working_dir)
        self.original_pdb_dir = self.working_dir / 'original_pdb_files'
        
    def setup_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        self.original_pdb_dir.mkdir(exist_ok=True)
        
    def get_pdb_files(self) -> List[str]:
        """Get list of PDB files in the working directory."""
        return [f for f in os.listdir(self.working_dir) 
                if f.endswith('.pdb') and os.path.isfile(self.working_dir / f)]
    
    def create_packmol_input(self, filename: str, tolerance: float, 
                           output_name: str, structures: List[str]) -> None:
        """Create a PACKMOL input file with specified parameters."""
        with open(filename, 'w') as pf:
            pf.write(f'tolerance {tolerance}\n')
            pf.write('filetype pdb\n')
            pf.write(f'output {output_name}\n\n')
            
            for structure in structures:
                pf.write(f'structure {structure}\n')
                pf.write('  number 1\n')
                pf.write(f'  inside box 0. 0. 0. {BOX_SIZE} {BOX_SIZE} {BOX_SIZE}.\n')
                pf.write('end structure\n\n')
    
    def process_single_molecules(self, pdb_files: List[str]) -> None:
        """Process single molecules to create self-pairs."""
        for molecule in pdb_files:
            name = molecule.split('.pdb')[0]
            pair_name = f'{name}_{name}.inp'
            self.create_packmol_input(
                pair_name, 
                TOLERANCE_SAME,
                f'{name}_{name}.pdb',
                [molecule, molecule]
            )
    
    def process_molecule_pairs(self, pdb_files: List[str]) -> None:
        """Process pairs of different molecules."""
        for mol1, mol2 in combinations(pdb_files, 2):
            name1 = mol1.split('.pdb')[0]
            name2 = mol2.split('.pdb')[0]
            pair_name = f'{name1}_{name2}.inp'
            self.create_packmol_input(
                pair_name,
                TOLERANCE_DIFF,
                f'{name1}_{name2}.pdb',
                [mol1, mol2]
            )
    
    def run_packmol(self) -> None:
        """Run PACKMOL on all input files."""
        for filename in os.listdir(self.working_dir):
            if filename.endswith('.inp'):
                os.system(f'{PACKMOL_PATH} < {filename} > output')
    
    def cleanup(self, pdb_files: List[str]) -> None:
        """Clean up temporary files and move original PDB files."""
        for filename in pdb_files:
            os.rename(filename, self.original_pdb_dir / filename)
        os.remove('output')
        for filename in os.listdir(self.working_dir):
            if filename.endswith('.inp'):
                os.remove(filename)

def main():
    """Main function to orchestrate the PACKMOL workflow."""
    handler = PackmolHandler()
    handler.setup_directories()
    
    pdb_files = handler.get_pdb_files()
    if not pdb_files:
        print("No PDB files found in the current directory.")
        return
    
    handler.process_single_molecules(pdb_files)
    handler.process_molecule_pairs(pdb_files)
    handler.run_packmol()
    handler.cleanup(pdb_files)

if __name__ == '__main__':
    main()
