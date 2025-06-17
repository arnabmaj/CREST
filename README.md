# CREST
Automated CREST runs

Make sure that all the python files are in the same folder. 
The run the main.py file from the relevant folder where you want the calculations to be done.

We first take the crystal, molecular, nanostructures and then just run the main.py file. 
1. It first converts the structures into pdb
2. Then using packmol, it creates pairs of molecules
3. Then the paired molecules are converted to xyz as CREST only reads xyz
Then all the paired molecules are submitted for running using CREST
Still developing - The CREST results will be submitted for DFT Raman calculations using Gaussian.
