#!/usr/bin/env python2.7
import sys, os, errno
from pcbnew import *


# Function to make directories... (is there anything built-in?)
def mkdir(name):
  try:
    os.makedirs(name)
  except OSError as e:
    if e.errno != errno.EEXIST:
      raise


# CONSTANTS 
BOARD_LAYERS = 2
DRILL_MAP = True


# Start of script: full filename is passed as the only argument
try:
  print("Loading file: %s" % sys.argv[1])
  fullname=sys.argv[1]
except:
  import glob
  fullname = glob.glob('./*.kicad_pcb')[0]

without_extension = os.path.splitext(fullname)[0]
# We removed extension, but not the name. Split the string at the slashes.
split = without_extension.split('/')
# Rejoin the string, but without the last split in the arr (and the first = '')
join = '';
for segment in split[1:len(split)-1]:
    join += '/' + segment;
path = join #The base path for exporting is the same as the .kicad_pcb file
print('Exporting to: %s' % path);

# We're outputting a lot of stuff... let's at least put it in one folder...
exp_dir = path + '/fab'
print('Base Export Directory: %s' % exp_dir)

# Dictionary of export types
exp_dict = { 'gerb': True,
             'pdf' : True,
             'dxf' : True,
             'hpgl': True,
             'post': True,
             'svg' : True,
             'und' : True,
           }

# Make directory for each export type
for output, enabled in exp_dict.items():
    print(output)
    print(enabled)
    mkdir(exp_dir)
    if(enabled):
        mkdir(exp_dir + '/' + output + '/')


# Load board
brd = LoadBoard(filename)

# Create Excellon files
drill = EXCELLON_WRITER(brd)
#drill.SetOptions(mirror, minimalHeader, offset, mergeNPTH)
drill.SetOptions(False, False, wxPoint(0,0), True)
#drill.SetFormat(metric)
drill.SetFormat(True)
#drill.CreateDrillandMapFilesSet(location, generateDrill, generateMap)
drill.CreateDrillandMapFilesSet(GERB_DIR, True, DRILL_MAP)
####
## NOTE: map is generated as a PDF by default?
## ... manually move it from gerb folder? does peter use this? just don't generate it?
## ... it is it usually generated as a gerber when going through the GUI?
####

# Create plotting object
pctl = PLOT_CONTROLLER(brd)

# Get current options of board?
# what is the point if this if we set them below?
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
popt.SetPlotReference(False)
popt.SetPlotValue(False)
popt.SetSubtractMaskFromSilk(True)
popt.SetUseGerberProtelExtensions(True)
#popt.SetUseGerberX2Format(False)

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
               #"F_Paste",
               "F_Mask",
               #"F_Fab",
               "B_Cu",
               "B_SilkS",
               #"B_Paste",
               "B_Mask",
               #"B_Fab",
               #"Eco2_User",
               #"Cmts_User",
               "Edge_Cuts"]

# TODO catch for invalid BOARD_LAYERS, do nothing for 2 layers, etc.
if BOARD_LAYERS == 4:
  gerb_layers.append("In1_Cu")
  gerb_layers.append("In2_Cu")

print "exporting layers: " + str(gerb_layers)

# Gerbers 
popt.SetOutputDirectory(GERB_DIR)
for name in gerb_layers:
    pctl.SetLayer(eval(name))
    # TODO: what does "bbb" mean below?
    pctl.OpenPlotfile(name, PLOT_FORMAT_GERBER, "bbb")
    pctl.PlotLayer()
pctl.ClosePlot()

# PDFs
popt.SetOutputDirectory(PDF_DIR)
for name in gerb_layers:
    pctl.SetLayer(eval(name))
    pctl.OpenPlotfile(name, PLOT_FORMAT_PDF, "bbb")
    pctl.PlotLayer()
pctl.ClosePlot()

# PDFs
popt.SetOutputDirectory(PDF_DIR)
for name in gerb_layers:
    pctl.SetLayer(eval(name))
    pctl.OpenPlotfile(name, PLOT_FORMAT_PDF, "bbb")
    pctl.PlotLayer()
pctl.ClosePlot()

# TODO: rename .gbr to .gts etc for Moko (aka Protel filenames)
