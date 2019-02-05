#!/usr/bin/env python2.7
import os
import pcbnew

# Get command line arguments (filename) 
try:
  filename=sys.argv[1]
except:
  import glob
  filename = glob.glob('./*.kicad_pcb')[0]
print("Loading file: %s" % filename)
# Might need this later
file_basename = os.path.splitext(filename)[0]

# Load board
brd = pcbnew.LoadBoard(filename)

for mod in brd.GetModules():
  print("* Module: %s at %s" % (mod.GetReference(), mod.GetPosition()))


