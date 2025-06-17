#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for initial conversion of various molecular structure formats to PDB.
This module handles the conversion of multiple input formats (VASP, SDF, PDB, MOL, MOL2, CIF, XYZ)
to PDB format using OpenBabel.
"""

import os
from pathlib import Path
from typing import List, Set
import subprocess
import logging

# Configuration
OPENBABEL_MODULE = 'openbabel/2.4.1'
ORIGINALS_DIR = 'originals'
SUPPORTED_FORMATS = {
    'vasp': '*.vasp',
    'sdf': '*.sdf',
    'pdb': '*.pdb',
    'mol': '*.mol',
    'mol2': '*.mol2',
    'cif': '*.cif',
    'xyz': '*.xyz'
}

class StructureConverter:
    def __init__(self, working_dir: str = './'):
        self.working_dir = Path(working_dir)
        self.originals_dir = self.working_dir / ORIGINALS_DIR
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
        self.originals_dir.mkdir(exist_ok=True)
    
    def get_input_files(self) -> List[Path]:
        """Get list of all supported input files in the working directory."""
        input_files = []
        for pattern in SUPPORTED_FORMATS.values():
            input_files.extend(self.working_dir.glob(pattern))
        return sorted(input_files)
    
    def convert_file(self, input_file: Path) -> None:
        """Convert a single input file to PDB format using OpenBabel."""
        pdb_file = input_file.with_suffix('.pdb')
        self.logger.info(f'Processing: {input_file.name}')
        
        try:
            # Load OpenBabel module and run conversion
            cmd = f'module load {OPENBABEL_MODULE}; obabel "{input_file}" -O "{pdb_file}"'
            subprocess.run(cmd, shell=True, check=True, capture_output=True)
            
            # Copy original file to originals directory
            original_path = self.originals_dir / input_file.name
            input_file.rename(original_path)
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f'Error converting {input_file.name}: {e.stderr.decode()}')
        except Exception as e:
            self.logger.error(f'Unexpected error converting {input_file.name}: {str(e)}')
    
    def cleanup(self) -> None:
        """Remove original input files after conversion."""
        for fmt in SUPPORTED_FORMATS:
            for file in self.working_dir.glob(f'*.{fmt}'):
                try:
                    file.unlink()
                except Exception as e:
                    self.logger.error(f'Error removing {file.name}: {str(e)}')

def main():
    """Main function to orchestrate the structure conversion workflow."""
    converter = StructureConverter()
    converter.setup_directories()
    
    input_files = converter.get_input_files()
    if not input_files:
        converter.logger.warning("No supported input files found in the current directory.")
        return
    
    converter.logger.info("Starting structure conversion...")
    for input_file in input_files:
        converter.convert_file(input_file)
    
    converter.cleanup()
    converter.logger.info("File conversion complete.")

if __name__ == '__main__':
    main()
