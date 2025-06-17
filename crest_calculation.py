#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for submitting CREST calculations.
This module handles the creation of job submission scripts and directories
for CREST calculations on molecular structures.
"""

import os
from pathlib import Path
from typing import List
import shutil
import logging

# Configuration
CREST_CALC_DIR = 'crest_calculations'
SLURM_CONFIG = {
    'nodes': 1,
    'tasks_per_node': 16,
    'mem_per_cpu': '7G',
    'time': '500:00:00'
}
CREST_OPTIONS = '--noreftopo --nci --T 16'

class CRESTJobManager:
    def __init__(self, working_dir: str = './'):
        self.working_dir = Path(working_dir)
        self.crest_dir = self.working_dir / CREST_CALC_DIR
        self._setup_logging()
        
    def _setup_logging(self) -> None:
        """Configure logging for the job manager."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        self.crest_dir.mkdir(exist_ok=True)
    
    def get_xyz_files(self) -> List[Path]:
        """Get list of XYZ files in the working directory."""
        return sorted(self.working_dir.glob('*.xyz'))
    
    def create_job_directory(self, xyz_file: Path) -> Path:
        """Create a directory for a single CREST calculation."""
        job_dir = self.crest_dir / xyz_file.stem
        job_dir.mkdir(exist_ok=True)
        return job_dir
    
    def create_submission_script(self, job_dir: Path, xyz_file: Path) -> None:
        """Create a SLURM submission script for a CREST calculation."""
        script_path = job_dir / 'submit.sh'
        
        with open(script_path, 'w') as f:
            f.write('#!/bin/bash\n')
            f.write(f'#SBATCH -N {SLURM_CONFIG["nodes"]}\n')
            f.write(f'#SBATCH --tasks-per-node={SLURM_CONFIG["tasks_per_node"]}\n')
            f.write(f'#SBATCH --mem-per-cpu={SLURM_CONFIG["mem_per_cpu"]}\n')
            f.write(f'#SBATCH -t {SLURM_CONFIG["time"]}\n')
            f.write(f'#SBATCH -J {xyz_file.stem}\n')
            f.write(f'#SBATCH -o {xyz_file.stem}.o\n')
            f.write(f'crest {xyz_file.name} {CREST_OPTIONS} > result.out\n')
        
        # Make the script executable
        script_path.chmod(0o755)
    
    def setup_job(self, xyz_file: Path) -> None:
        """Set up a single CREST calculation job."""
        try:
            # Create job directory
            job_dir = self.create_job_directory(xyz_file)
            
            # Copy XYZ file to job directory
            shutil.copy2(xyz_file, job_dir)
            
            # Create submission script
            self.create_submission_script(job_dir, xyz_file)
            
            self.logger.info(f'Created CREST job setup for {xyz_file.name}')
            
        except Exception as e:
            self.logger.error(f'Error setting up job for {xyz_file.name}: {str(e)}')
    
    def submit_jobs(self) -> None:
        """Submit all CREST calculation jobs."""
        for job_dir in self.crest_dir.iterdir():
            if job_dir.is_dir():
                try:
                    os.chdir(job_dir)
                    os.system('sbatch submit.sh')
                    self.logger.info(f'Submitted job in {job_dir.name}')
                except Exception as e:
                    self.logger.error(f'Error submitting job in {job_dir.name}: {str(e)}')
                finally:
                    os.chdir(self.working_dir)

def main():
    """Main function to orchestrate the CREST calculation workflow."""
    manager = CRESTJobManager()
    manager.setup_directories()
    
    xyz_files = manager.get_xyz_files()
    if not xyz_files:
        manager.logger.warning("No XYZ files found in the current directory.")
        return
    
    manager.logger.info("Setting up CREST calculations...")
    for xyz_file in xyz_files:
        manager.setup_job(xyz_file)
    
    manager.logger.info("Submitting CREST jobs...")
    manager.submit_jobs()
    manager.logger.info("All jobs submitted successfully.")

if __name__ == '__main__':
    main()

