#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for converting PDB files to XYZ format using OpenBabel.
This module handles the conversion of molecular structures from PDB to XYZ format,
which is required for CREST calculations.
"""

import os
from pathlib import Path
from typing import List
import subprocess
import logging

# Configuration
OPENBABEL_MODULE = 'openbabel/2.4.1'
XYZ_DIR = 'xyz_files'

class PDBToXYZConverter:
    def __init__(self, working_dir: str = './'):
        self.working_dir = Path(working_dir)
        self.xyz_dir = self.working_dir / XYZ_DIR
        self._setup_logging()
        
    def _setup_logging(self) -> None:
        """Configure logging for the converter."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        self.xyz_dir.mkdir(exist_ok=True)
    
    def get_pdb_files(self) -> List[str]:
        """Get list of PDB files in the working directory."""
        return sorted(self.working_dir.glob('*.pdb'))
    
    def convert_file(self, pdb_file: Path) -> None:
        """Convert a single PDB file to XYZ format using OpenBabel."""
        xyz_file = pdb_file.with_suffix('.xyz')
        self.logger.info(f'Converting {pdb_file.name} to XYZ format')
        
        try:
            # Load OpenBabel module and run conversion
            cmd = f'module load {OPENBABEL_MODULE}; obabel "{pdb_file}" -O "{xyz_file}"'
            subprocess.run(cmd, shell=True, check=True, capture_output=True)
            
            # Move XYZ file to xyz_files directory
            target_path = self.xyz_dir / xyz_file.name
            xyz_file.rename(target_path)
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f'Error converting {pdb_file.name}: {e.stderr.decode()}')
        except Exception as e:
            self.logger.error(f'Unexpected error converting {pdb_file.name}: {str(e)}')
    
    def cleanup(self) -> None:
        """Remove original PDB files after conversion."""
        for pdb_file in self.get_pdb_files():
            try:
                pdb_file.unlink()
            except Exception as e:
                self.logger.error(f'Error removing {pdb_file.name}: {str(e)}')

def main():
    """Main function to orchestrate the PDB to XYZ conversion workflow."""
    converter = PDBToXYZConverter()
    converter.setup_directories()
    
    pdb_files = converter.get_pdb_files()
    if not pdb_files:
        converter.logger.warning("No PDB files found in the current directory.")
        return
    
    converter.logger.info("Starting PDB to XYZ conversion...")
    for pdb_file in pdb_files:
        converter.convert_file(pdb_file)
    
    converter.cleanup()
    converter.logger.info("Conversion complete.")

if __name__ == '__main__':
    main()
