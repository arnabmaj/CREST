#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main module for orchestrating the CREST calculation workflow.
This module coordinates the conversion of molecular structures and submission
of CREST calculations through a series of steps.
"""

import logging
from pathlib import Path
import initial_convert
import packmol
import convert
import crest_calculation

class WorkflowManager:
    def __init__(self, working_dir: str = './'):
        self.working_dir = Path(working_dir)
        self._setup_logging()
        
    def _setup_logging(self) -> None:
        """Configure logging for the workflow manager."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def run_workflow(self) -> None:
        """Execute the complete CREST calculation workflow."""
        try:
            # Step 1: Convert input structures to PDB format
            self.logger.info("Step 1: Converting input structures to PDB format...")
            initial_convert.main()
            
            # Step 2: Create molecular pairs using PACKMOL
            self.logger.info("Step 2: Creating molecular pairs using PACKMOL...")
            packmol.main()
            
            # Step 3: Convert paired molecules to XYZ format
            self.logger.info("Step 3: Converting paired molecules to XYZ format...")
            convert.main()
            
            # Step 4: Submit CREST calculations
            self.logger.info("Step 4: Submitting CREST calculations...")
            crest_calculation.main()
            
            self.logger.info("Workflow completed successfully!")
            
        except Exception as e:
            self.logger.error(f"Workflow failed: {str(e)}")
            raise

def main():
    """Main function to run the CREST calculation workflow."""
    manager = WorkflowManager()
    manager.run_workflow()

if __name__ == '__main__':
    main()
