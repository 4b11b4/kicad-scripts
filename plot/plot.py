#!/usr/bin/env python2.7
import sys, os, errno
from pcbnew import *

# CONSTANTS 
LAYER_COUNT = 4
DRILL_MAP = True
ART_BOARD = True #TODO: act different if component or art board

# Helper function to make directories
def mkdir(name):
  try:
    os.makedirs(name)
  except OSError as e:
    if e.errno != errno.EEXIST:
      raise

# Get command line arguments (filename) 
try:
  filename=sys.argv[1]
except:
  import glob
  filename = glob.glob('./*.kicad_pcb')[0]
print("Loading file: %s" % filename)

EXPORT_DIR = sys.argv[2]
# TODO: handle path string incase '/' is already present
GERB_DIR = EXPORT_DIR + '/' + "gerb/"
PDF_DIR = EXPORT_DIR + '/' + 'pdf/'

# Might need this later
file_basename = os.path.splitext(filename)[0]

# Load board
brd = LoadBoard(filename)

# Create output folders
mkdir(EXPORT_DIR)
print "export dir: ({0})".format(EXPORT_DIR)
mkdir(GERB_DIR)
print "gerb dir: ({0})".format(GERB_DIR)

# Create Excellon files
drill = EXCELLON_WRITER(brd)
#drill.SetOptions(mirror, minimalHeader, offset, mergeNPTH)
drill.SetOptions(False, False, wxPoint(0,0), True)
#drill.SetFormat(metric)
drill.SetFormat(True)
#drill.CreateDrillandMapFilesSet(location, generateDrill, generateMap)
drill.CreateDrillandMapFilesSet(GERB_DIR, True, DRILL_MAP)
###
# NOTE: map is generated as a PDF by default?
# ... manually move it from gerb folder? does peter use this? just don't generate it?
# ... it is it usually generated as a gerber when going through the GUI?
###

# Create plotting object
pctl = PLOT_CONTROLLER(brd) 
# Get current options of board? what is the point if this if we set them below?
popt = pctl.GetPlotOptions()

# Gerber export 
# Set plot options 
# TODO: add rest of plot options from documentation
popt.SetPlotFrameRef(False)
popt.SetLineWidth(FromMM(0.1))
# TODO: what is auto scale? I dont see on GUI
popt.SetAutoScale(False)
popt.SetScale(1)
popt.SetMirror(False)
popt.SetUseGerberAttributes(False)
popt.SetExcludeEdgeLayer(True)
popt.SetUseAuxOrigin(False)

# TODO: investigate if possible to check for zone fills before exporting from python
# TODO: plot values/ref options for popt?
# TODO: subtract soldermask from silkscreen?

###
# TODO: change this to be inside the manufacturing repository and additionally...
# create flag to determine whether it ends up in a prototype folder or production folder
# name the folder based on this flag, give increasing verison number based on previous exports, time & date, etc.
###

gerb_layers = ["F_Cu",
               "F_SilkS",
               "F_Paste",
               "F_Mask",
               "F_Fab",
               "B_Cu",
               "B_SilkS",
               "B_Paste",
               "B_Mask",
               "B_Fab",
               "Eco2_User",
               "Cmts_User",
               "Edge_Cuts"]

# TODO catch for invalid LAYER_COUNT, do nothing for 2 layers, etc.
if LAYER_COUNT == 4:
  gerb_layers.append("In1_Cu")
  gerb_layers.append("In2_Cu")

print "exporting layers: " + str(gerb_layers)

# Generate Gerbers 
popt.SetOutputDirectory(GERB_DIR)
for name in gerb_layers:
    pctl.SetLayer(eval(name))
    # TODO: what does "bbb" mean below?
    pctl.OpenPlotfile(name, PLOT_FORMAT_GERBER, "bbb")
    pctl.PlotLayer()
pctl.ClosePlot()

# Generate PDFs
popt.SetOutputDirectory(PDF_DIR)
for name in gerb_layers:
    pctl.SetLayer(eval(name))
    # TODO: what does "bbb" mean below?
    pctl.OpenPlotfile(name, PLOT_FORMAT_PDF, "bbb")
    pctl.PlotLayer()
pctl.ClosePlot()

# TODO: rename .gbr to .gts etc for Moko (aka Protel filenames)
