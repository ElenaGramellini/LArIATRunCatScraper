# Copyright (C) 2017-2017 Elena Gramellini <elena.gramellini@yale.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You can read copy of the GNU General Public License here:
# <http://www.gnu.org/licenses/>.
#
# To Do
# [ x ] read input as ttree file
# [   ] print event percentage

"""@Package docstring
Scope of this python script: 
Given a list of run, subrun, event
read from the lariat run catalogue and assess the beam conditions 

Author: Elena Gramellini

Creation Date: 2016-26-06 

Version 0 
-----------------------------------------------------------------------
Input:  csv file whose column are run, subrun, event  
Output: csv file whose column are run, N event for that run, magnet polarity, magnet current, secondary beam energy  
"""   

# Some reduntant import. 
# We probably use only requests, collections, ROOT and array
# But, you know, just in case
import ROOT,argparse
from ROOT import *
from array import array
import math
from collections import defaultdict

# This code takes as an argument 
# the root file generated by ScanPage.py
parser = argparse.ArgumentParser()
parser.add_argument("fname"   , nargs='?', default = 'RunIIPosBeamConditions.root', type = str, help="insert fileName")
args    = parser.parse_args()
fname   = args.fname


rFile = ROOT.TFile(fname)
rTree = rFile.Get('RunConditionsTTree')

evtsPerBeamCondition = defaultdict(int)
runsPerBeamCondition = defaultdict(int)
for entry in range(rTree.GetEntries()):
    rTree.GetEntry(entry)
    key = "Pol"+str(int(round(rTree.polarity)))+"_Curr"+str(int(round(rTree.current)))+"_Energy"+ str(int(round(rTree.energy)))
    evtsPerBeamCondition[key] += rTree.nevents
    runsPerBeamCondition[key] += 1


totEvts    = sum(evtsPerBeamCondition.values())
totRuns    = sum(runsPerBeamCondition.values())

stupidList = evtsPerBeamCondition.keys()
stupidList.sort()

crossCheck = 0
print "_____________ Events Breakdown _____________"
for k in stupidList:
    print k, evtsPerBeamCondition[k], 100*float(evtsPerBeamCondition[k])/float(totEvts),"%"
    crossCheck += evtsPerBeamCondition[k]

print
print "_____________ Runs Breakdown _____________"

for k in stupidList:
    print k, runsPerBeamCondition[k], 100*float(runsPerBeamCondition[k])/float(totRuns),"%"

print
print "_____________ Cross Check _____________"
print crossCheck,"=", totEvts, "?"
'''
# Define TFile and TTree
# The TTree has 1 enrty per run
f = TFile( outName+".root", 'recreate' )
t = TTree( 'RunConditionsTTree', 'tree' )

f.Close()
'''

raw_input()