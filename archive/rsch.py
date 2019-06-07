#!/usr/bin/env python2.7

''' This file attempts to get a list of the components from the netlist.
'''

import sys, os, errno
from kinparse import parse_netlist

try: # Enter fn when running python file. eg: "python rsch.py [fn]"
  fn=sys.argv[1] # fn=filename
except:
  # If you don't enter a fn, but an existing file matches the
  # keyword below, it will find the file.
  # i.e. "first matching file in ./"
  import glob
  fn = glob.glob('./*.net')[0]

fn_base = os.path.splitext(fn)[0] # fn without the . extension

print("Loading file: %s" % fn)

# Load netlist 
nl = parse_netlist(fn)
print('Netlist generated from: {}'.format(nl.design.source.val))
