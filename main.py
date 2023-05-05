#Developed by Arnab Majumdar on 30th November 2022
#!/usr/bin/env python


import sys
import convert
import initial_convert
import packmol
import convert
import crest_calculation

initial_convert.main() # convert the input structure files
packmol.main() # pack the molecules into pairs of two using packmol 
convert.main() # convert the pair-ed molecules into xyz format as CREST can only read xyz
crest_calculation.main() # Submit all the CREST calculations
