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


# Setup
## CONSTANTS 
DRILL_MAP_EN = True #print drl-map pdf
BOARD_NUM_LAYERS = 2 #2, 4...
LAYERS = ["F_Cu",
          #"F_Adhes",
          "F_Paste",
          "F_SilkS",
          "F_Mask",
          "B_Cu",
          #"B_Adhes",
          "B_Paste",
          "B_SilkS",
          "B_Mask",
          #"Dwgs_User",
          #"Cmts_User",
          #"Eco1_User",
          #"Eco2_User",
          "Edge_Cuts",
          #"Margin",
          #"F_CrtYd",
          #"F_Fab",
          #"B_CrtYd",
          #"B_Fab",
         ]
if BOARD_NUM_LAYERS == 4:
  LAYERS.append("In1_Cu")
  LAYERS.append("In2_Cu")

## Might as well check if the layers are correct at the start
print("Are you sure you want to export these layers?");
for layer in LAYERS: print(layer)
raw_input("[Warning] -- will overwrite files, press any key to continue:")

## Get only argument: full filename of .kicad_pcb file
try:
  print("Loading file: %s" % sys.argv[1])
  fullname=sys.argv[1]
except:
  import glob
  fullname = glob.glob('./*.kicad_pcb')[0]

## Remove file extension and name to get base path
without_extension = os.path.splitext(fullname)[0] #splitext vs split?
path = os.path.abspath(os.path.split(fullname)[0]) #get rid of splitting...
#The base path for exporting is at the .kicad_pcb file

## Put everything in one folder
exp_dir = path + '/fab';
print('Exporting to: %s' % exp_dir);

## Dictionary of possible export types
exp_dict = { 'dxf'   : 0,
             'gerber': 1,
             'hpgl'  : 0,
             'pdf'   : 1,
             'post'  : 1,
             'svg'   : 1,
             'undefined': 0 };
## If enabled, make directory
mkdir(exp_dir); # make the fab folder first
DIRS = {}; # will contain path for each enabled output type
for output, enabled in exp_dict.items():
    if(enabled):
        directory = exp_dir + '/' + output + '/'
        DIRS.update({output:directory})
        mkdir(directory)
# End Setup


# PCBnew Objects 
brd = LoadBoard(fullname) # Load board
## http://
pctl = PLOT_CONTROLLER(brd) # Create plotter
## http://
popt = pctl.GetPlotOptions() # Access plotter options
## http://docs.kicad-pcb.org/doxygen/classPCB__PLOT__PARAMS.html
drill = EXCELLON_WRITER(brd) # Create driller. Drill options set via driller.
## http://docs.kicad-pcb.org/doxygen/classEXCELLON__WRITER.html


# PCBnew Output
## Settings (TODO: check fill before export?)
drill.SetOptions(False, False, wxPoint(0,0), True) #mirror,min,offset,merge
drill.SetFormat(True) # T=metric, F=imperial
popt.SetAutoScale(False) #nodoc
popt.SetExcludeEdgeLayer(True) #from other layers
popt.SetLineWidth(FromMM(0.1))
popt.SetMirror(False) #diy boards
popt.SetPlotFrameRef(False) #nodoc
popt.SetPlotReference(False) #nodoc
popt.SetPlotValue(False) #nodoc
popt.SetScale(1)
popt.SetSubtractMaskFromSilk(True) #erase silk if no mask underneath
popt.SetUseAuxOrigin(False) #no additional origins are used
popt.SetUseGerberAttributes(False) #dont use attributes
popt.SetUseGerberProtelExtensions(True) #file extensions

## Generic Export (Iteration Over All Types)
for output, dire in DIRS.items(): #'dir' is a keyword
    popt.SetOutputDirectory(dire)
    PLOT_FORMAT_TYPE = 'PLOT_FORMAT_' + output.upper()
    print(PLOT_FORMAT_TYPE),
    for layer in LAYERS:
        print(layer),
        pctl.SetLayer(eval(layer))
        pctl.OpenPlotfile(layer, eval(PLOT_FORMAT_TYPE), "bbb")
        pctl.PlotLayer()
    pctl.ClosePlot()
    print('')

## Drill Export
drill.CreateDrillandMapFilesSet(DIRS['gerber'], True, DRILL_MAP_EN) #loc,drl,map
